# -*- coding: utf-8 -*-
import re
import unittest
from logio.rules import *
from logio import rules
from logio.logparser import expend_vars
from logio.logparser import get_default_rules

class TestLogParse(unittest.TestCase):

    def test01(self):
        """test year
        """
        for x in range(1900, 2999):
            year = str(x)
            assert re.match(YEAR, year).groupdict()["year"] == year

    def test02(self):
        """test month
        """
        for x in range(1, 13):
            month = "{:02d}".format(x)
            assert re.match(MONTH, month).groupdict()["month"] == month

    def test03(self):
        """test day
        """
        for x in range(1, 32):
            day = "{:02d}".format(x)
            assert re.match(DAY, day).groupdict()["day"] == day

    def test04(self):
        """test hour
        """
        for x in range(1, 25):
            hour = "{:02d}".format(x)
            assert re.match(HOUR, hour).groupdict()["hour"] == hour

    def test05(self):
        """test minute
        """
        for x in range(1, 61):
            minute = "{:02d}".format(x)
            assert re.match(MINUTE, minute).groupdict()["minute"] == minute

    def test06(self):
        """test second
        """
        for x in range(1, 61):
            second = "{:02d}".format(x)
            assert re.match(SECOND, second).groupdict()["second"] == second

    def test07(self):
        """test date_simple, e.g. 20190630
        """
        info = re.match(DATE_SIMPLE, "20190630").groupdict()
        assert info["year"] == "2019"
        assert info["month"] == "06"
        assert info["day"] == "30"
        assert info["date_simple"] == "20190630"

    def test08(self):
        """test DATE, e.g. 2019-06-30
        """
        info = re.match(DATE, "2019-06-30").groupdict()
        assert info["year"] == "2019"
        assert info["month"] == "06"
        assert info["day"] == "30"

    def test09(self):
        """test DATE_DMY, e.g. 03/Jun/2019
        """
        for month_short_name in "Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec".split("|"):
            info = re.match(DATE_DMY, "01/{month_short_name}/2019".format(month_short_name=month_short_name)).groupdict()
            assert info["year"] == "2019"
            assert info["month_short_name"] == month_short_name
            assert info["day"] == "01"

    def test10(self):
        """test TIME_SIMPLE, e.g. 200103
        """
        info = re.match(TIME_SIMPLE, "200103").groupdict()
        assert info["hour"] == "20"
        assert info["minute"] == "01"
        assert info["second"] == "03"
        assert info["time_simple"] == "200103"
    
    def test11(self):
        """test TIME, e.g. 20:01:03
        """
        info = re.match(TIME, "20:01:03").groupdict()
        assert info["hour"] == "20"
        assert info["minute"] == "01"
        assert info["second"] == "03"
        assert info["time"] == "20:01:03"
        
    def test12(self):
        """test DATETIME_SIMPLE, e.g. 20190630200501
        """
        info = re.match(DATETIME_SIMPLE, "20190630200501").groupdict()
        assert info["year"] == "2019"
        assert info["month"] == "06"
        assert info["day"] == "30"
        assert info["date_simple"] == "20190630"
        assert info["hour"] == "20"
        assert info["minute"] == "05"
        assert info["second"] == "01"
        assert info["time_simple"] == "200501"
        assert info["datetime_simple"] == "20190630200501"

    def test13(self):
        """test DATETIME, e.g. 2019-06-30 20:05:01
        """
        info = re.match(DATETIME, "2019-06-30 20:05:01").groupdict()
        assert info["year"] == "2019"
        assert info["month"] == "06"
        assert info["day"] == "30"
        assert info["date"] == "2019-06-30"
        assert info["hour"] == "20"
        assert info["minute"] == "05"
        assert info["second"] == "01"
        assert info["time"] == "20:05:01"
        assert info["datetime"] == "2019-06-30 20:05:01"
     
    def test14(self):
        """test TIMEZONE, e.g. +0800
        """
        info = re.match(TIMEZONE, "+0800").groupdict()
        assert info["timezone"] == "+0800"

    def test15(self):
        """test TIMEZONE_ISO, e.g. +08:06
        """
        info = re.match(TIMEZONE, "+08:06").groupdict()
        assert info["timezone"] == "+08:06"

    def test16(self):
        """test QUOTED_VALUE, e.g. 
        """
        for value in [
                "abc",
                "hello world",
                "http://a.com",
                '''"es-ES,es;q=0.8"''',
                '''"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11"''',
                "it\\\"s not ok",
                ]:
            info = re.match(QUOTED_VALUE, value).group()
            assert info == value

    def test17(self):
        """test NAME_VALUE, e.g. filename
        """
        for name in ["filename", "op"]:
            info = re.match(NAME_VALUE, name).group()
            assert info == name
    
    def test19(self):
        """test OPTION
        """
        for option in [
                "a=123",
                "a=hello world",
                '''a="hello world"''',
                '''a="it\\\"s not ok"''',
                ]:
            info = re.match(OPTION, option).group()
            assert info == option

    def test20(self):
        """test IPV4
        """
        for ip in ["127.0.0.1", "10.0.0.1", "114.114.114.114", "172.16.0.1", "192.168.0.1"]:
            info = re.match(IPV4, ip).group()
            assert info == ip

    def test21(self):
        """test access time, e.g. [03/Jan/2013:21:17:20 -0600]
        """
        for time in ["[03/Jan/2013:21:17:20 -0600]"]:
            info = re.match(ISO_FORMAT_TIME_VALUE, time).group()
            assert info == time

    def test22(self):
        """test access time, e.g. [03/Jan/2013:21:17:20 -0600]
        """
        info = re.match(ISO_FORMAT_TIME, "[03/Jan/2013:21:17:20 -0600]").groupdict()
        assert info["year"] == "2013"
        assert info["month_short_name"] == "Jan"
        assert info["day"] == "03"
        assert info["hour"] == "21"
        assert info["minute"] == "17"
        assert info["second"] == "20"
        assert info["timezone"] == "-0600"
        assert info["datetime"] == "03/Jan/2013:21:17:20 -0600"

    def test23(self):
        """test IPV4_SERVICE
        """
        info = re.match(IPV4_SERVICE, "127.0.0.1:9000").group()
        assert info == "127.0.0.1:9000"
    
    def test30(self):
        """test expend_vars
        """
        rules = {
            "YEAR": YEAR,
            "MONTH": MONTH,
            "DAY": DAY,
            "HOUR": HOUR,
            "MINUTE": MINUTE,
            "SECOND": SECOND,
            "DATE_SIMPLE": "(?P<date_simple>{YEAR}{MONTH}{DAY})",
            "TIME_SIMPLE": "(?P<time_simple>{HOUR}{MINUTE}{SECOND})",
            "DATETIME_SIMPLE": "(?P<datetime>{DATE_SIMPLE}{TIME_SIMPLE})",
        }
        new_rules = expend_vars(rules)
        assert not "YEAR" in new_rules["DATE_SIMPLE"]
        assert not "MONTH" in new_rules["DATE_SIMPLE"]
        assert not "DAY" in new_rules["DATE_SIMPLE"]
        assert not "HOUR" in new_rules["TIME_SIMPLE"]
        assert not "MINUTE" in new_rules["TIME_SIMPLE"]
        assert not "SECOND" in new_rules["TIME_SIMPLE"]
        assert not "DATE_SIMPLE" in new_rules["DATETIME_SIMPLE"]
        assert not "TIME_SIMPLE" in new_rules["DATETIME_SIMPLE"]

    def test31(self):
        rules = get_default_rules()
        assert rules

    def test32(self):
        text = "[03/Jul/2019:14:41:43.570635527 +0800] conn=16959994 op=1 RESULT err=0 tag=101 nentries=1 etime=0.0001746563"
        rules = get_default_rules()
        rules.update({"RESULT": "({ISO_FORMAT_TIME_WITH_MICROSECOND} conn=(?P<conn>\\d+) op=(?P<op>\\d+).*)"})
        rules = expend_vars(rules)
        print(rules["RESULT"])
        match = re.match(rules["RESULT"], text)
        print(match)
        assert match

    def test33(self):
        for name in dir(rules):
            if not name.startswith("_"):
                pattern = getattr(rules, name)
                assert re.compile(pattern)

if __name__ == "__main__":
    unittest.main()