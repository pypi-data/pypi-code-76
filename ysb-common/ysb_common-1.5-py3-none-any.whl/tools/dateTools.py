import time
import datetime


class DateTools:

    @staticmethod
    def get_today(type1=None):
        """
        获取当前时间：返回不同的格式
        :param: type:
        1返回年，2返回月，3返回日。None返回年月日yyyy-mm-dd
        :return:
        """
        if type1 is None:
            today_str = str(time.strftime('%Y-%m-%d', time.localtime(time.time())))
        else:
            type2 = str(type1)
            cur = datetime.datetime.now()
            if type2 == '1':
                today_str = str(cur.year)
            elif type2 == '2':
                yf = str(cur.month)
                if int(yf) < 10:
                    today_str = "0" + yf
                else:
                    today_str = yf
            elif type2 == '3':
                today_str = cur.day

        return str(today_str)
