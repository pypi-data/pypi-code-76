# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2020 p-cube.cn, Inc. All Rights Reserved
#
###############################################################################
"""
IntentEntity模型

Authors: fubo01
Date: 2020/03/11 00:00:00
"""

import json
import os
import copy
from typing import Dict

import torch
import torch.jit
from torch.utils.data import Dataset, DataLoader
import logging

from ..base.abstract import AbstractModelApp, AbstractDataSet
from ..base.common import ModelDataType, BerType, ModelState, Const
from ..base.common import CoachSettings, ModelSettings, DeviceSettings, ExportModelSettings
from ..base.model import IntentSlotModel
from ..base.model_data import IntentEntitySample
from ..base.model_dict import TagsDict, AbstractTagger
from ..base.tokenizer import BertTokenizer, AbstractTokenizer


class IntentEntityModelSettings(ModelSettings):
    """ Intent Entity模型配置 """

    # intent 类别数量
    intent_class_count: int = 0

    # entity 类别数量
    entity_class_count: int = 0

    # Dropout prob
    drop_out_prob: float = 0.5

    # 最大tokens长度
    max_tokens: int = 0


class IntentEntityCoachSettings(CoachSettings):
    """ Intent Entity训练参数配置 """

    # intent词典文件
    intent_label_dic: str = ""

    # 内部部entity词典文件
    entity_label_inner_dic: str = ""

    # 外部entity词典文件
    entity_label_dic: str = ""


class IntentEntityExportedModelSettings(ExportModelSettings):
    """ Intent Entity模型导出模型配置 """

    # intent词典文件
    intent_label_dic: str = ""

    # 内部部entity词典文件
    entity_label_inner_dic: str = ""

    # 外部entity词典文件
    entity_label_dic: str = ""

    # 最大tokens长度
    max_tokens: int = 0


class IntentEntityDataSet(AbstractDataSet):
    """
    Intent Entity 数据格式
    {"query": "", "intent_label": "", "entity_labels": [{"label": "", "pos":1, "len": 3}, ...]}
    """

    def __init__(self, intent_label: AbstractTagger, entity_label: AbstractTagger,
                 entity_inner_label: AbstractTagger, tokenizer: AbstractTokenizer
                 ):
        super().__init__()
        self.__intent_label = intent_label
        self.__entity_label = entity_label
        self.__entity_inner_label = entity_inner_label
        self.__tokenizer = tokenizer

    def get_intent_label_size(self):
        """
        获取intent label的数量
        :return:
        """
        return self.__intent_label.get_size()

    def get_entity_label_size(self):
        """
        获取entity label的数量
        :return:
        """
        return self.__entity_label.get_size()

    def get_entity_inner_label_size(self):
        """
        获取entity inner label的数量
        :return:
        """
        return self.__entity_inner_label.get_size()

    def parse_sample(self, line: str) -> Dict:
        """
        解析json格式的sample数据
        :param line:
        :return:
        """
        output = {"data": []}
        sample = IntentEntitySample.parse_raw(line)

        intent_label_idx = self.__intent_label.tag2id(sample.intent_label)
        if intent_label_idx < 0:
            logging.warning("Error format of line %s" % line)
            return {}

        tokens = self.__tokenizer.tokenize(sample.query)
        entity_idx = [self.__entity_inner_label.tag2id("O")] * self.__tokenizer.max_length

        tokens_str = "|".join([str(elem) for elem in tokens.padding_tokens])
        for pos, elem in enumerate(sample.token_labels):
            term_tokens = self.__tokenizer.tokenize(sample.query[elem.pos:elem.pos + elem.length])
            term_tokens_str = "|".join([str(elem) for elem in term_tokens.tokens])
            if term_tokens_str not in tokens_str:
                logging.warning("Error line intent label %s" % line)
                return {}
            pos = tokens_str.index(term_tokens_str)
            index = tokens_str[:pos].count("|")
            tokens_label = []
            if len(term_tokens.tokens) == 1:
                tokens_label = ["S-" + elem.label]

            if len(term_tokens.tokens) > 1:
                tokens_label_head = ["B-" + elem.label]
                tokens_label_tail = ["E-" + elem.label]
                tokens_label_body = ["I-" + elem.label] * (len(term_tokens.tokens) - 2)
                tokens_label = tokens_label_head + tokens_label_body + tokens_label_tail
            if len(tokens_label) == 0:
                logging.warning("Error line token label %s" % line)
                return {}
            tokens_label_idx = [self.__entity_inner_label.tag2id(label) for label in tokens_label]
            entity_idx[index:index + len(tokens_label)] = tokens_label_idx

        output["data"] = copy.deepcopy(tokens.padding_tokens)
        output["intent_label"] = intent_label_idx
        output["entity_label"] = entity_idx
        return output

    def __getitem__(self, index):
        return self.data[index]["data"], self.data[index]["intent_label"], self.data[index]["entity_label"]

    def __len__(self):
        return len(self.data)

    @staticmethod
    def collate_fn(batch):
        """
        数据封装
        :param batch: 数据batch
        :return:
        """
        data, intent_label, entity_label = zip(*batch)
        return torch.LongTensor(data), torch.LongTensor(list(intent_label)), torch.LongTensor(list(entity_label))


class IntentEntity(AbstractModelApp):
    """ Intent Entity """

    def __init__(
            self, device_settings: DeviceSettings,
            coach_settings: IntentEntityCoachSettings = IntentEntityCoachSettings(),
            model_settings: IntentEntityModelSettings = IntentEntityModelSettings(),
            export_settings: IntentEntityExportedModelSettings = IntentEntityExportedModelSettings()
    ):
        super().__init__(device_settings, coach_settings, model_settings, export_settings)
        self.device_settings = device_settings
        self.model_settings = model_settings
        self.coach_settings = coach_settings
        self.export_settings = export_settings
        self.intent_labeler = AbstractTagger()
        self.entity_labeler = AbstractTagger()
        self.entity_inner_labeler = AbstractTagger()
        self.tokenizer = AbstractTokenizer()
        self.loss_intent_func = None
        self.loss_entity_func = None

    def load_third_dict(self) -> bool:
        # 加载intent类别词典
        self.intent_labeler = TagsDict(
            tags_file=self.coach_settings.dict_dir + "/" + self.coach_settings.intent_label_dic
        )

        # 加载外部entity类别词典
        self.entity_labeler = TagsDict(
            tags_file=self.coach_settings.dict_dir + "/" + self.coach_settings.entity_label_dic
        )

        # 加载内部entity类别词典
        self.entity_inner_labeler = TagsDict(
            tags_file=self.coach_settings.dict_dir + "/" + self.coach_settings.entity_label_inner_dic
        )
        self.model_settings.intent_class_count = self.intent_labeler.get_size()
        self.model_settings.entity_class_count = self.entity_inner_labeler.get_size()

        # 加载分词
        self.tokenizer = BertTokenizer(
            max_sent_len=self.model_settings.max_tokens,
            bert_type=BerType.LITE_BERT
        )
        return True

    def define_data_pipe(self) -> Dataset:
        """ 创建数据集计算pipe """
        return IntentEntityDataSet(
            intent_label=self.intent_labeler,
            entity_label=self.entity_labeler,
            entity_inner_label=self.entity_inner_labeler,
            tokenizer=self.tokenizer
        )

    def define_model(self) -> bool:
        """
        定义模型
        :return: bool
        """
        self.model = IntentSlotModel(
            intent_class_count=self.model_settings.intent_class_count,
            entity_class_count=self.model_settings.entity_class_count,
            dropout_prob=self.model_settings.drop_out_prob,
            max_tokens=self.model_settings.max_tokens
        )
        return True

    def load_model_ckpt(self, model_path_ckpt) -> bool:
        """
        加载ckpt模型
        :param model_path_ckpt:
        :return:
        """
        # 模型配置文件
        config_file = model_path_ckpt + "/" + self.coach_settings.model_conf_file
        with open(config_file, "r") as fp:
            config_data = json.load(fp)
        self.coach_settings = IntentEntityCoachSettings.parse_obj(config_data["coach_settings"])
        self.model_settings = IntentEntityModelSettings.parse_obj(config_data["model_settings"])

        # 加载模型文件
        model_file = model_path_ckpt + "/" + self.coach_settings.model_file
        if self.define_model() is False:
            logging.error("Failed to define sent_similarity_model")
            return False
        try:
            self.model.load_state_dict(torch.load(model_file, map_location=torch.device("cpu")))
        except Exception as exp:
            logging.error("load sent_classifier_model params failed %s" % exp)
            return False

        return True

    def create_loss_optimizer(self) -> bool:
        """
        创建loss function和optimizer
        :return: bool
        """
        self.loss_intent_func = torch.nn.NLLLoss()
        self.loss_entity_func = torch.nn.NLLLoss()
        self.loss_func = torch.nn.NLLLoss()  # 未使用的loss function
        self.optimizer = torch.optim.Adam(
            self.get_model_params(),
            lr=self.coach_settings.lr, weight_decay=self.coach_settings.lr_weight_decay
        )
        return True

    def stop_criteria(self) -> (bool, int):
        """
        停止训练条件，如果不重载，则默认训练最长次数
        :return: bool, int
        """
        return False, -1

    def show_network_tf(self) -> bool:
        """
        在tensor board上画出network
        不实现函数则不画出网络图
        :return: bool
        """
        self.set_model_state(ModelState.INFERENCE)
        dummy_input = self.set_tensor_gpu(self.model.get_dummy_input())
        self.tb_logger.add_graph(self.model, dummy_input)
        self.set_model_state(ModelState.TRAIN)
        return True

    def epoch_train(self) -> bool:
        """
        使用训练数据进行一个epoch的训练
        :return: bool
        """
        train_data_loader = DataLoader(
            self.data_pipe_train,
            batch_size=self.coach_settings.train_batch_size,
            shuffle=True,
            collate_fn=IntentEntityDataSet.collate_fn,
        )
        self.set_model_state(model_state=ModelState.TRAIN)
        for _, (x, y1, y2) in enumerate(train_data_loader):
            x, y1, y2 = self.set_tensor_gpu(x), self.set_tensor_gpu(y1), self.set_tensor_gpu(y2)
            y1_, y2_ = self.model(x)
            y2_ = torch.transpose(y2_, dim0=2, dim1=1)
            loss = self.loss_intent_func(y1_, y1) + self.loss_entity_func(y2_, y2)
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
        return True

    def validation(self, epoch, data_type=ModelDataType.VALID) -> (bool, float):
        """
        验证当前效果
        :param epoch:
        :param data_type:
        :return: bool, average loss
        """
        loss_score = 0
        count_loss = 0

        correct_intent_count = 0
        intent_count = 0

        correct_entity_count = 0
        entity_count = 0

        data_loader = None
        if data_type == ModelDataType.VALID:
            data_loader = DataLoader(
                self.data_pipe_valid,
                batch_size=self.coach_settings.valid_batch_size,
                shuffle=False,
                collate_fn=IntentEntityDataSet.collate_fn,
            )
        if data_type == ModelDataType.TRAIN:
            data_loader = DataLoader(
                self.data_pipe_train,
                batch_size=self.coach_settings.train_batch_size,
                shuffle=False,
                collate_fn=IntentEntityDataSet.collate_fn,
            )
        if data_loader is None:
            return False, 0.0

        self.set_model_state(model_state=ModelState.INFERENCE)
        for _, (x, y1, y2) in enumerate(data_loader):
            x, y1, y2 = self.set_tensor_gpu(x), self.set_tensor_gpu(y1), self.set_tensor_gpu(y2)
            y1_, y2_ = self.model(x)
            y2_ = torch.transpose(y2_, dim0=2, dim1=1)
            loss_score = loss_score + float(self.loss_intent_func(y1_, y1) + self.loss_entity_func(y2_, y2))
            count_loss = count_loss + 1

            correct_intent_count = correct_intent_count + int(torch.sum(torch.eq(torch.max(y1_, dim=1)[1], y1)))
            intent_count = intent_count + y1.shape[0]

            # to-do 添加entity acc
            correct_entity_count = correct_entity_count + int(torch.sum(torch.eq(y2, torch.max(y2_, dim=1)[1])))
            entity_count = entity_count + y2.shape[0] * y2.shape[1]

        # 平均loss
        ave_loss = (1.0 * loss_score) / (count_loss + Const.MIN_POSITIVE_NUMBER)
        intent_acc = (1.0 * correct_intent_count) / (intent_count + Const.MIN_POSITIVE_NUMBER)
        entity_acc = (1.0 * correct_entity_count) / (entity_count + Const.MIN_POSITIVE_NUMBER)
        logging.info(
            "Valid data Dataset %s IntentCorrectCount %d IntentCount %d IntentAcc=%s" % (
                data_type, correct_intent_count, intent_count, str(intent_acc)
            )
        )

        logging.info(
            "Valid data Dataset %s EntityCorrectCount %d EntityCount %d EntityAcc=%s" % (
                data_type, correct_entity_count, entity_count, str(entity_acc)
            )
        )
        return True, ave_loss

    def release_model(self, model_path_ckpt: str, model_path_script: str) -> bool:
        """
        发布模型（TorchScript模型）
        :param model_path_ckpt ckpt的模型文件夹
        :param model_path_script torch script模型文件夹
        :return:
        """
        os.system("rm -rf %s" % model_path_script)
        os.system("mkdir -p %s" % model_path_script)

        # 生成模型配置清单
        export_model_settings = IntentEntityExportedModelSettings(
            model_config_file="config.json",
            model_file="model.pt",
            third_dict_dir="dict",
            intent_label_dic=self.coach_settings.intent_label_dic,
            entity_label_inner_dic=self.coach_settings.entity_label_inner_dic,
            entity_label_dic=self.coach_settings.entity_label_dic,
            max_tokens=self.model_settings.max_tokens
        )
        dict_path = model_path_script + "/" + export_model_settings.third_dict_dir
        model_file = model_path_script + "/" + export_model_settings.model_file
        config_file = model_path_script + "/" + export_model_settings.model_config_file
        try:
            with open(config_file, "w") as fp:
                fp.write(export_model_settings.json())
        except Exception as ex:
            logging.error("Failed to save sent_classify_model.config %s" % ex)
            return False

        # 打包第三方词典
        os.system("mkdir %s" % dict_path)
        os.system(
            "cp -rf %s %s/" % (
                self.coach_settings.dict_dir + "/" + self.coach_settings.intent_label_dic, dict_path
            )
        )
        os.system(
            "cp -rf %s %s/" % (
                self.coach_settings.dict_dir + "/" + self.coach_settings.entity_label_dic, dict_path
            )
        )
        os.system(
            "cp -rf %s %s/" % (
                self.coach_settings.dict_dir + "/" + self.coach_settings.entity_label_inner_dic, dict_path
            )
        )

        # 生成torch script模型文件
        try:
            self.model.eval()
            dummy_input = self.model.get_dummy_input()
            torch.jit.trace(self.model, dummy_input).save(model_file)
        except Exception as ex:
            logging.error("Failed to export sent_classify_model %s" % ex)
            return False

    def load_released_model(self, model_path_script: str) -> bool:
        """
        加载发布的模型及其相关的词典（TorchScript模型）
        :param model_path_script torch script模型文件夹
        :return:
        """
        # 解析model config
        config_file = model_path_script + "/config.json"
        try:
            export_model_settings = IntentEntityExportedModelSettings.parse_file(path=config_file)
        except Exception as ex:
            logging.error("Failed to load sent_classify_model config file %s " % ex)
            return False

        dict_path = model_path_script + "/" + export_model_settings.third_dict_dir
        model_file = model_path_script + "/" + export_model_settings.model_file
        intent_label_dic = dict_path + "/" + export_model_settings.intent_label_dic
        entity_label_dic = dict_path + "/" + export_model_settings.token_label_dic
        entity_label_inner_dic = dict_path + "/" + export_model_settings.token_label_inner_dic

        # 加载模型文件
        self.model = torch.jit.load(model_file, map_location=torch.device('cpu'))

        # 读取Intent词典
        self.intent_labeler = TagsDict(tags_file=intent_label_dic)

        # 读取内部entity词典
        self.entity_inner_labeler = TagsDict(tags_file=entity_label_inner_dic)

        # 读取外部entity词典
        self.entity_labeler = TagsDict(tags_file=entity_label_dic)

        # 加载分词
        self.tokenizer = BertTokenizer(
            max_sent_len=export_model_settings.max_tokens,
            bert_type=BerType.LITE_BERT
        )

        # 定义datapipe
        self.data_pipe = IntentEntityDataSet(
            intent_label=self.intent_labeler,
            entity_label=self.entity_labeler,
            entity_inner_label=self.entity_inner_labeler,
            tokenizer=self.tokenizer
        )

        return True

    def inference(self, query: str) -> dict:
        """
        inference 接口
        :param query:
        :return:
        """
        data_str = IntentEntitySample(query=query, intent_label=self.intent_labeler.id2tag(0), entity_labels=[]).json()
        if self.data_pipe is None:
            logging.error("No valid data pipe")
            return {}
        data = self.data_pipe.parse_sample(data_str)
        tokens = torch.LongTensor([data["data"]])
        intent_result, entity_result = self.model(tokens)
        intent_label_idx = int(torch.argmax(intent_result, dim=1)[0])
        entity_labels_idx = torch.argmax(entity_result, dim=2)[0].tolist()

        output = {
            "query": query,
            "intent_label": self.intent_labeler.id2tag(intent_label_idx),
            "entity_labels": [],
            "entities": []
        }
        str_tokens = self.tokenizer.convert_ids_to_tokens(data["data"])
        for index, elem in enumerate(entity_labels_idx):

            token = str_tokens[index]
            label = self.entity_inner_labeler.id2tag(elem)

            if token == self.tokenizer.padding:
                break
            output["entity_labels"].append({"token": token, "label": label})
        return output
