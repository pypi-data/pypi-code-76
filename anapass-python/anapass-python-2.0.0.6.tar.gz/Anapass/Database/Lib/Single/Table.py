
from abc import ABCMeta, abstractmethod

class Table(metaclass=ABCMeta) :

    def __init__(this, tableName) : 
        this.__TableName = tableName
    
    def GetTableName(this) :
        return this.__TableName




