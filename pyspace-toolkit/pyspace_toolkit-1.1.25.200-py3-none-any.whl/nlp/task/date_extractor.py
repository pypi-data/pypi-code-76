import datetime
import dateutil
import pytz
import copy
import os
import re

class DateHelpers:
    month_day_count_list = ['###', 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    month_text_list = ['###', 'ocak', 'subat', 'mart', 'nisan', 'mayis', 'haziran', 'temmuz', 'agustos', 'eylul', 'ekim', 'kasim', 'aralik']
    text_digit_1_list = ['###', 'bir', 'iki', 'uc', 'dort', 'bes', 'alti', 'yedi', 'sekiz', 'dokuz']
    text_digit_2_list = ['###', 'on', 'yirmi', 'otuz', 'kirk', 'elli', 'altmis', 'yetmis', 'seksen', 'doksan']
 
    #############################################################################
    
    def get_latest_history_year(d, m):
        today = datetime.datetime.now(tz=pytz.timezone("Europe/Istanbul"))
        if today.month < m or (today.month == m and today.day < d):
            return today.year - 1
        else:
            return today.year
    
    def get_latest_year_after_given_date(d1, m1, y1, d2, m2):
        
        if m1 < m2 or (m1 == m2 and d1 < d2):
            return y1
        else:
            return y1 + 1
        
    def get_last_day_of_month_year(m, y):
        
        result = DateHelpers.month_day_count_list[m]
        if m == 2 and y % 4 == 0:
            result += 1
        return result
        
    def fill_dates(dates):
        dates = copy.deepcopy(dates)
        
        DAY = 0
        MONTH = 1
        YEAR = 2
        EMPTY = -1
        
        if len(dates) == 1:
            # 2017
            # ocak 2017
            # 15 ocak
            # ocak
            
            if dates[0][DAY] == EMPTY: 
                dates[0][DAY] = 1
                
            if dates[0][MONTH] == EMPTY: 
                dates[0][MONTH] = 1
            
            if dates[0][YEAR] == EMPTY:
                dates[0][YEAR] = DateHelpers.get_latest_history_year(dates[0][DAY], dates[0][MONTH])
            
            return dates
        elif len(dates) == 2:
            # 2017 2018 arasinda # Y1, Y2
            # 2017 ocak 2018 subat # Y1 M1 Y2 M2
            
            # ayin 15 i ile 20'si arasi # D1 D2
            # ayin 15 ile 20si arasi # D1 D2
            
            # ocak mart # M1 M2
            # kasimdan ocaga kadar # M1 M2

            # 15 mayistan agustosa kadar # D1 M1 M2
            # hazirandan 15 eylule kadar # M1 D2 M2
            DATE1 = dates[0]
            DATE2 = dates[1]
            
            bD1 = DATE1[DAY] != EMPTY
            bM1 = DATE1[MONTH] != EMPTY
            bY1 = DATE1[YEAR] != EMPTY
            bD2 = DATE2[DAY] != EMPTY
            bM2 = DATE2[MONTH] != EMPTY
            bY2 = DATE2[YEAR] != EMPTY
            
            if not bD1:
                DATE1[DAY] = 1
            if not bD2:
                DATE2[DAY] = 32
            if not bM1:
                DATE1[MONTH] = 1
            if not bM2:
                DATE2[MONTH] = 12
            if not bY1:
                DATE1[YEAR] = DateHelpers.get_latest_history_year(DATE1[DAY], DATE1[MONTH])
            if not bY2:
                DATE2[YEAR] = DateHelpers.get_latest_year_after_given_date(DATE1[DAY], DATE1[MONTH], DATE1[YEAR], DATE2[DAY], DATE2[MONTH],)
                
            if DATE2[DAY] == 32:
                DATE2[DAY] = DateHelpers.get_last_day_of_month_year(DATE2[MONTH], DATE2[YEAR])
                
            return dates
        else:
            # can not work on more than 2 dates
            return dates
 
    #############################################################################
    
    def substract_date(date, duration):
        
        date = copy.deepcopy(date)
        
        if duration[0] != 0: 
            
            if date[0] <= duration[0]: # substract 10 days from 5 days
                if date[1] <= 1:
                    date[2] = date[2] - 1
                    date[1] = date[1] + 12

                date[1] = date[1] - 1

                prev_month_day_count = DateHelpers.get_last_day_of_month_year(date[1], date[2])
                date[0] = date[0] + prev_month_day_count
            
            date[0] = date[0] - duration[0]
            
        if duration[1] != 0:
            
            if date[1] <= duration[1]:
                date[2] = date[2] - 1
                date[1] = date[1] + 12
                
            date[1] = date[1] - duration[1]
            date[0] = min(date[0], DateHelpers.get_last_day_of_month_year(date[1], date[2]))
            
        if duration[2] != 0:
            
            date[2] = date[2] - duration[2]
        
        return date
    
    def add_date(date, duration):

        _start = datetime.datetime(date[2],date[1],date[0])
        _duration = dateutil.relativedelta.relativedelta(years=duration[2], months=duration[1], days=duration[0])
        
        _end = _start + _duration
        return [_end.day, _end.month, _end.year]

    #############################################################################
    
    def year_fix(y):
        return int(y)
    
    def month_fix(m):
        if m in DateHelpers.month_text_list:
            return DateHelpers.month_text_list.index(m)
        else:
            return int(m)
    
    def day_fix(d):
        try:
            return int(d)
        except:
            temp = 0
            if d[:2] == 'on':
                temp += 10
                d = d[2:].strip()
            elif d[:5] == 'yirmi':
                temp += 20
                d = d[5:].strip()
            elif d[:4] == 'otuz':
                temp += 30
                d = d[4:].strip()
            
            if d in DateHelpers.text_digit_1_list:
                temp += DateHelpers.text_digit_1_list.index(d)
            
            d = temp
            return d

class DateParser:
    
    def __init__(self, duckling_base_url=None):
        from pyspace.requests.api import DucklingAPI
        self.duckling_base_url = duckling_base_url
        self.duckling = DucklingAPI(url=self.get_duckling_url())
        # self.today = self.get_today()
        
    def get_duckling_url(self):
        
        if os.getenv('SOFIE_DUCKLING_URL'):
            duckling_url = os.environ["SOFIE_DUCKLING_URL"]
        elif os.environ.get("RASA_DUCKLING_HTTP_URL"):
            duckling_url =  os.environ["RASA_DUCKLING_HTTP_URL"]
        else:
            duckling_url = self.duckling_base_url

        if duckling_url[:7] != 'http://' and duckling_url[:8] != 'https://':
            duckling_url = 'http://' + duckling_url
        if duckling_url[-6:] != '/parse':
            if duckling_url[-1] == '/':
                duckling_url += 'parse'
            else:
                duckling_url += '/parse'

        return duckling_url
    
    def get_today(self,):
        
        today = self.duckling.query('bugun')
        today = [d for d in today if d['dim'] == 'time']
        today = today[0]
        today = today['value']['value']
        today = [int(today[8:10]),int(today[5:7]),int(today[:4])]
        
        return today
    
    def parse_date__exact(self, text):

        year_digit = r'(20[012]\d)'
        year = fr'{year_digit}'

        month_digit = r'([01]?\d)'
        month_text = r'(ocak|subat|mart|nisan|mayis|haziran|temmuz|agustos|eylul|ekim|kasim|aralik)'
        month = fr'({month_digit}|{month_text})'

        text_digit_1 = r'(bir|iki|uc|dort|bes|alti|yedi|sekiz|dokuz)'
        text_digit_2 = r'(on|yirmi)'
        text_digit_3 = r'(otuz|otuz\s?bir)'
        day_text = fr'(({text_digit_2}\s*)*{text_digit_1}|{text_digit_2}|{text_digit_3})'
        day_digit = r'([0123]?\d)'
        day = fr'({day_digit}|{day_text})'

        dlm_punct = r'[\-\.\/]'
        dlm_space = r'\s'
        dlm = fr'({dlm_punct}|{dlm_space})'

        start = fr'(?<![a-zA-Z0-9])' # [\s\^]
        end = fr'(?![0-9])' # [\s\$]
        #########################################################################

        fill_dates = DateHelpers.fill_dates
        year_fix = DateHelpers.year_fix
        month_fix = DateHelpers.month_fix
        day_fix = DateHelpers.day_fix

        #########################################################################

        rd1 = fr'{start}{month}{dlm}{year}{dlm}{month}{dlm}{year}{end}'
        rd2 = fr'{start}{year}{dlm}{month}{dlm}{year}{dlm}{month}{end}'
        rd3 = fr'{start}{day}{dlm}{month}{dlm}{day}{dlm}{month}{end}'
        rd4 = fr'{start}{month}{dlm}{day}{dlm}{month}{dlm}{day}{end}'

        rdc1 = fr'{start}{start}{year}{dlm}{month_text}{dlm}{month_text}{end}'
        rdc2 = fr'{start}{month_text}{dlm}{month_text}{dlm}{year}{end}'
        rdc3 = fr'{start}{month}{dlm}{day}{dlm}{day}{end}'
        rdc4 = fr'{start}{day}{dlm}{day}{dlm}{month}{end}'

        r1 = fr'{start}{day}{dlm}{month}{dlm}{year}{end}'
        r2 = fr'{start}{day_digit}{dlm_punct}{month_digit}{end}'
        r3 = fr'{start}{day}{dlm}*{month_text}{end}'
        r4 = fr'{start}{year}{dlm}*{month_text}{end}'
        r5 = fr'{start}{month_text}{dlm}*{year}{end}'
        r6 = fr'{start}({month_text}){end}'
        r7 = fr'{start}({year}){end}'

        extraction_regexes = [
            (rd1, ((-1,0,4),(-1,6,10))),
            (rd2, ((-1,2,0),(-1,8,6))),
            (rd3, ((0,9,-1),(13,22,-1))),
            (rd4, ((4,0,-1),(17,13,-1))),

            (rdc1, ((-1,2,0),(-1,4,0))),
            (rdc2, ((-1,0,4),(-1,2,4))),
            (rdc3, ((4,0,-1),(13,0,-1))),
            (rdc4, ((0,18,-1),(9,18,-1))),

            (r1, ((0,9,13),)),
            (r2, ((0,1,-1),)),
            (r3, ((0,9,-1),)),
            (r4, ((-1,2,0),)),
            (r5, ((-1,0,2),)),
            (r6, ((-1,0,-1),)),
            (r7, ((-1,-1,0),)),
        ]

        output = {'exact':[]}
        for rX, gX in extraction_regexes:
            matches = re.findall(rX, text)
            if matches:
                # print(matches)
                temp = []
                for m in matches:
                    for g in gX:
                        _d = day_fix(m[g[0]])    if g[0]!=-1 else -1
                        _m = month_fix(m[g[1]])  if g[1]!=-1 else -1
                        _y = year_fix(m[g[2]])   if g[2]!=-1 else -1
                        temp.append([_d, _m,_y])
                output['exact'].extend(temp)
                text = re.sub(rX,'',text).strip()

        output['exact_filled'] = fill_dates(output['exact'])

        # print(text)

        return output

    def parse_date__duration(self, text):

        start = fr'(?<![a-zA-Z0-9])' # [\s\^]
        end = fr'(?![0-9])' # [\s\$]

        unit = r'\b(gun|ay|yil|sene)'

        text_digit_1 = r'(bir|iki|uc|dort|bes|alti|yedi|sekiz|dokuz)'
        text_digit_2 = r'(on|yirmi|otuz|kirk|elli|altmis|yetmis|seksen|doksan)'

        count_text = fr'(({text_digit_2}\s*){{0,1}}{text_digit_1}{{0,1}})'
        count_digit = r'(\d{1,2})'
        count = fr'({count_digit}|{count_text})'

        duration = fr'{start}{count}\s*{unit}'
        matches = re.findall(duration, text)

        output = {'durations':[]}

        temp = []
        for m in matches:

            temp_count = 0
            temp_count += int(m[1]) if m[1] != '' else 0
            temp_count += 10*DateHelpers.text_digit_2_list.index(m[4]) if m[4] != '' else 0
            temp_count += 1*DateHelpers.text_digit_1_list.index(m[5]) if m[5] != '' else 0
            temp_count += 1 if temp_count==0 else 0

            if m[6] == 'gun':
                temp.append([temp_count,0,0])
            elif m[6] == 'ay':
                temp.append([0,temp_count,0])
            elif m[6] in ['yil', 'sene']:
                temp.append([0,0,temp_count])

        output['durations'].extend(temp)

        # print(matches)
        return output

    def parse_date__phrase(self, text):

        text_date_regex_1 = r'\b(dun|bugun|yarin|hafta(sonu)*)' # haftasonu
        text_date_regex_2 = r'\b(yaz|kis|bahar|sonbahar|ilkbahar)'
        text_date_regex = fr'({text_date_regex_1}|{text_date_regex_2})'

        matches = re.findall(text_date_regex, text)

        output = {'phrase':[]}

        temp = []
        for m in matches:
            temp.append(m[0])
        #    output['text'] = [m[0] for m in matches] if isinstance(output['text'][0], tuple) else output['text']
        # text = re.sub(text_date_regex,'',text).strip()
        output['phrase'].extend(temp)

        return output

    def parse_date__direction(self, text):

        this_regex = r'\bbu\b'

        until_regex_1 = r'\b(son)'
        until_regex_2 = r'((d[ae]n )?(beri|sonra))'
        until_regex = fr'({until_regex_1}|{until_regex_2})'

        ago_regex = r'\b(once|gecen|gect)' # onceki, gectigimiz

        at_regex = r'(de|da)\b'

        next_regex = r'\b(gelecek)\b'

        ##############################################

        output = {}

        ##############################################

        if re.findall(ago_regex, text):
            output['direction'] = 'ago'
            text = re.sub(ago_regex,'',text).strip()

        elif re.findall(until_regex, text):
            output['direction'] = 'until'
            text = re.sub(until_regex,'',text).strip()

        elif re.findall(this_regex, text):
            output['direction'] = 'this'
            text = re.sub(this_regex,'',text).strip()

        elif re.findall(next_regex, text):
            output['direction'] = 'next'
            text = re.sub(next_regex,'',text).strip()

        else:
            # print('No target specified.')
            output['direction'] = 'default'


        return output

    def parse_date(self, text):
        from pyspace.nlp.preprocessing.normalizer.xnormalizer import xNormalizer

        text = xNormalizer.tr_normalize(text).lower()
        
        # today = self.today
        today = self.get_today()
        ##########################################################
        ##########################################################

        output = {}
        output.update(self.parse_date__exact(text))
        output.update(self.parse_date__duration(text))
        output.update(self.parse_date__phrase(text))
        output.update(self.parse_date__direction(text))

        if output['exact'] != []:

            exact_filled = output['exact_filled']

            if len(exact_filled) == 1:
                if output['direction'] == 'until':
                    return exact_filled + [today]
                elif output['direction'] == 'ago':
                    return [DateHelpers.substract_date(exact_filled[0],[0,3,0])] + exact_filled
                else:
                    exact_nonfilled = output['exact']
                    exact_nonfilled = exact_nonfilled[0]

                    if exact_nonfilled[0] != -1:
                        return exact_filled + exact_filled
                    elif exact_nonfilled[0] == -1 and exact_nonfilled[1] != -1:
                        return exact_filled + [[DateHelpers.get_last_day_of_month_year(exact_filled[0][1],exact_filled[0][2]),exact_filled[0][1],exact_filled[0][2]]]
                    elif exact_nonfilled[1] == -1:
                        return exact_filled + [[31, 12, exact_filled[0][2]]]

                    return exact_filled
            elif len(exact_filled) == 2:
                return exact_filled
            else:
                return []

        elif output['durations'] != []:

            durations = output['durations']
            if len(durations) != 1:
                print("WARNING: MORE THAN ONE DURATION.")
                print(durations)
            duration = durations[0]

            if output['direction'] == 'until' or output['direction'] == 'default':
                startdate = DateHelpers.substract_date(today, duration)

                return [startdate, today]

            elif output['direction'] == 'this':
                startdate = copy.deepcopy(today)
                if duration[0] != 0:
                    pass
                elif duration[1] != 0:
                    startdate[0] = 1
                elif duration[2] != 0:
                    startdate[0] = 1
                    startdate[1] = 1
                return [startdate, today]

            elif output['direction'] == 'ago':
                startdate = DateHelpers.substract_date(today, duration)


                if duration[0] != 0:
                    enddate = startdate
                    pass
                elif duration[1] != 0:
                    enddate = copy.deepcopy(startdate)
                    startdate[0] = 1
                    enddate[0] = DateHelpers.get_last_day_of_month_year(enddate[1], enddate[2])
                elif duration[2] != 0:
                    enddate = copy.deepcopy(startdate)
                    startdate[0] = 1
                    startdate[1] = 1
                    enddate[1] = 12
                    enddate[0] = DateHelpers.get_last_day_of_month_year(enddate[1], enddate[2])

                return [startdate, enddate]

        elif output['phrase'] != []:

            def parse_phrase(query, direction=None):
                _base_query = query

                if direction in ['this', 'default']:
                    query = 'bu ' + query

                elif direction in ['ago', 'until', ]: # TODO remove until
                    query = 'gecen ' + query

                elif direction == 'next':
                    query = 'gelecek ' + query 

                duck = self.duckling.query(query)
                duck = [d for d in duck if d['dim'] == 'time']

                if len(duck) > 1:
                    print("WARNING: MORE THAN ONE DUCKLING RESULT.")
                    print(duck)
                elif len(duck) == 0:
                    print("ERROR: NO DUCKLING RESULT FOR GIVEN PHRASE.")
                    return []
                duck = duck[0]

                if 'from' in duck['value'] and 'to' in duck['value']:
                    startdate = duck['value']['from']['value']
                    startdate = [int(startdate[8:10]),int(startdate[5:7]),int(startdate[:4])]
                    enddate = duck['value']['to']['value']
                    enddate = [int(enddate[8:10]),int(enddate[5:7]),int(enddate[:4])]

                    return [startdate, enddate]
                else:
                    startdate = duck['value']['value']
                    startdate = [int(startdate[8:10]),int(startdate[5:7]),int(startdate[:4])]
                    enddate = startdate

                    if _base_query == 'hafta':
                        enddate = DateHelpers.add_date(startdate, [6,0,0])

                    return [startdate, enddate]

            phrases = output['phrase']
            if len(phrases) != 1:
                print("WARNING: MORE THAN ONE PHRASE.")
                print(phrases)
            query = phrases[0]
            startdate, enddate = parse_phrase(query, output['direction'])
            if startdate is None:
                return []
            if (startdate[2] * 10**4 + startdate[1] * 10**2 + startdate[0]) > (today[2] * 10**4 + today[1] * 10**2 + today[0] + 5):
                startdate, enddate = parse_phrase(query, 'ago')
            return [startdate, enddate]

        else:
            return []
