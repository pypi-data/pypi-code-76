import csv
import os
from abc import ABC, abstractmethod
from numpy import random


class Bangsue(ABC):

    @abstractmethod
    def codename_csv_get(self, specify=None):
        pass

    @abstractmethod
    def get_code_name(self, specify=None):
        pass

    @abstractmethod
    def convert_codename_to_string(self, bangsue, selection=None):
        pass


class BTSSkyTrain(Bangsue):

    def __init__(self):
        super()
        self.file_loc = os.path.join(os.path.dirname(__file__), 'file', 'bts_skytrain.csv')

    def codename_csv_get(self, specify=None):
        super().codename_csv_get()
        bangsue = []
        reader = csv.DictReader(open(file=self.file_loc, newline='', encoding='utf-8-sig'))
        for row in reader:
            if row['station'] == '' or row['number'] == '':
                pass
            elif specify is not None:
                if specify == row['station'] or specify == row['number'] or specify == row['line']:
                    bangsue.append({
                        "station": (row['station']).rstrip().replace(' ', '_').replace('-', '_').lower(),
                        "number": (row['number']).rstrip().replace(' ', '').lower(),
                        "line": (row['line']).rstrip().replace(' ', '').lower()
                    })
                else:
                    pass
            else:
                bangsue.append({
                    "station": (row['station']).rstrip().replace(' ', '_').replace('-', '_').lower(),
                    "number": (row['number']).rstrip().replace(' ', '').lower(),
                    "line": (row['line']).rstrip().replace(' ', '').lower()
                })

        return bangsue

    def get_code_name(self, specify=None):
        super().get_code_name()
        bangsue = self.codename_csv_get(specify)
        number = random.randint(0, len(bangsue))
        return bangsue[number]

    def convert_codename_to_string(self, bangsue, selection=None):
        super().convert_codename_to_string(bangsue)
        if selection == "station_only":
            return '_'.join([bangsue['station']])
        elif selection == "station_with_number":
            return '_'.join([bangsue['station'], bangsue['number']])
        elif selection == "number_with_station":
            return '_'.join([bangsue['number'], bangsue['station']])
        elif selection == "number_only":
            return '_'.join([bangsue['number']])


class MRTATrain(Bangsue):

    def __init__(self):
        super()
        self.file_loc = os.path.join(os.path.dirname(__file__), 'file', 'mrta_train.csv')

    def codename_csv_get(self, specify=None):
        super().codename_csv_get()
        bangsue = []
        reader = csv.DictReader(open(file=self.file_loc, newline='', encoding='utf-8-sig'))
        for row in reader:
            if row['station'] == '' or row['number'] == '':
                pass
            elif specify is not None:
                if specify == row['station'] or specify == row['number'] or specify == row['line']:
                    bangsue.append({
                        "station": (row['station']).rstrip().replace(' ', '_').replace('-', '_').lower(),
                        "number": (row['number']).rstrip().replace(' ', '').lower(),
                        "line": (row['line']).rstrip().replace(' ', '').lower()
                    })
                else:
                    pass
            else:
                bangsue.append({
                    "station": (row['station']).rstrip().replace(' ', '_').replace('-', '_').lower(),
                    "number": (row['number']).rstrip().replace(' ', '').lower(),
                    "line": (row['line']).rstrip().replace(' ', '').lower()
                })

        return bangsue

    def get_code_name(self, specify=None):
        super().get_code_name()
        bangsue = self.codename_csv_get(specify)
        number = random.randint(0, len(bangsue))
        return bangsue[number]

    def convert_codename_to_string(self, bangsue, selection=None):
        super().convert_codename_to_string(bangsue)
        if selection == "station_only":
            return '_'.join([bangsue['station']])
        elif selection == "station_with_number":
            return '_'.join([bangsue['station'], bangsue['number']])
        elif selection == "number_with_station":
            return '_'.join([bangsue['number'], bangsue['station']])
        elif selection == "number_only":
            return '_'.join([bangsue['number']])


class ThailandDistrict(Bangsue):

    def __init__(self):
        super()
        self.file_loc = os.path.join(os.path.dirname(__file__), 'file', 'tambon_bse.csv')

    def codename_csv_get(self, specify=None):
        super().codename_csv_get()
        bangsue = []
        reader = csv.DictReader(open(file=self.file_loc, newline='', encoding='utf-8-sig'))
        for row in reader:
            if row['sub_district'] == '' or row['district'] == '' or row['province'] == '':
                pass
            elif row['sub_district'] == row['district'] or row['district'] == row['province']:
                pass
            else:
                if row['sub_district'] == "district":
                    bangsue.append({
                        "district": (row['district']).replace(' ', '').lower(),
                        "province": (row['province']).replace(' ', '_').lower()
                    })
                else:
                    bangsue.append({
                        "sub_district": (row['sub_district']).replace(' ', '').lower(),
                        "district": (row['district']).replace(' ', '').lower(),
                        "province": (row['province']).replace(' ', '_').lower()
                    })

        return bangsue

    def get_code_name(self, specify=None):
        super().get_code_name()
        bangsue = self.codename_csv_get(specify)
        number = random.randint(0, len(bangsue))
        return bangsue[number]

    def convert_codename_to_string(self, bangsue, selection=None):
        super().convert_codename_to_string(bangsue)
        if bangsue['sub_district'] == '':
            if selection == "province_with_district":
                return '_'.join([bangsue['province'], bangsue['district']])
            elif selection == "district":
                return '_'.join([bangsue['district']])
            elif selection == "province":
                return '_'.join([bangsue['province']])
            elif selection == "all":
                return '_'.join([bangsue['district'], bangsue['province']])
        else:
            if selection == "province_with_district":
                return '_'.join([bangsue['province'], bangsue['district']])
            elif selection == "province_with_subdistrict":
                return '_'.join([bangsue['sub_district'], bangsue['province']])
            elif selection == "subdistrict_with_district":
                return '_'.join([bangsue['sub_district'], bangsue['district']])
            elif selection == "subdistrict":
                return '_'.join([bangsue['subdistrict']])
            elif selection == "district":
                return '_'.join([bangsue['district']])
            elif selection == "province":
                return '_'.join([bangsue['province']])
            elif selection == "all":
                return '_'.join([bangsue['sub_district'], bangsue['district'], bangsue['province']])
