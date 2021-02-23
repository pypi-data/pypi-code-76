import requests
import traceback
import time
from ...api.raw import *
from .raw_data_helper import RawDataHelper
from ...view.raw_models import OSFundNav
from ...api.raw import RawDataApi
class OverseaDataUpdate:

    def __init__(self, update_period:int=35, data_per_page:int=20):
        self.update_period = update_period
        self.data_per_page = data_per_page
        self.data_helper = RawDataHelper()
        self.raw_data_api = RawDataApi()
        self.today = datetime.datetime.now().date()

    def update_fund_nav(self):
        try:
            nav_dic = {
                'navDate':'datetime',
                'price':'nav',
            }
            fund_info = self.raw_data_api.get_over_sea_fund_info()
            fund_id_list = fund_info.codes.tolist()
            update_period_dates = self.today - datetime.timedelta(days=self.update_period)
            exsited_price = self.raw_data_api.get_oversea_fund_nav(start_date = update_period_dates).drop(columns=['_update_time'], errors='ignore')

            result = []
            for fund_id in fund_id_list:
                url = 'https://fund.bluestonehk.com/fund/ifast/info/getHistoryNavs?productId={}&pageSize={}&pageNo={}'.format(
                    fund_id, self.data_per_page, 1
                )
                response = requests.get(url)
                datas = response.json()
                if datas['message'] != '请求成功' or datas['body']['data'] == []:
                    continue
                new_nav = pd.DataFrame(datas['body']['data'])[nav_dic.keys()].rename(columns=nav_dic)
                td = pd.to_datetime(new_nav.datetime)
                td = [_.date() for _ in td]
                new_nav.datetime = td
                exsited_date = exsited_price[exsited_price['codes'] == fund_id].datetime.max()
                new_df = new_nav[new_nav.datetime > exsited_date].copy()
                if new_df.empty:
                    idx = fund_id_list.index(fund_id)
                    if idx % 20 == 0:
                        time.sleep(0.1)
                        print(f'finish fund nav {idx}')
                    continue
                new_df.loc[:,'codes'] = fund_id
                result.append(new_df)
                idx = fund_id_list.index(fund_id)
                if idx % 20 == 0:
                    time.sleep(0.1)
                    print(f'finish fund nav {idx}')

            nav_result = pd.concat(result)
            self.data_helper._upload_raw(nav_result, OSFundNav.__table__.name)
            return True

        except Exception as e:
            print(e)
            traceback.print_exc()
            return False
    