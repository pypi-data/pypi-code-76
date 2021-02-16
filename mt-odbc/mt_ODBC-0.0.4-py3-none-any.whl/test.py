import pyodbc

import mt_ODBC
import mt_FileMan

if __name__ == '__main__':

    ioMan = mt_FileMan.mtIOMan
    logFile = ioMan.startLog(ioMan)
    #input(str(logFile))
    #QtCore.pyqtRemoveInputHook()
    #app = QtWidgets.QApplication(sys.argv) # Create QApplication instance
    #window = MainUI() # Create MainUI instance
    #print('pressed the model button...')
    #cur = conDB('DSN=Playground;UID=mt;PWD=mt')
    
    #con = self.mtConnect()
    if not cur:
        print('no connection')
        sys.exit()
    #cur = con.cursor()
    #print(con, cur)
    #input('...')
    while True:
        sql = mt_ODBC.buildQuery()
        #print(sql)
        #print(whereClauses)
        try:
            #result = mt_ODBC.execQuery(cur, sql, preBuilt = True)
            result = mt_ODBC.execQuery(cur, sql, True)
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
        result = ioMan.sorted_nicely(resultList)
        print(result)
        #for x in result:
        #    self.modelComboBox.addItem(x)        
    cur.close()
    #con.close()
    sys.exit(sys.argv) # Start the app