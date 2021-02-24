# coding:utf-8
import datetime as dt
from bs4 import BeautifulSoup

from src.browser import Browser
from src.utils.color import Color


class AttendanceManager(object):

    def __init__(self, headless=True):
        self.headless = headless
        self.browser = Browser(headless=headless)
        self.driver = self.browser.driver

    def confirm(self, method):
        if self.open() and method in dir(self):
            getattr(self, method)()
            self.exit()

    def open(self):
        return self.browser.open_attendance()

    def history(self):
        timetable = self.get_attendance_timetable(dt.datetime.now().day)
        self.print_timetable(timetable)

    def print_timetable(self, timetable):
        texts = [
            Color.get_colored(Color.BOLD, '出勤:     ')
            + ', '.join(timetable[0]),
            Color.get_colored(Color.BOLD, '退勤:     ')
            + ', '.join(timetable[1]),
            Color.get_colored(Color.BOLD, '休憩開始: ')
            + ', '.join(timetable[2]),
            Color.get_colored(Color.BOLD, '休憩終了: ')
            + ', '.join(timetable[3])
        ]
        print('================================')
        for text in texts:
            print(text)
        print('================================')

    def get_attendance_timetable(self, day) -> list:
        timetable = self.get_attendance(day)
        for i, t in enumerate(timetable):
            timetable[i] = [t for t in t.strings]

        return timetable

    def get_attendance(self, day) -> list:
        html = self.driver.page_source.encode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        attendances = soup.find_all('td', class_='column-attendance')

        attendance_array = []
        time = 0
        while time < len(attendances):
            attendance_array.append(attendances[time:time+4])
            time += 4

        return attendance_array[day-1]

    def exit(self):
        self.driver.close()
