from core.pandas_module import write_Data_PD
from WebResources.webWorker import getWeb_data

def getProduct(url,filename="products.xlsx"):
    data = getWeb_data(url)
    write_Data_PD(data,filename)

