import random
import dictdataset


class pydatamake(object):
    def __init__(self):
        self.Interger = 'Interger'
        self.Char = 'Char'
        self.Float = 'Float'

    def Intmake(self, row=10):
        dataset = []
        for i in range(row):
            dataset.append(random.randint(1, 10))
        return dataset

    def Floatmkae(self, row=10):
        dataset = []
        for i in range(row):
            dataset.append(random.uniform(1, 10))
        return dataset

    def Dictmake(self, row=10):
        Dictmake_dataset = []
        for i in range(row):
            Dictmake_dataset.append({'class': random.choice(dictdataset.class_dicts),
                                     'phone': random.choice(dictdataset.phone_dicts),
                                     'name': random.choice(dictdataset.names_dict)})
        return Dictmake_dataset


datamake = pydatamake()
print(datamake.Dictmake())
