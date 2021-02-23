import datetime
import calendar


class DateToolsCls:
    """
    #日期时间获取类
    """
    # 1. 获取「今天」  2021-01-07
    today = datetime.date.today()
    # 2. 获取当前月的第一天
    first_day = today.replace(day=1)
    # 3. 减一天，得到上个月的最后一天
    last_month_last_day = first_day - datetime.timedelta(days=1)
    last_month_first_day = last_month_last_day.replace(day=1)

    @staticmethod
    def get_last_month_first_day():
        """
        获取上个月的第一天
        :return:
        """
        return str(DateToolsCls.last_month_first_day)

    @staticmethod
    def get_last_month_last_day():
        """
        获取上个月的最后一天
        :return:
        """
        return str(DateToolsCls.last_month_last_day)

    @staticmethod
    def get_this_month_first_day():
        """
        获取本月第一天
        :return:
        """
        return str(DateToolsCls.first_day)

    @staticmethod
    def get_this_month_last_day():
        """
        获取本月最后一天
        :return:
        """
        last_day = datetime.date.today().replace(day=calendar.monthrange(datetime.date.today().year, datetime.date.today().month)[1])
        return str(last_day)
