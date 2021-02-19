from . import other
import pandas as pd
import os
data_dir = os.path.dirname(os.path.abspath(other.__file__))
data_dir = data_dir.replace("\\","/")
def read(data_dir):
	return pd.read_excel(data_dir+'/rules.xlsx',index_col=0)