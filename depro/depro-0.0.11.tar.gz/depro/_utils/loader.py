# -*- coding: utf-8 -*-
"""
Created on Wed Dec 25 16:01:40 2019

load data

@author: tadahaya
"""
import pandas as pd
import numpy as np
import xlrd
import csv
from pathlib import Path
import pickle


def to_pickle(data,url):
    """ to save as pickle """
    with open(url,"wb") as f:
        pickle.dump(data,f)


def read_pickle(url):
    """ to load pickle """
    with open(url,"rb") as f:
        temp = pickle.load(f)
    return temp


def load(url,ftype="csv",**kwargs):
    """
    load a file

    Parameters
    ----------
    ftype: str
        "csv","tsv","xlsx"

    sheet: int (ftype="xlsx" only)
        inicates sheet No. to be loaded

    whole: boolean (ftype="xlsx" only)
        returns a list of whole sheets data if True

    """
    file = File()
    if ftype=="tsv":
        file._2tsv()
    elif ftype=="xlsx":
        file._2xlsx()
    return file.load(url,**kwargs)


def load_line(url,ftype="tsv",**kwargs):
    """
    load a file by lines

    Parameters
    ----------
    ftype: str
        "csv" or "tsv"

    """  
    file = File()
    if ftype=="tsv":
        file._2tsv_line()
    elif ftype=="csv":
        file._2csv_line()
    else:
        raise ValueError("*** check file type!! ***")
    return file.load(url,**kwargs)


def load_multiple(url,ftype="csv",**kwargs):
    """
    load files

    Parameters
    ----------
    ftype: str
        "csv","tsv","xlsx"

    Returns
    ----------
    MultipleLoad obj

    """
    data = MultipleLoad()
    data.load(url,ftype,**kwargs)
    print("--- load multiple files ---")
    print("attributes: data, filename, path, path0")
    return data


###########################################################
class MultipleLoad():
    """ return MultipleLoad obj """
    def __init__(self):
        self._file = File()
        self.data = []
        self.filename = []
        self.path = []
        self.path0 = ""

    def _switch(self,ftype,read_line=False):
        if ftype=="tsv":
            if read_line:
                self._file._2tsv_line()
            else:
                self._file._2tsv()
        elif ftype=="csv":
            if read_line:
                self._file._2csv_line()
            else:
                self._file._2csv()
        elif ftype=="xlsx":
            self._file._2xlsx()
        else:
            raise ValueError("** check filetype!! **")

    def _get_path(self,url,ftype,extension=None):
        if extension is None:
            if ftype=="tsv":
                indicator = "*.txt"
            else:
                indicator = "*." + ftype
        else:
            indicator = "*." + extension
        p = Path(url)
        self.path = list(map(lambda x: x.as_posix(),list(p.glob(indicator))))    
        self.filename = [v.split("/")[-1].replace(indicator,"") for v in self.path]
    
    def load(self,url,ftype,extension=None,read_line=False,**kwargs):
        """
        load files
        return MultipleLoad obj

        Parameters
        ----------
        url: str
            a path indicating a folder of interest

        ftype: str
            indicate "csv","tsv", or "xlsx"
            
        extension: str
            indicate extension of files to be loaded

        sheet: int (ftype="xlsx" only)
            inicates sheet No. to be loaded

        whole: boolean (ftype="xlsx" only)
            returns a list of whole sheets data if True

        read_line: boolean (ftype="csv" or "tsv" only)
            read multiple files by line

        """
        self.path0 = url
        self._switch(ftype,read_line)
        self._get_path(url,ftype,extension)
        self.data = []
        ap = self.data.append
        for v in self.path:
            temp = self._file.load(v,**kwargs)
            ap(temp)


### not yet
class LoadLarge():
    """ load large tsv/csv reader line by line """
    def __init__(self,url=""):
        if len(url)==0:
            raise ValueError("input url!!")
        self.url = url
        self.data0 = pd.DataFrame()
        self.data = pd.DataFrame()
        self.sep = ""

    
    def _generator(self,sep="\t"):
        """ generator function """
        with open(self.url,newline="",encoding="utf-8_sig") as f:
            reader = csv.reader(f,delimiter=sep)
            for row in reader:
                yield row


    def check(self,sep="\t",num=100):
        """ to check data content """
        print("check data")
        ### loading
        gen = self._generator(sep=sep)
        lst = []
        ap = lst.append
        for i,v in enumerate(gen):
            if i < num:
                ap(v)
            else:
                break
        self.data0 = pd.DataFrame(lst)
        self.sep = sep
        return self.data0
 
    
    def load(self,sep="",focus=0,flag="",col_end=None):
        """ to read large data line by line """
        print("may consume large memory")
        ### loading
        print("loading...")
        if len(sep)!=0:            
            gen = self._generator(sep=sep)
        elif len(self.sep)!=0:
            gen = self._generator(sep=self.sep)
        else:
            gen = self._generator()
        lst = []
        ap = lst.append
        if col_end is None:
            if len(flag) > 0:                
                for v in gen:
                    if v[focus]==flag:
                        break
                    else:
                        ap(v)
            else:
                for v in gen:
                    ap(v)
        else:
            if len(flag) > 0:                
                for v in gen:
                    if v[focus]==flag:
                        break
                    else:
                        ap(v[:col_end + 1])
            else:
                for v in gen:
                    ap(v[:col_end + 1])
        self.data = pd.DataFrame(lst)
        del lst
        print("completed!!")
        return self.data


###########################################################
class File():
    def __init__(self):
        self.data = FileCsv()

    def _2csv(self):
        self.data = FileCsv()

    def _2csv_line(self):
        self.data = FileCsvLine()

    def _2tsv(self):
        self.data = FileTsv()

    def _2tsv_line(self):
        self.data = FileTsvLine()

    def _2xlsx(self):
        self.data = FileXlsx()

    def load(self,url,**kwargs):
        return self.data.load(url,**kwargs)


###########################################################
class FileXlsx():
    def load(self,url,sheet=None,whole=False):
        """
        read an excel file
        
        """
        dat = xlrd.open_workbook(url)
        sheets = dat.sheets()
        if sheet is None:
            res = []
            for v in sheets:
                try:
                    temp = self._sheet2df(v)
                    res.append(temp)
                except IndexError:
                    break
            if whole==False:
                res = res[0]
        elif type(sheet)==int:
            temp = sheets[sheet]
            res = self._sheet2df(temp)
        else:
            raise ValueError("** check sheet!! **")
        return res


    def _sheet2df(self,sheet):
        """ sheet to dataframe """
        flag = True
        i = 0
        vals = []
        ap = vals.append
        while flag:
            try:
                temp = sheet.row_values(i)
                ap(temp)
                i += 1
            except IndexError:
                flag = False
        col = vals[0]
        del vals[0]
        df = pd.DataFrame(vals,columns=col)
        return df.replace("",np.nan)


class FileCsv():
    def load(self,url,**kwargs):
        return pd.read_csv(url,index_col=0,sep=",",
                        engine='python',**kwargs) # engine is indicated for passing an initialization error 2020/4/12


class FileTsv():
    def load(self,url,**kwargs):
        return pd.read_csv(url,index_col=0,sep="\t",
                        engine='python',**kwargs) # engine is indicated for passing an initialization error 2020/4/12


class FileCsvLine():
    def load(self,url,encoding="utf-8"):
        """ load a data by line """
        with open(url,encoding=encoding) as f:
            reader = csv.reader(f,delimiter=",")
            lst = [v for v in reader]
        return pd.DataFrame(lst)


class FileTsvLine():
    def load(self,url,encoding="utf-8"):
        """ load a data by line """
        with open(url,encoding=encoding) as f:
            reader = csv.reader(f,delimiter="\t")
            lst = [v for v in reader]
        return pd.DataFrame(lst)