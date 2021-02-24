# -*- coding: utf-8 -*-
"""
:Author: HuangJianYi
:Date: 2020-05-26 17:51:04
:LastEditTime: 2021-02-24 15:57:52
:LastEditors: HuangJingCan
:Description: 抽奖
"""
import random
import datetime
from seven_cloudapp.handlers.seven_base import *

from seven_cloudapp.models.behavior_model import *
from seven_cloudapp.models.db_models.user.user_info_model import *
from seven_cloudapp.models.db_models.prize.prize_order_model import *
from seven_cloudapp.models.db_models.gear.gear_value_model import *
from seven_cloudapp.models.db_models.price.price_gear_model import *
from seven_cloudapp.models.db_models.coin.coin_order_model import *
from seven_cloudapp.models.db_models.machine.machine_value_model import *
from seven_cloudapp.models.db_models.surplus.surplus_queue_model import *

from seven_cloudapp_ppmt.models.db_models.act.act_info_model import *
from seven_cloudapp_ppmt.models.db_models.act.act_prize_model import *
from seven_cloudapp_ppmt.models.db_models.machine.machine_info_model import *
from seven_cloudapp_ppmt.models.db_models.prize.prize_roster_model import *


class LotteryHandler(SevenBaseHandler):
    """
    :description: 抽奖
    """
    def get_async(self):
        """
        :description: 抽奖
        :param prize_id:奖品id
        :param login_token:登录令牌
        :param act_id:活动id
        :param real_name:用户名
        :param telephone:电话
        :param province:省
        :param city:市
        :param county:区县
        :param street:街道
        :param address:地址
        :return: 抽奖
        :last_editors: HuangJianYi
        """
        open_id = self.get_taobao_param().open_id
        app_id = self.get_taobao_param().source_app_id
        prize_id = int(self.get_param("prize_id", 0))
        login_token = self.get_param("login_token")
        act_id = int(self.get_param("act_id", 0))
        real_name = self.get_param("real_name")
        telephone = self.get_param("telephone")
        province = self.get_param("province")
        city = self.get_param("city")
        county = self.get_param("county")
        street = self.get_param("street")
        address = self.get_param("address")

        db_transaction = DbTransaction(db_config_dict=config.get_value("db_cloudapp"))
        user_info_model = UserInfoModel(db_transaction=db_transaction)
        gear_value_model = GearValueModel(db_transaction=db_transaction)
        prize_roster_model = PrizeRosterModel(db_transaction=db_transaction)
        act_prize_model = ActPrizeModel(db_transaction=db_transaction)
        coin_order_model = CoinOrderModel(db_transaction=db_transaction)
        surplus_queue_model = SurplusQueueModel(db_transaction=db_transaction)
        prize_order_model = PrizeOrderModel(db_transaction=db_transaction)
        #请求太频繁限制
        if self.check_post(f"Lottery_Post_{act_id}_{str(open_id)}_{str(prize_id)}") == False:
            return self.reponse_json_error("HintMessage", "对不起，请求太频繁")
        user_info = user_info_model.get_entity("act_id=%s and open_id=%s", params=[act_id, open_id])
        if not user_info:
            return self.reponse_json_error("NoUser", "对不起，用户不存在")
        if user_info.user_state == 1:
            return self.reponse_json_error("UserState", "对不起，你是黑名单用户,无法抽盲盒")
        if user_info.login_token != login_token:
            return self.reponse_json_error("ErrorToken", "对不起，已在另一台设备登录,当前无法抽盲盒")

        act_info_model = ActInfoModel()
        act_info = act_info_model.get_entity("id=%s and is_release=1", params=act_id)
        if not act_info:
            return self.reponse_json_error("NoAct", "对不起，活动不存在")

        now_date = self.get_now_datetime()
        if TimeHelper.format_time_to_datetime(now_date) < TimeHelper.format_time_to_datetime(act_info.start_date):
            return self.reponse_json_error("NoAct", "活动将在" + act_info.start_date + "开启")
        if TimeHelper.format_time_to_datetime(now_date) > TimeHelper.format_time_to_datetime(act_info.end_date):
            return self.reponse_json_error("NoAct", "活动已结束")

        act_prize = act_prize_model.get_entity_by_id(prize_id)
        if not act_prize:
            return self.reponse_json_error("NoPrize", "对不起，奖品不存在")

        surplus_queue = surplus_queue_model.get_entity("app_id=%s and open_id=%s and prize_id=%s", params=[app_id, open_id, prize_id])
        if not surplus_queue:
            return self.reponse_json_error("NoPrize", "对不起，请重新选择盲盒")

        machine_info_model = MachineInfoModel()
        machine_info = machine_info_model.get_entity("id=%s and is_release=1", params=act_prize.machine_id)
        if not machine_info:
            return self.reponse_json_error("NoMachine", "对不起，盒子不存在")

        if machine_info.sale_type == 2:
            sale_date_str = str(machine_info.sale_date)
            sale_date = TimeHelper.format_time_to_datetime(sale_date_str if sale_date_str != "0000-00-00 00:00:00" else now_date)
            if TimeHelper.format_time_to_datetime(now_date) < sale_date:
                china_sale_date = sale_date.month + "月" + sale_date.day + "日" + sale_date.hour + "点"
                return self.reponse_json_error("NoStart", "该商品" + china_sale_date + "开售,敬请期待~")

        price_gear_model = PriceGearModel()
        price_gear = price_gear_model.get_entity("id=%s", params=machine_info.price_gears_id)
        if not price_gear:
            return self.reponse_json_error("NoPriceGear", "对不起，价格档位不存在")
        gear_value = gear_value_model.get_entity("act_id=%s and open_id=%s and price_gears_id=%s", params=[act_id, open_id, price_gear.id])
        if not gear_value or gear_value.current_value <= 0:
            return self.reponse_json_error("NoLotteryCount", "对不起，次数不足")
        now_date = self.get_now_datetime()
        prize_order_id = 0
        #抽奖
        try:
            #创建订单
            prize_order = PrizeOrder()
            prize_order.app_id = app_id
            prize_order.open_id = open_id
            prize_order.act_id = act_id
            prize_order.user_nick = user_info.user_nick
            prize_order.real_name = real_name
            prize_order.telephone = telephone
            prize_order.province = province
            prize_order.city = city
            prize_order.county = county
            prize_order.street = street
            prize_order.adress = address
            prize_order.create_date = now_date
            prize_order.modify_date = now_date
            prize_order.order_no = self.create_order_id()
            prize_order_id = prize_order_model.add_entity(prize_order)
            if prize_order_id <= 0:
                return self.reponse_json_error("Error", "对不起，请重新选择")

            db_transaction.begin_transaction()
            #扣除用户次数
            gear_value.current_value -= 1
            gear_value.modify_date = now_date
            gear_value_model.update_entity(gear_value)

            #录入用户奖品
            prize_roster = PrizeRoster()
            prize_roster.app_id = app_id
            prize_roster.act_id = act_id
            prize_roster.open_id = open_id
            prize_roster.machine_id = act_prize.machine_id
            prize_roster.machine_name = machine_info.machine_name
            prize_roster.machine_price = machine_info.machine_price
            prize_roster.series_id = machine_info.series_id
            prize_roster.prize_pic = act_prize.unpack_pic
            prize_roster.toys_pic = act_prize.toys_pic
            prize_roster.prize_id = act_prize.id
            prize_roster.prize_name = act_prize.prize_name
            prize_roster.prize_price = act_prize.prize_price
            prize_roster.prize_detail = act_prize.prize_detail
            prize_roster.tag_id = act_prize.tag_id
            prize_roster.user_nick = user_info.user_nick
            prize_roster.is_sku = act_prize.is_sku
            prize_roster.goods_code = act_prize.goods_code
            prize_roster.goods_code_list = act_prize.goods_code_list
            prize_roster.prize_order_no = prize_order.order_no
            prize_roster.order_status = 1
            prize_roster.create_date = now_date

            #录入用户开盒次数
            machine_value_model = MachineValueModel()
            machine_value = machine_value_model.get_entity("act_id=%s and machine_id=%s and open_id=%s", params=[act_id, act_prize.machine_id, open_id])
            if not machine_value:
                machine_value = MachineValue()
                machine_value.act_id = act_id
                machine_value.app_id = app_id
                machine_value.open_id = open_id
                machine_value.machine_id = act_prize.machine_id
                machine_value.open_value = 1
                machine_value.create_date = now_date
                machine_value.modify_date = now_date
                machine_value_model.add_entity(machine_value)
            else:
                machine_value.open_value += 1
                machine_value.modify_date = now_date
                machine_value_model.update_entity(machine_value)

            #添加商家对帐记录
            coin_order = None
            coin_order_set = coin_order_model.get_entity("act_id=%s and price_gears_id=%s and open_id=%s and pay_order_id=0 and surplus_count>0", "id asc", params=[act_id, machine_info.price_gears_id, open_id])

            if coin_order_set:
                coin_order_set.surplus_count = coin_order_set.surplus_count - 1
                coin_order_set.prize_ids = coin_order_set.prize_ids + "," + str(act_prize.id) if len(coin_order_set.prize_ids) > 0 else str(act_prize.id)
                coin_order = coin_order_set
            else:
                coin_order_pay = coin_order_model.get_entity("act_id=%s and price_gears_id=%s and open_id=%s and pay_order_id>0 and surplus_count>0", "id asc", params=[act_id, machine_info.price_gears_id, open_id])
                if coin_order_pay:
                    coin_order_pay.surplus_count = coin_order_pay.surplus_count - 1
                    coin_order_pay.prize_ids = coin_order_pay.prize_ids + "," + str(act_prize.id) if len(coin_order_pay.prize_ids) > 0 else str(act_prize.id)
                    coin_order = coin_order_pay

            if coin_order != None:
                coin_order_model.update_entity(coin_order)
                prize_roster.main_pay_order_no = coin_order.main_pay_order_no
                prize_roster.order_no = coin_order.pay_order_no
                if coin_order.pay_order_no != "":
                    prize_roster.frequency_source = 0
                else:
                    prize_roster.frequency_source = 1

            prize_roster.prize_order_id = prize_order_id
            prize_roster_model.add_entity(prize_roster)
            #库存处理
            act_prize_model.update_table("hand_out=hand_out+1,prize_total=prize_total-1", "id=%s", act_prize.id)
            surplus_queue_model.del_entity("id=%s", params=[surplus_queue.id])
            result_prize = {}
            result_prize["prize_name"] = act_prize.prize_name
            result_prize["prize_id"] = act_prize.id
            result_prize["unpack_pic"] = act_prize.unpack_pic
            result_prize["tag_id"] = act_prize.tag_id
            result_prize["prize_detail"] = self.json_loads(act_prize.prize_detail)
            if user_info.user_nick:
                length = len(user_info.user_nick)
                if length > 2:
                    result_prize["user_nick"] = user_info.user_nick[0:length - 2] + "**"
                else:
                    result_prize["user_nick"] = user_info.user_nick[0:1] + "*"
            behavior_model = BehaviorModel()
            behavior_model.report_behavior_log(app_id, act_id, open_id, act_info.owner_open_id, 'openUserCount_' + str(machine_info.id), 1)
            behavior_model.report_behavior_log(app_id, act_id, open_id, act_info.owner_open_id, 'openCount_' + str(machine_info.id), 1)
            behavior_model.report_behavior_log(app_id, act_id, open_id, act_info.owner_open_id, 'LotteryerCount', 1)
            behavior_model.report_behavior_log(app_id, act_id, open_id, act_info.owner_open_id, 'LotteryCount', 1)
            db_transaction.commit_transaction()

            self.reponse_json_success(result_prize)
        except Exception as ex:
            db_transaction.rollback_transaction()
            self.logger_info.info("LotteryHandler:" + str(ex))
            if prize_order_id > 0:
                prize_order_model.del_entity("id=%s", params=prize_order_id)


class ShakeItHandler(SevenBaseHandler):
    """
    :description: 晃一晃
    """
    @filter_check_params("prize_id,key_id,login_token,act_id")
    def get_async(self):
        """
        :description: 晃一晃
        :param prize_id:奖品id
        :param key_id:key_id
        :param login_token:登录令牌
        :param act_id:活动id
        :param serial_no:serial_no
        :return: dict
        :last_editors: HuangJianYi
        """
        open_id = self.get_taobao_param().open_id
        app_id = self.get_taobao_param().source_app_id
        prize_id = int(self.get_param("prize_id", 0))
        key_id = int(self.get_param("key_id", 0))
        login_token = self.get_param("login_token")
        act_id = int(self.get_param("act_id", 0))
        serial_no = int(self.get_param("serial_no", 0))

        user_info_model = UserInfoModel()
        act_info_model = ActInfoModel()
        act_prize_model = ActPrizeModel()
        surplus_queue_model = SurplusQueueModel()
        # self.logger_info.info(str(serial_no) + "【serial_no】")
        info = {}
        info["prize_name"] = ""
        info["prize_id"] = ""
        info["tips"] = ""
        info["is_limit"] = 1

        user_info = user_info_model.get_entity("open_id=%s and act_id=%s", params=[open_id, act_id])
        if not user_info:
            return self.reponse_json_error("NoUser", "对不起，用户不存在")
        if user_info.user_state == 1:
            return self.reponse_json_error("UserState", "对不起，你是黑名单用户,无法拆盒子")
        if user_info.login_token != login_token:
            return self.reponse_json_error("ErrorToken", "对不起，已在另一台设备登录,当前无法抽盲盒")

        act_info_model = ActInfoModel()
        act_info = act_info_model.get_entity("id=%s and is_release=1", params=[act_id])
        if not act_info:
            return self.reponse_json_error("NoAct", "对不起，活动不存在")

        now_date = self.get_now_datetime()
        if TimeHelper.format_time_to_datetime(now_date) < TimeHelper.format_time_to_datetime(act_info.start_date):
            return self.reponse_json_error("NoAct", "活动将在" + act_info.start_date + "开启")
        if TimeHelper.format_time_to_datetime(now_date) > TimeHelper.format_time_to_datetime(act_info.end_date):
            return self.reponse_json_error("NoAct", "活动已结束")

        act_prize = act_prize_model.get_entity_by_id(prize_id)
        if not act_prize:
            return self.reponse_json_error("NoPrize", "对不起，奖品不存在")

        surplus_queue = surplus_queue_model.get_entity("open_id=%s and prize_id=%s", params=[open_id, prize_id])
        if not surplus_queue:
            return self.reponse_json_error("NoPrize", "对不起，请重新选择盲盒")

        machine_info_model = MachineInfoModel()
        machine_info = machine_info_model.get_entity("id=%s and is_release=1", params=act_prize.machine_id)
        if not machine_info:
            return self.reponse_json_error("NoMachine", "对不起，盒子不存在")
        if machine_info.sale_type == 2:
            sale_date = TimeHelper.format_time_to_datetime(machine_info.sale_date)
            if TimeHelper.format_time_to_datetime(now_date) < sale_date:
                china_sale_date = sale_date.month + "月" + sale_date.day + "日" + sale_date.hour + "点"
                return self.reponse_json_error("NoStart", "该商品" + china_sale_date + "开售,敬请期待~")
        shakebox_tips_list = self.json_loads(act_info.shakebox_tips)
        if len(shakebox_tips_list) <= 0:
            info["tips"] = act_info.exceed_tips
            return self.reponse_json_success(info)
        ran_num_list = []
        for i in range(len(shakebox_tips_list)):
            if i == 0:
                for j in range(7):
                    ran_num_list.append(i)
            else:
                ran_num_list.append(i)
        ran_num = random.randint(0, int(len(ran_num_list) - 1))
        ran_num = int(ran_num_list[ran_num])
        # self.logger_info.info(str(ran_num_list)+"--" + str(ran_num) + "【ran_num_list】")
        incre_key = str(prize_id)
        if machine_info.is_repeat_prize == 1 and serial_no > 0:
            incre_key = str(prize_id) + "-" + str(serial_no)
        redis_num_key = "shakebox_tipsnumlist_" + str(open_id) + "_" + str(act_prize.machine_id) + "_" + str(key_id)
        shakebox_tipsnumlist = self.redis_init().get(redis_num_key)
        if shakebox_tipsnumlist != None:
            shakebox_tipsnumlist = self.json_loads(shakebox_tipsnumlist)
        else:
            shakebox_tipsnumlist = {}
        num = shakebox_tipsnumlist[incre_key] if incre_key in shakebox_tipsnumlist.keys() else 0
        if int(num) >= int(act_info.shakebox_tips_num):
            info["tips"] = act_info.exceed_tips
            return self.reponse_json_success(info)
        if ran_num == 0:
            redis_prizelist_key = "shakebox_tipsprizelist_" + str(open_id) + "_" + str(act_prize.machine_id) + "_" + str(key_id)
            shakebox_tipsprizelist = self.redis_init().get(redis_prizelist_key)
            if shakebox_tipsprizelist != None:
                shakebox_tipsprizelist = self.json_loads(shakebox_tipsprizelist)
            else:
                shakebox_tipsprizelist = {}
            prize_list = shakebox_tipsprizelist[incre_key] if incre_key in shakebox_tipsprizelist.keys() else []
            cur_prize = None
            exclude_Prizeid_list = [prize_id]
            if len(prize_list) > 0:
                exclude_Prizeid_list.extend(prize_list)
            exclude_Prizeid_ids = ','.join(str(prize_id) for prize_id in exclude_Prizeid_list)
            condition = f"machine_id={act_prize.machine_id} and id not in ({exclude_Prizeid_ids}) and is_release=1 and tag_id=1"
            cur_prize = act_prize_model.get_entity(condition, order_by="RAND()")
            if cur_prize is not None:
                info["tips"] = shakebox_tips_list[0].replace("XX", cur_prize.prize_name)
                info["prize_name"] = cur_prize.prize_name
                info["prize_id"] = cur_prize.id
                info["is_limit"] = 0
                prize_list.append(cur_prize.id)
                shakebox_tipsnumlist[incre_key] = int(num + 1)
                shakebox_tipsprizelist[incre_key] = prize_list
                self.redis_init().set(redis_num_key, self.json_dumps(shakebox_tipsnumlist), ex=3600 * 1)
                self.redis_init().set(redis_prizelist_key, self.json_dumps(shakebox_tipsprizelist), ex=3600 * 1)
            else:
                info["tips"] = act_info.exceed_tips
        else:
            info["tips"] = shakebox_tips_list[ran_num]
            info["is_limit"] = 0

        self.reponse_json_success(info)


class ShakeItPrizeListHandler(SevenBaseHandler):
    """
    :description: 晃一晃奖品列表
    """
    @filter_check_params("prize_id,key_id,machine_id")
    def get_async(self):
        """
        :description: 晃一晃奖品列表
        :param prize_id:奖品id
        :param key_id:key_id
        :param machine_id:机台id
        :param serial_no:serial_no
        :return list
        :last_editors: HuangJingCan
        """
        open_id = self.get_taobao_param().open_id
        app_id = self.get_taobao_param().source_app_id
        prize_id = int(self.get_param("prize_id", 0))
        key_id = int(self.get_param("key_id", 0))
        machine_id = int(self.get_param("machine_id", 0))
        serial_no = int(self.get_param("serial_no", 0))

        machine_info_model = MachineInfoModel()
        machine_info = machine_info_model.get_entity("id=%s and is_release=1", params=machine_id)
        if not machine_info:
            return self.reponse_json_error("NoMachine", "对不起，盒子不存在")
        incre_key = str(prize_id)
        if machine_info.is_repeat_prize == 1 and serial_no > 0:
            incre_key = str(prize_id) + "-" + str(serial_no)

        result_act_prize_list_dict = []

        redis_prizelist_key = "shakebox_tipsprizelist_" + str(open_id) + "_" + str(machine_id) + "_" + str(key_id)
        shakebox_tipsprizelist = self.redis_init().get(redis_prizelist_key)
        if shakebox_tipsprizelist != None:
            shakebox_tipsprizelist = self.json_loads(shakebox_tipsprizelist)
        else:
            shakebox_tipsprizelist = {}
        exclude_prize_list = shakebox_tipsprizelist[incre_key] if incre_key in shakebox_tipsprizelist.keys() else []

        act_prize_list_dict = ActPrizeModel().get_dict_list("machine_id=%s and is_release=1", order_by="tag_id desc,sort_index desc", params=[machine_id])
        for i in range(len(act_prize_list_dict)):

            exclude_prize_id = [prize_id for prize_id in exclude_prize_list if prize_id == act_prize_list_dict[i]["id"]]

            result_act_prize = {}
            result_act_prize["prize_id"] = act_prize_list_dict[i]["id"]
            result_act_prize["prize_name"] = act_prize_list_dict[i]["prize_name"]
            result_act_prize["prize_pic"] = act_prize_list_dict[i]["prize_pic"]
            result_act_prize["tag_id"] = act_prize_list_dict[i]["tag_id"]
            result_act_prize["is_exclude"] = True if exclude_prize_id else False
            result_act_prize_list_dict.append(result_act_prize)

        self.reponse_json_success(result_act_prize_list_dict)


class RecoverHandler(SevenBaseHandler):
    """
    :description: 回收预分配的奖品
    """
    @filter_check_params("machine_id,login_token,act_id,key_id")
    def get_async(self):
        """
        :description: 回收预分配的奖品
        :param login_token:登录令牌
        :param act_id:活动id
        :param machine_id:机台id
        :param key_id:key_id
        :param ver:版本
        :return reponse_json_success
        :last_editors: HuangJingCan
        """
        open_id = self.get_taobao_param().open_id
        app_id = self.get_taobao_param().source_app_id
        login_token = self.get_param("login_token")
        act_id = int(self.get_param("act_id", 0))
        machine_id = int(self.get_param("machine_id", 0))
        key_id = self.get_param("key_id")
        ver_no = self.get_param("ver")
        user_info_model = UserInfoModel()
        db_transaction = DbTransaction(db_config_dict=config.get_value("db_cloudapp"))
        act_prize_model = ActPrizeModel(db_transaction=db_transaction)
        surplus_queue_model = SurplusQueueModel(db_transaction=db_transaction)

        #请求太频繁限制
        if self.check_post(f"Recover_Post_{str(open_id)}_{str(machine_id)}_{str(key_id)}", 60) == False:
            return self.reponse_json_error("HintMessage", "对不起，请求太频繁")
        #删除小盒子历史产生的数据
        redis_num_key = "shakebox_tipsnumlist_" + str(open_id) + "_" + str(machine_id) + "_" + str(key_id)
        redis_prizelist_key = "shakebox_tipsprizelist_" + str(open_id) + "_" + str(machine_id) + "_" + str(key_id)
        self.redis_init().delete(redis_num_key)
        self.redis_init().delete(redis_prizelist_key)
        user_info = user_info_model.get_entity("act_id=%s and open_id=%s", params=[act_id, open_id])
        if not user_info:
            return self.reponse_json_error("NoUser", "对不起，用户不存在")
        if user_info.user_state == 1:
            return self.reponse_json_error("UserState", "对不起，你是黑名单用户")
        if user_info.login_token != login_token:
            return self.reponse_json_error("ErrorToken", "对不起，已在另一台设备登录,当前无法操作")
        surplus_queue_list = surplus_queue_model.get_list("act_id=%s and open_id=%s and machine_id=%s", params=[act_id, open_id, machine_id])
        if len(surplus_queue_list) > 0:
            for surplus_queue in surplus_queue_list:
                try:
                    db_transaction.begin_transaction()
                    if ver_no == "1.0.0":
                        act_prize_model.update_table("surplus=surplus+1", "id=%s", params=[surplus_queue.prize_id])
                    else:
                        act_prize_model.update_table("surplus=surplus+1", "id=%s and (surplus+1)<=prize_total", params=[surplus_queue.prize_id])
                    surplus_queue_model.del_entity("id=%s", params=[surplus_queue.id])
                    db_transaction.commit_transaction()
                except Exception as es:
                    db_transaction.rollback_transaction()
                    continue

        self.reponse_json_success()