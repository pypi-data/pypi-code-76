import re
import math

from .datas.a1 import a1_data
from .datas.a2 import a2_data
from .datas.a3 import a3_data


class Address:

    def smart(self, string, user=True):
        '''
        智能解析
        '''
        if user:
            decompose = self.decompose(string)
            result = decompose
        else:
            result = {}
            result['addr'] = string

        fuzz = self.fuzz(result['addr'])
        parse = self.parse(fuzz['a1'], fuzz['a2'], fuzz['a3'])

        result['province'] = parse['province']
        result['city'] = parse['city']
        result['region'] = parse['region']

        result['street'] = fuzz['street'] if fuzz.get('street') else ''
        result['street'] = result['street'].replace(result['region'], '')
        result['street'] = result['street'].replace(result['city'], '')
        result['street'] = result['street'].replace(result['province'], '')

        return result

    @staticmethod
    def decompose(string):
        '''
        分离手机号(座机)，身份证号，姓名等用户信息
        '''
        compose = {}

        search = ['收货地址', '详细地址', '地址', '收货人', '收件人', '收货', '所在地区', '邮编', '电话', '手机号码','身份证号码', '身份证号', '身份证', '：', ':', '；', ';', '，', ',', '。']
        for item in search:
            string = string.replace(item, ' ')
        
        string = re.sub(r'\s{1,}', ' ', string)
        string = re.sub(r'0-|0?(\d{3})-(\d{4})-(\d{4})', r'\1\2\3', string)

        match = re.search(r'\d{18}|\d{17}X', string, re.IGNORECASE)
        if match:
            compose['idn'] = match.group().upper()
            string = string.replace(match.group(), '')

        match = re.search(r'\d{7,11}|\d{3,4}-\d{6,8}', string)
        if match:
            compose['mobile'] = match.group()
            string = string.replace(match.group(), '')

        match = re.search(r'\d{6}', string)
        if match:
            compose['postcode'] = match.group()
            string = string.replace(match.group(), '')

        string = re.sub(r' {2,}', ' ', string).strip()

        split_arr = string.split(' ')
        if len(split_arr) > 1:
            compose['name'] = split_arr[0]
            for value in split_arr:
                if len(value) < len(compose['name']):
                    compose['name'] = value
            string = string.replace(compose['name'], '')

        compose['addr'] = string

        return compose

    @staticmethod
    def fuzz(addr):
        '''
        根据统计规律分析出二三级地址
        '''
        addr_origin = addr
        addr = addr.replace(' ', '')
        addr = addr.replace(',', '')
        addr = addr.replace('自治区', '省')
        addr = addr.replace('自治州', '州')

        addr = addr.replace('小区', '')
        addr = addr.replace('校区', '')

        a1 = ''
        a2 = ''
        a3 = ''
        street = ''

        if (addr.find('县') != -1 and addr.find('县') < math.floor((len(addr) / 3) * 2) or (addr.find('区') != -1 and addr.find('区') < math.floor((len(addr) / 3) * 2)) or addr.find('旗') != -1 and addr.find('旗') < math.floor((len(addr) / 3) * 2)):

            if addr.find('旗') != -1:
                deep3_keyword_pos = addr.find('旗')
                a3 = addr[deep3_keyword_pos-1:deep3_keyword_pos+1]
            if addr.find('区') != -1:
                deep3_keyword_pos = addr.find('区')

                if addr.find('市') != -1:
                    city_pos = addr.find('市')
                    zone_pos = addr.find('区')
                    a3 = addr[city_pos+1:zone_pos+1]
                else:
                    a3 = addr[deep3_keyword_pos-2:deep3_keyword_pos+1]
            if addr.find('县') != -1:
                deep3_keyword_pos = addr.find('县')

                if addr.find('市') != -1:
                    city_pos = addr.find('市')
                    zone_pos = addr.find('县')
                    a3 = addr[city_pos+1:zone_pos+1]
                else:
                    
                    if addr.find('自治县') != -1:
                        a3 = addr[deep3_keyword_pos-6:deep3_keyword_pos+1]
                        if a3[0:1] in ['省', '市', '州']:
                            a3 = a3[1:]
                    else:
                        a3 = addr[deep3_keyword_pos-2:deep3_keyword_pos+1]
            street = addr_origin[deep3_keyword_pos+1:]
        else:
            if addr.find('市') != -1:

                if addr.count('市') == 1:
                    deep3_keyword_pos = find_last(addr, '市')
                    a3 = addr[deep3_keyword_pos-2:deep3_keyword_pos+1]
                    street = addr_origin[deep3_keyword_pos+1:]
                elif addr.count('市') >= 2:
                    deep3_keyword_pos = find_last(addr, '市')
                    a3 = addr[deep3_keyword_pos-2:deep3_keyword_pos+1]
                    street = addr_origin[deep3_keyword_pos+1:]
            else:

                a3 = ''
                street = addr

        if addr.find('市') != -1 or addr.find('盟') != -1 or addr.find('州') != -1:
            tmp_pos_1 = addr.find('市')
            tmp_pos_2 = addr.find('盟')
            tmp_pos_3 = addr.find('州')
            tmp_pos_4 = addr.find('自治州')
            if tmp_pos_1 != -1:
                a2 = addr[tmp_pos_1-2:tmp_pos_1+1]
            elif tmp_pos_2 != -1:
                a2 = addr[tmp_pos_2-2:tmp_pos_2+1]
            elif tmp_pos_3 != -1:
                
                if tmp_pos_4 != -1:
                    a2 = addr[tmp_pos_4-4:tmp_pos_4+1]
                else:
                    a2 = addr[tmp_pos_4-2:tmp_pos_4+1]
            else:
                a2 = ''
        else:
            a2 = ''

        r = {
            'a1': a1,
            'a2': a2,
            'a3': a3,
            'street': street,
        }

        return r

    @staticmethod
    def parse(a1, a2, a3):
        '''
        智能解析出省市区+街道地址
        '''
        r = {}

        if a3 != '':

            area3_matches = {}
            area2_matches = {}
            for i, v in a3_data.items():
                if v['name'].find(a3) != -1:
                    area3_matches[i] = v

            if area3_matches and len(area3_matches) > 1:
                if a2:
                    for i, v in a2_data.items():
                        if v['name'].find(a2) != -1:
                           area2_matches[i] = v

                    if area2_matches:
                        for i, v in area3_matches.items():

                            if area2_matches.get(v['pid']):
                                r['city'] = area2_matches[v['pid']]['name']
                                r['region'] = v['name']
                                sheng_id = area2_matches[v['pid']]['pid']
                                r['province'] = a1_data[sheng_id]['name']
                else:

                    r['province'] = ''
                    r['city'] = ''
                    r['region'] = a3
            elif area3_matches and len(area3_matches) == 1:
                for i, v in area3_matches.items():
                    city_id = v['pid']
                    r['region'] = v['name']
                city = a2_data[city_id]
                province = a1_data[city['pid']]

                r['province'] = province['name']
                r['city'] = city['name']
            elif not area3_matches and a2 == a3:

                for i, v in a2_data.items():
                    if v['name'].find(a2) != -1:
                        area2_matches[i] = v
                        sheng_id = v['pid']
                        r['city'] = v['name']

                r['province'] = a1_data[sheng_id]['name']
                r['region'] = ''

        return r    

def find_last(haystack, needle):
    last_pos = -1
    while True:
        pos = haystack.find(needle, last_pos+1)
        if pos == -1:
            return last_pos
        last_pos = pos
