# -*- coding: utf-8 -*-
"""
:Author: HuangJingCan
:Date: 2020-05-12 20:04:54
:LastEditTime: 2021-02-24 16:00:09
:LastEditors: HuangJingCan
:description: 用户相关
"""
from seven_cloudapp.handlers.seven_base import *
from seven_cloudapp.libs.customize.seven import *

from seven_cloudapp.models.db_models.user.user_info_model import *
from seven_cloudapp.models.db_models.gear.gear_value_model import *
from seven_cloudapp.models.db_models.gear.gear_log_model import *
from seven_cloudapp.models.db_models.price.price_gear_model import *
from seven_cloudapp.models.db_models.coin.coin_order_model import *
from seven_cloudapp.models.db_models.machine.machine_value_model import *
from seven_cloudapp.models.enum import OperationType, SourceType
from seven_cloudapp.models.seven_model import *

from seven_cloudapp.handlers.server.user_s import LoginHandler
from seven_cloudapp.handlers.server.user_s import UserStatusHandler

from seven_cloudapp_ppmt.models.db_models.machine.machine_info_model import *


class UserListHandler(SevenBaseHandler):
    """
    :description: 用户列表
    """
    @filter_check_params("act_id")
    def get_async(self):
        """
        :description: 用户列表
        :param page_index：页索引
        :param page_size：页大小
        :param act_id：活动id
        :param user_nick：用户昵称
        :return PageInfo
        :last_editors: HuangJingCan
        """
        page_index = int(self.get_param("page_index", 0))
        page_size = int(self.get_param("page_size", 20))
        act_id = int(self.get_param("act_id", 0))
        user_nick = self.get_param("nick_name")

        condition = "act_id=%s"
        params = [act_id]
        if user_nick:
            condition += " AND user_nick=%s"
            params.append(user_nick)

        page_list, total = UserInfoModel().get_dict_page_list("id,act_id,open_id,user_nick,pay_price,user_state", page_index, page_size, condition, order_by="id desc", params=params)

        if page_list:
            where_machine_value = SevenHelper.get_condition_by_id_list("open_id", [i["open_id"] for i in page_list])
            where_gear_value = SevenHelper.get_condition_by_id_list("open_id", [i["open_id"] for i in page_list])
            price_gear_list = PriceGearModel().get_list("act_id=%s and is_del=1", params=[act_id])
            if price_gear_list:
                id_list_str = str([i.id for i in price_gear_list]).strip('[').strip(']')
                where_gear_value += f" and price_gears_id NOT IN({id_list_str})"
            dict_machine_value_list = MachineValueModel().get_dict_list(f"act_id={act_id} AND {where_machine_value}", "open_id", field="open_id,sum(open_value) as open_value")
            dict_gear_value_list = GearValueModel().get_dict_list(f"act_id={act_id} AND {where_gear_value}", "open_id", field="open_id,sum(current_value) as current_value")
            for i in range(0, len(dict_machine_value_list)):
                dict_machine_value_list[i]["open_value"] = int(dict_machine_value_list[i]["open_value"])
            for i in range(0, len(dict_gear_value_list)):
                dict_gear_value_list[i]["current_value"] = int(dict_gear_value_list[i]["current_value"]) if dict_gear_value_list[i]["current_value"] else 0
            new_dict_list = SevenHelper.merge_dict_list(page_list, "open_id", dict_machine_value_list, "open_id", "open_value")
            new_dict_list = SevenHelper.merge_dict_list(new_dict_list, "open_id", dict_gear_value_list, "open_id", "current_value")
            page_info = PageInfo(page_index, page_size, total, new_dict_list)

            self.reponse_json_success(page_info)
        else:
            self.reponse_json_success(PageInfo(page_index, page_size, total, page_list))


class UserMachineListHandler(SevenBaseHandler):
    """
    :description: 用户机台数据列表
    """
    @filter_check_params("act_id")
    def get_async(self):
        """
        :description: 用户机台数据列表
        :param act_id:活动id
        :param user_open_id:user_open_id
        :return: list
        :last_editors: HuangJingCan
        """
        act_id = int(self.get_param("act_id", 0))
        user_open_id = self.get_param("user_open_id")
        condition = "act_id=%s and open_id=%s"
        new_dict_list = []
        dict_machine_Info_list = MachineInfoModel().get_dict_list("act_id=%s and is_release=1", field="id,machine_name", params=act_id)
        dict_machine_value_list = MachineValueModel().get_dict_list(condition, params=[act_id, user_open_id])
        if len(dict_machine_Info_list) > 0:
            new_dict_list = SevenHelper.merge_dict_list(dict_machine_Info_list, "id", dict_machine_value_list, "machine_id", "open_value")
            return self.reponse_json_success(new_dict_list)

        self.reponse_json_success(new_dict_list)


class GearValueHandler(SevenBaseHandler):
    """
    :description: 设置开盒次数
    """
    @filter_check_params("user_open_id,act_id")
    def post_async(self):
        """
        :description: 设置开盒次数
        :param user_open_id：用户唯一标识
        :param set_content_list：档位设置集合
        :return: reponse_json_success
        :last_editors: HuangJianYi
        """
        user_open_id = self.get_param("user_open_id")
        set_content_list = self.get_param("set_content_list")
        act_id = int(self.get_param("act_id", "0"))
        app_id = self.get_param("app_id")
        modify_date = self.get_now_datetime()

        user_info_model = UserInfoModel()
        user_info = user_info_model.get_entity("open_id=%s and act_id=%s", params=[user_open_id, act_id])
        if not user_info:
            return self.reponse_json_error("NoUser", "对不起，找不到该用户")

        gear_value_model = GearValueModel()

        if act_id <= 0:
            return self.reponse_json_error_params()

        set_content_list = self.json_loads(set_content_list)

        for set_content in set_content_list:
            price_gears_id = set_content["price_gears_id"]
            current_value = set_content["current_value"]

            result = False
            history_value = 0
            gear_value = gear_value_model.get_entity("act_id=%s AND open_id=%s AND price_gears_id=%s", params=[act_id, user_open_id, price_gears_id])
            if gear_value:
                history_value = gear_value.current_value
                if history_value != current_value:
                    result = gear_value_model.update_table("current_value=%s,modify_date=%s", "act_id=%s AND open_id=%s AND price_gears_id=%s", [current_value, modify_date, act_id, user_open_id, price_gears_id])
            else:
                gear_value = GearValue()
                gear_value.act_id = act_id
                gear_value.app_id = app_id
                gear_value.open_id = user_open_id
                gear_value.price_gears_id = price_gears_id
                gear_value.open_value = 0
                gear_value.current_value = current_value
                gear_value.modify_date = modify_date
                gear_value.create_date = modify_date
                result = gear_value_model.add_entity(gear_value)
                if result > 0:
                    result = True

            if result:
                gear_log = GearLog()
                gear_log.app_id = app_id
                gear_log.act_id = act_id
                gear_log.open_id = user_open_id
                gear_log.price_gears_id = price_gears_id
                gear_log.type_value = SourceType.手动配置.value
                gear_log.current_value = current_value - history_value
                gear_log.history_value = history_value
                gear_log.create_date = modify_date
                GearLogModel().add_entity(gear_log)

                #添加商家对帐记录
                coin_order_model = CoinOrderModel()
                if (current_value - history_value) > 0:
                    coin_order = CoinOrder()
                    coin_order.open_id = user_open_id
                    coin_order.app_id = app_id
                    coin_order.act_id = act_id
                    coin_order.price_gears_id = price_gears_id
                    coin_order.reward_type = 0
                    coin_order.nick_name = user_info.user_nick
                    coin_order.buy_count = current_value - history_value
                    coin_order.surplus_count = current_value - history_value
                    coin_order.create_date = self.get_now_datetime()
                    coin_order.modify_date = self.get_now_datetime()
                    coin_order_model.add_entity(coin_order)
                else:
                    del_count = history_value - current_value
                    update_coin_order_list = []
                    coin_order_set_list = coin_order_model.get_list("act_id=%s and open_id=%s and surplus_count>0 and price_gears_id=%s and pay_order_id=0", "id asc", params=[act_id, user_open_id, price_gears_id])

                    if len(coin_order_set_list) > 0:
                        for coin_order in coin_order_set_list:
                            if coin_order.surplus_count > del_count:
                                coin_order.surplus_count = coin_order.surplus_count - del_count
                                del_count = 0
                            else:
                                del_count = del_count - coin_order.surplus_count
                                coin_order.surplus_count = 0
                            update_coin_order_list.append(coin_order)
                            if del_count == 0:
                                break
                    if del_count > 0:
                        coin_order_pay_list = coin_order_model.get_list("act_id=%s and open_id=%s and surplus_count>0 and price_gears_id=%s and pay_order_id>0", "id asc", params=[act_id, user_open_id, price_gears_id])
                        if len(coin_order_pay_list) > 0:
                            for coin_order in coin_order_pay_list:
                                if coin_order.surplus_count > del_count:
                                    coin_order.surplus_count = coin_order.surplus_count - del_count
                                    del_count = 0
                                else:
                                    del_count = del_count - coin_order.surplus_count
                                    coin_order.surplus_count = 0
                                update_coin_order_list.append(coin_order)
                                if del_count == 0:
                                    break
                    for coin_order in update_coin_order_list:
                        coin_order_model.update_entity(coin_order)

        self.reponse_json_success()


class GearLogHandler(SevenBaseHandler):
    """
    :description: 用户档位配置记录
    """
    def get_async(self):
        """
        :description: 用户档位配置记录
        :param act_id:活动id
        :param user_open_id:user_open_id
        :return list
        :last_editors: HuangJianYi
        """
        act_id = int(self.get_param("act_id", 0))
        user_open_id = self.get_param("user_open_id")
        price_gear_model = PriceGearModel()
        gear_value_model = GearValueModel()
        gear_log_model = GearLogModel()

        price_gear_list = price_gear_model.get_list("act_id=%s and is_del=0", params=act_id)
        gear_value_list = gear_value_model.get_list("act_id=%s and open_id=%s", params=[act_id, user_open_id])
        gear_log_list_dict = gear_log_model.get_dict_list("act_id=%s and open_id=%s", order_by='create_date desc', params=[act_id, user_open_id])

        gear_log_groups = []
        for price_gear in price_gear_list:
            gear_log_group = {}
            gear_log_group["gear_value_id"] = price_gear.id
            gear_log_group["gear_value_price"] = price_gear.price
            for gear_value in gear_value_list:
                if gear_value.price_gears_id == price_gear.id:
                    gear_log_group["surplus_value"] = gear_value.current_value
                    continue
            if "surplus_value" not in gear_log_group.keys():
                gear_log_group["surplus_value"] = 0
            gear_log_group["gear_log_list"] = [i for i in gear_log_list_dict if i["price_gears_id"] == price_gear.id]
            gear_log_groups.append(gear_log_group)

        self.reponse_json_success(gear_log_groups)