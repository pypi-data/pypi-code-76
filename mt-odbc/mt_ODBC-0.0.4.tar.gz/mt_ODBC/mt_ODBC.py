#!/usr/bin/env python

#from PyQt5.QtWidgets import *
#from PyQt5.QtCore import *
#from PyQt5.QtGui import *

import pyodbc

class PyODBCWrapper(object): 
    def __init__(self, cnxn): 
        self.cnxn = cnxn 

    def __getattr__(self, attr): 
        return getattr(self.cnxn, attr) 

    def cursor(self): 
        return CursorWrapper(self.cnxn.cursor()) 

class CursorWrapper(object): 
    def __init__(self, cursor): 
        self.cursor = cursor 

    def __getattr__(self, attr): 
        return getattr(self.cursor, attr) 

    def fetchone(self): 
        row = self.cursor.fetchone() 
        if not row: 
            return None 
        return dict((t[0], value) for t, value in zip (self.cursor.description, row))
        
    

def conDB(connectionString):
    try:
        con = pyodbc.connect(connectionString, autocommit=True)
        cur = PyODBCWrapper(con)
    except pyodbc.Error as err:
        print(err)
    #cursor = con.cursor()
    return cur

def disconDB(CursorWrapper, PyODBCWrapper):
    CursorWrapper.cursor.close()
    PyODBCWrapper.close()

def callStoredProc(conn, procName, *args):
    sql = """SET NOCOUNT ON;
             EXEC %s %s""" % (procName, ','.join(['?'] * len(args)))
    conn.execute(sql, args)
    return 0

def queryStoredProc(conn, procName, *args):
    sql = """SET NOCOUNT ON;
             EXEC %s %s""" % (procName, ','.join(['?'] * len(args)))
    #print(sql)
    #print(args)
    try:
        result = conn.execute(sql, args).fetchone()
    except pyodbc.Error as err:
        result = "%s Failed to Execute: \n %s" % (procName, err)
    if verbose:
        print(result)
    return result
    
def buildQuery(sql=""):
    wheresDone = False
    whereClauses = []
    while len(sql)<1:
        sql = input('Enter an sql select query...\n')
    while wheresDone is False:
        whereX = input('enter \'where what\' - optional...')
        if len(whereX)>0:
            whereY = input('enter \'what is\'...')
            whereClause = (whereX, whereY)
            whereClauses.append(whereClause)
        else:
            wheresDone = True
    print(whereClauses)
    for x in whereClauses:
        if whereClauses.index(x)==0:
            if x[0][0:3] == "[L]":
                sql = sql + ' where ' + x[0][3:] + " LIKE '" + x[1] + "'"
            else:
                sql = sql + ' where ' + x[0] + "='" + x[1] + "'"
        else:
            if x[0][0:3] == "[L]":
                sql = sql + ' and ' + x[0][3:] + " LIKE '" + x[1] + "'"
            else:
                sql = sql + ' and ' + x[0] + "='" + x[1] + "'"
    input(sql)
    return sql
    
def execQuery(conn, query, preBuilt = False, *args):
    sql = query
    print(conn, query, args)
    if len(args)>0:
        for arg in args[0]:
            whereX = arg[0]
            whereY = arg[1]
            if arg == args[0][0] and preBuilt == False:
                sql = sql + ' where ' + whereX + "='" + whereY + "'"
            else:
                sql = sql + ' and ' + whereX + "='" + whereY + "'"
        print(sql)
    result = conn.execute(sql)
    return result
    
    
class Tee(object):
    def __init__(self, *files):
        self.files = files
    def write(self, obj):
        for f in self.files:
            f.write(obj)
            f.flush() # If you want the output to be visible immediately
    def flush(self) :
        for f in self.files:
            f.flush()
            
            
if __name__ == '__main__':

    import sys
    import pathlib
    from datetime import datetime

    theCurrentDatetime = datetime.now()
    #Make dir if not exist (python 3.5+), use pathlib2 < 3.5
    pathlib.Path('../LOG').mkdir(parents=True, exist_ok=True)
    pathlib.Path('../UI').mkdir(parents=True, exist_ok=True) 
    logFN = '../LOG/log_'+theCurrentDatetime.strftime("%Y-%m-%d_%H-%M-%S")+'.log'
    f = open(logFN, 'w')
    original = sys.stdout
    sys.stdout = Tee(sys.stdout, f)
    #QtCore.pyqtRemoveInputHook()
    #app = QtWidgets.QApplication(sys.argv) # Create QApplication instance
    #window = MainUI() # Create MainUI instance
    #print('pressed the model button...')
    con = conDB('DSN=Playground;UID=mt;PWD=mt')
    #con = self.mtConnect()
    if not con:
        print('no connection')
        sys.exit()
    cur = con.cursor()
    print(con, cur)
    input('...')
    sql = "SELECT DISTINCT(i4203) FROM mt.inventory"
    whereX = ''
    whereX = ''
    while True:
        print(sql)
        try:
            if len(whereX)>0:
                #result = con.execute(sql, (whereY)).fetchone()
                result = cur.execute(sql, (whereY)).fetchone()
            else:
                result = con.execute(sql).fetchall()
        except pyodbc.Error as err:
            result = "%s Failed to Execute: \n %s" % (err)
        print(result)
        resultList = []
        x = ''
        for x in result:
            #if len(whereX)>0:
            #    input(x)
            resultList.append(str(x))
            
        #result = sorted(resultList, key=lambda item: (int(item.partition(' ')[0])
        #                       if item[0].isdigit() else float('inf'), item))
        result = sorted_nicely(resultList)
        print(result)
        #for x in result:
        #    self.modelComboBox.addItem(x)
        sql = input('Enter an sql select query...\n')
        whereX = input('enter \'where what\' - optional...')
        if len(whereX)>0:
            whereY = input('enter \'what is\'...')
            sql = sql + ' where ' + whereX + "=?"
    con.close()
    sys.exit(sys.argv) # Start the app
