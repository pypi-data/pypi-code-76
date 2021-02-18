from tools.Gerenciador_de_arquivos import dir_to_safe
import pandas as pd
import inspect

class Criar_planilha:
    def __init__(self, classe):
        self.classe = classe

    def class_columns(self):
        attributes = inspect.getmembers(self.classe, lambda a:not(inspect.isroutine(a)))
        properties = [a[0].replace('_',' ').capitalize() for a in attributes if not (a[0].startswith('__') and a[0].endswith('__'))]
        return properties 

    def csv(self, info, titulo):
        df = pd.DataFrame(info, columns=self.class_columns())
        df.to_csv(dir_to_safe('.csv', titulo), sep=';', encoding='utf-8')
    
    def excel(self, info):
        df = pd.DataFrame(info, columns=self.class_columns())
        df.to_excel(dir_to_safe('.xlsx'), encoding='utf-8')