# -*- coding: utf-8 -*-
"""
:Author: HuangJianYi
:Date: 2020-06-02 13:44:17
:LastEditTime: 2021-02-24 15:59:23
:LastEditors: HuangJingCan
:description: 奖品相关
"""
from copy import deepcopy
from seven_cloudapp.handlers.seven_base import *

from seven_cloudapp.models.seven_model import *
from seven_cloudapp.models.enum import *

from seven_cloudapp.handlers.server.prize_s import PrizeDelHandler
from seven_cloudapp.handlers.server.prize_s import PrizeReleaseHandler

from seven_cloudapp_ppmt.models.db_models.act.act_prize_model import *


class PrizeListHandler(SevenBaseHandler):
    """
    :description: 奖品列表
    """
    @filter_check_params("machine_id")
    def get_async(self):
        """
        :description: 奖品列表
        :param act_id:活动id
        :param page_index:页索引
        :param page_size:页大小
        :param machine_id:机台id
        :return: 
        :last_editors: HuangJianYi
        """
        act_id = int(self.get_param("act_id", 0))
        page_index = int(self.get_param("page_index", 0))
        page_size = int(self.get_param("page_size", 10))
        machine_id = int(self.get_param("machine_id", 0))
        # field = "id,sort_index,prize_pic,unpack_pic,toys_pic,prize_name,prize_price,probability,prize_limit,surplus,prize_total,tag_id,is_sku,is_release,is_prize_notice,is_surplus,prize_detail,goods_code,goods_code_list,goods_id"
        condition = "machine_id=%s"

        if machine_id <= 0:
            return self.reponse_json_error_params()

        act_prize_model = ActPrizeModel()

        # 奖品总件数
        prize_all_count = act_prize_model.get_total("machine_id=%s", params=machine_id)
        # 库存不足奖品件数
        prize_surplus_count = act_prize_model.get_total("machine_id=%s AND prize_total=0", params=machine_id)
        # 可被抽中奖品件数
        prize_lottery_count = act_prize_model.get_total("machine_id=%s AND probability>0 AND prize_total>0 AND is_release=1", params=machine_id)
        #奖品总权重
        sum_probability = act_prize_model.get_dict("machine_id=%s and is_release=1", field="sum(probability) as probability", params=machine_id)

        page_list, total = act_prize_model.get_dict_page_list("*", page_index, page_size, condition, "", "sort_index desc", params=machine_id)

        for i in range(len(page_list)):
            # page_list[i]["prize_detail"] = self.json_loads(page_list[i]["prize_detail"])
            if page_list[i]["goods_code_list"] == "":
                page_list[i]["goods_code_list"] = "[]"
            page_list[i]["goods_code_list"] = self.json_loads(page_list[i]["goods_code_list"])

        page_info = PageInfo(page_index, page_size, total, page_list)
        page_info.prize_all_count = prize_all_count
        page_info.prize_surplus_count = prize_surplus_count
        page_info.prize_lottery_count = prize_lottery_count
        if sum_probability["probability"]:
            page_info.prize_sum_probability = int(sum_probability["probability"])
        else:
            page_info.prize_sum_probability = 0

        self.reponse_json_success(page_info)


class PrizeHandler(SevenBaseHandler):
    """
    :description: 奖品保存
    """
    @filter_check_params("app_id,act_id,machine_id")
    def post_async(self):
        """
        :description: 奖品保存
        :param prize_id：奖品id
        :return: reponse_json_success
        :last_editors: HuangJianYi
        """
        act_id = int(self.get_param("act_id", "0"))
        prize_id = int(self.get_param("prize_id", "0"))
        machine_id = int(self.get_param("machine_id", "0"))
        prize_type = int(self.get_param("prize_type", "0"))
        tag_id = int(self.get_param("tag_id", "1"))
        sort_index = int(self.get_param("sort_index", "0"))
        prize_pic = self.get_param("prize_pic", "")
        unpack_pic = self.get_param("unpack_pic")
        toys_pic = self.get_param("toys_pic")
        prize_name = self.get_param("prize_name")
        prize_price = self.get_param("prize_price")
        surplus = int(self.get_param("surplus", "0"))
        prize_total = int(self.get_param("prize_total", "0"))
        is_surplus = int(self.get_param("is_surplus", "0"))
        probability = int(self.get_param("probability", "0"))
        prize_limit = int(self.get_param("prize_limit", "0"))
        prize_detail = self.get_param("prize_detail", "")
        is_release = int(self.get_param("is_release", "1"))
        is_prize_notice = int(self.get_param("is_prize_notice", "1"))
        is_sku = int(self.get_param("is_sku", "0"))
        goods_id = int(self.get_param("goods_id", "0"))
        goods_code = self.get_param("goods_code")
        goods_code_list = self.get_param("goods_code_list")
        app_id = self.get_param("app_id")
        owner_open_id = self.get_param("owner_open_id")
        # self.logger_info.info(self.request.uri + "-PrizeHandler-保存奖品" + str(self.request_params))
        if act_id <= 0:
            return self.reponse_json_error_params()

        act_prize_model = ActPrizeModel()
        act_prize = None
        old_act_prize = None
        if prize_id > 0:
            act_prize = act_prize_model.get_entity_by_id(prize_id)

        if not act_prize:
            act_prize = ActPrize()
        else:
            old_act_prize = deepcopy(act_prize)

        act_prize.act_id = act_id
        act_prize.app_id = app_id
        act_prize.owner_open_id = owner_open_id
        act_prize.machine_id = machine_id
        act_prize.prize_type = prize_type
        act_prize.tag_id = tag_id
        act_prize.sort_index = sort_index
        act_prize.prize_pic = prize_pic if prize_pic != "" else unpack_pic
        act_prize.unpack_pic = unpack_pic
        act_prize.toys_pic = toys_pic
        act_prize.prize_name = prize_name
        act_prize.prize_price = prize_price
        act_prize.is_surplus = is_surplus
        act_prize.probability = probability
        act_prize.prize_limit = prize_limit
        act_prize.prize_detail = prize_detail if prize_detail != "" else json.dumps([])
        act_prize.modify_date = self.get_now_datetime()
        act_prize.is_release = is_release
        act_prize.is_prize_notice = is_prize_notice
        act_prize.is_sku = is_sku
        act_prize.goods_id = goods_id
        act_prize.goods_code = goods_code
        act_prize.goods_code_list = goods_code_list

        if prize_id > 0:
            if surplus > 0:
                act_prize.surplus = surplus
            self.create_operation_log(OperationType.add.value, act_prize.__str__(), "PrizeHandler", None, act_prize)
            act_prize_model.update_entity(act_prize)
            if surplus == 0:
                operate_num = prize_total - act_prize.prize_total
                act_prize_model.update_table(f"surplus=surplus+{operate_num},prize_total=prize_total+{operate_num}", "id=%s", act_prize.id)
        else:
            act_prize.create_date = act_prize.modify_date
            act_prize.surplus = surplus if surplus > 0 else prize_total
            act_prize.prize_total = prize_total
            act_prize.id = act_prize_model.add_entity(act_prize)
            self.create_operation_log(OperationType.update.value, act_prize.__str__(), "PrizeHandler", old_act_prize, act_prize)

        self.reponse_json_success(act_prize.id)

    @filter_check_params("app_id,act_id,machine_id")
    def get_async(self):
        """
        :description: 奖品保存
        :param prize_id：奖品id
        :return: reponse_json_success
        :last_editors: HuangJianYi
        """
        act_id = int(self.get_param("act_id", "0"))
        prize_id = int(self.get_param("prize_id", "0"))
        machine_id = int(self.get_param("machine_id", "0"))
        prize_type = int(self.get_param("prize_type", "0"))
        tag_id = int(self.get_param("tag_id", "0"))
        sort_index = int(self.get_param("sort_index", "0"))
        prize_pic = self.get_param("prize_pic", "")
        unpack_pic = self.get_param("unpack_pic")
        toys_pic = self.get_param("toys_pic")
        prize_name = self.get_param("prize_name")
        prize_price = self.get_param("prize_price")
        surplus = int(self.get_param("surplus", "0"))
        prize_total = int(self.get_param("prize_total", "0"))
        is_surplus = int(self.get_param("is_surplus", "0"))
        probability = int(self.get_param("probability", "0"))
        prize_limit = int(self.get_param("prize_limit", "0"))
        prize_detail = self.get_param("prize_detail", "")
        is_release = int(self.get_param("is_release", "1"))
        is_sku = int(self.get_param("is_sku", "0"))
        goods_id = int(self.get_param("goods_id", "0"))
        goods_code = self.get_param("goods_code")
        goods_code_list = self.get_param("goods_code_list")
        app_id = self.get_param("app_id")
        owner_open_id = self.get_param("owner_open_id")
        # self.logger_info.info(self.request.uri + "-PrizeHandler-保存奖品" + str(self.request_params))
        if act_id <= 0:
            return self.reponse_json_error_params()

        act_prize_model = ActPrizeModel()
        act_prize = None
        old_act_prize = None
        if prize_id > 0:
            act_prize = act_prize_model.get_entity_by_id(prize_id)

        if not act_prize:
            act_prize = ActPrize()
        else:
            old_act_prize = act_prize

        act_prize.act_id = act_id
        act_prize.app_id = app_id
        act_prize.owner_open_id = owner_open_id
        act_prize.machine_id = machine_id
        act_prize.prize_type = prize_type
        act_prize.tag_id = tag_id
        act_prize.sort_index = sort_index
        act_prize.prize_pic = prize_pic if prize_pic != "" else unpack_pic
        act_prize.unpack_pic = unpack_pic
        act_prize.toys_pic = toys_pic
        act_prize.prize_name = prize_name
        act_prize.prize_price = prize_price
        act_prize.is_surplus = is_surplus
        act_prize.probability = probability
        act_prize.prize_limit = prize_limit
        act_prize.prize_detail = prize_detail if prize_detail != "" else json.dumps([])
        act_prize.modify_date = self.get_now_datetime()
        act_prize.is_release = is_release
        act_prize.is_sku = is_sku
        act_prize.goods_id = goods_id
        act_prize.goods_code = goods_code
        act_prize.goods_code_list = goods_code_list

        if prize_id > 0:
            if surplus > 0:
                act_prize.surplus = surplus
            self.create_operation_log(OperationType.add.value, act_prize.__str__(), "PrizeHandler", None, act_prize)
            act_prize_model.update_entity(act_prize)
            if surplus == 0:
                operate_num = prize_total - act_prize.prize_total
                act_prize_model.update_table(f"surplus=surplus+{operate_num},prize_total=prize_total+{operate_num}", "id=%s", act_prize.id)
        else:
            act_prize.create_date = act_prize.modify_date
            act_prize.surplus = surplus if surplus > 0 else prize_total
            act_prize.prize_total = prize_total
            act_prize.id = act_prize_model.add_entity(act_prize)
            self.create_operation_log(OperationType.update.value, act_prize.__str__(), "PrizeHandler", old_act_prize, act_prize)

        self.reponse_json_success(act_prize.id)