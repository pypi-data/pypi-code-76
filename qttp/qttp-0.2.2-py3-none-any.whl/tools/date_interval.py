from datetime import datetime, timedelta

class DateInterval:
    def __init__(self, start, end, count_limit):
        self.start = start
        self.end = end
        self.count_limit = count_limit

    def __getitem__(self, ind):
        new_start_date, new_end_date = self.__hour_date()
        return new_start_date, new_end_date

    def __hour_date(self):
        s, e = self.__date_to_datetime()

        start_date = datetime(s[0], s[1], s[2])
        end_date = datetime(e[0], e[1], e[2])

        end = start_date + timedelta(hours=self.count_limit)
        date_list = [start_date, end]
        while True:
            end = end + timedelta(hours=self.count_limit)

            if end_date > end:
                date_list.append(end)

            if end_date < end:
                date_list.append(end_date)
                break

        new_start_date = list(map(self.__date_to_string, date_list))[:-1]
        new_end_date = list(map(self.__date_to_string, date_list))[1:]
        return new_start_date, new_end_date

    def __date_to_datetime(self):
        start = list(map(int, self.start.split("-")))
        end = list(map(int, self.end.split("-")))
        return start, end

    def __date_to_string(self, date):
        date = date.strftime('%Y-%m-%d %H:%M:%S')
        return date
