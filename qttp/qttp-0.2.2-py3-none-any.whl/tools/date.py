from datetime import datetime, timedelta

class HunDate:
    def __init__(self):
        self.now = datetime.now()

    def today(self):
        date = self.now.strftime('%Y-%m-%d')
        return date

    def today_plus_1day(self):
        date = self.now + timedelta(days=1)
        date = date.strftime('%Y-%m-%d')
        return date

    def time_detail(self):
        date_time = self.now.strftime('%Y-%m-%d %H:%M:%S')
        return date_time

    def today_minus_day(self, day):
        minus_day = self.now - timedelta(days=day)
        minus_day = minus_day.strftime('%Y-%m-%d')
        return minus_day

    def date_minus_day(self, date, day):
        date = self.__get_date_for_timestamp(date)
        minus_date = date - timedelta(days=day)
        minus_date = minus_date.strftime('%Y-%m-%d')
        return minus_date

    def date_plus_day(self, date, day):
        date = self.__get_date_for_timestamp(date)
        plus_date = date + timedelta(days=day)
        plus_date = plus_date.strftime('%Y-%m-%d')
        return plus_date


    def minus_hour(self, hour):
        minus_hour = self.now - timedelta(hours=hour)
        minus_hour = minus_hour.strftime('%Y-%m-%d %H:00:00')
        return minus_hour

    def now_millisecond(self, days=0):
        t = self.now - timedelta(days=days)
        return int(t.timestamp()*1000)

    def millisecond(self, date):
        date = self.__get_date_for_timestamp(date)
        return int(date.timestamp()*1000)

    def seconds(self, date):
        date = self.__get_date_for_timestamp(date)
        return int(date.timestamp())

    def __get_date_for_timestamp(self, date):
        try:
            date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

        except:
            date = date + " 00:00:00"
            date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

        return date
