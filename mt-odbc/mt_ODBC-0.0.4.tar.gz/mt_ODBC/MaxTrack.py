#!/usr/bin/env python

#from PyQt5.QtWidgets import *
#from PyQt5.QtCore import *
#from PyQt5.QtGui import *

from PyQt5 import QtWidgets, QtCore, uic, QtGui
from datetime import datetime
import winreg, errno

import mt_ODBC
import mt_FileMan

class ActionDone(Exception): pass

class ExtendedCombo( QtWidgets.QComboBox ):
    def __init__( self,  parent = None):
        super( ExtendedCombo, self ).__init__( parent )

        self.setFocusPolicy( QtCore.Qt.StrongFocus )
        self.setEditable( True )
        self.completer = QtWidgets.QCompleter( self )

        # always show all completions
        self.completer.setCompletionMode( QtWidgets.QCompleter.UnfilteredPopupCompletion )
        self.pFilterModel = QtCore.QSortFilterProxyModel( self )
        self.pFilterModel.setFilterCaseSensitivity( QtCore.Qt.CaseInsensitive )



        self.completer.setPopup( self.view() )


        self.setCompleter( self.completer )


        self.lineEdit().textEdited[str].connect( self.pFilterModel.setFilterFixedString )
        self.completer.activated.connect(self.setTextIfCompleterIsClicked)

    def setModel( self, model ):
        super(ExtendedCombo, self).setModel( model )
        self.pFilterModel.setSourceModel( model )
        self.completer.setModel(self.pFilterModel)

    def setModelColumn( self, column ):
        self.completer.setCompletionColumn( column )
        self.pFilterModel.setFilterKeyColumn( column )
        super(ExtendedCombo, self).setModelColumn( column )


    def view( self ):
        return self.completer.popup()

    def index( self ):
        return self.currentIndex()

    def setTextIfCompleterIsClicked(self, text):
      if text:
        index = self.findText(text)
        self.setCurrentIndex(index)
        
    def currentData(self):
        if self.index()<0:
            return ''
        return self.itemData(self.index())

# Define function to import external files when using PyInstaller.
#def resource_path(relative_path):
#    """ Get absolute path to resource, works for dev and for PyInstaller """
#    try:
#        # PyInstaller creates a temp folder and stores path in _MEIPASS
#        base_path = sys._MEIPASS
#    except Exception:
#        base_path = os.path.abspath(".")

#    return os.path.join(base_path, relative_path)

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
    
class ActionDone(Exception): pass

class MainUI(QtWidgets.QFrame):
    def __init__(self):
        super(MainUI, self).__init__() # Call init for inherited class

        uiPath = resource_path('../UI/MaxTrack_Main.ui')
        uic.loadUi(uiPath, self) # Load .ui
        self.stayAlive = False
        
        self.tabs = self.findChild(QtWidgets.QTabWidget, 'tabWidget')
        print(self.findChildren(QtWidgets.QLineEdit))
        
        # Make pointers we need to manipulate widgets
        # Line Edit Widgets
        self.customerLineEdit = self.tabs.findChild(QtWidgets.QLineEdit, 'custNum_lineEdit')
        self.mfgLineEdit = self.tabs.findChild(QtWidgets.QLineEdit, 'mfg_lineEdit')
        self.snPrefixLineEdit = self.tabs.findChild(QtWidgets.QLineEdit, 'snPre_lineEdit')
        self.snStartLineEdit = self.tabs.findChild(QtWidgets.QLineEdit, 'snStart_lineEdit')
        self.snEndLineEdit = self.tabs.findChild(QtWidgets.QLineEdit, 'snEnd_lineEdit')
        self.controlNumLineEdit = self.tabs.findChild(QtWidgets.QLineEdit, 'controlNumStart_lineEdit')
        self.idPrefixLineEdit = self.tabs.findChild(QtWidgets.QLineEdit, 'idPre_lineEdit')
        self.idStartLineEdit = self.tabs.findChild(QtWidgets.QLineEdit, 'idStart_lineEdit')
        self.idEndLineEdit = self.tabs.findChild(QtWidgets.QLineEdit, 'idEnd_lineEdit')
        self.altNameLineEdit = self.tabs.findChild(QtWidgets.QLineEdit, 'nameToAppear_lineEdit')
        # Push Button Widgets
        self.beginPushButt = self.tabs.findChild(QtWidgets.QPushButton, 'start_pushButton')
        self.beginPushButt.clicked.connect(self.beginButtPressed)
        self.beginPushButt = self.tabs.findChild(QtWidgets.QPushButton, 'model_pushButton')
        self.beginPushButt.clicked.connect(self.modelButtPressed)
       # Combo Box Widgets
        #self.modelComboBox = self.tabs.findChild(QtWidgets.QComboBox, 'model_comboBox')
        self.dsnComboBox = self.tabs.findChild(QtWidgets.QComboBox, 'dsn_comboBox')
        self.searchComboBox = ExtendedCombo()
       #Layout Widgets that we need to manipulate later
        self.modelHLayout = self.findChild(QtWidgets.QHBoxLayout, 'horizontalLayout_3')
        #self.searchComboBox = ExtendedCombo()
        
        #Set the variables to read to ODBC sources with winreg 
        root = winreg.HKEY_LOCAL_MACHINE
        key = winreg.OpenKey(root, "SOFTWARE\WOW6432Node\ODBC\ODBC.INI")
        #Create a list to hold the ODBC sources
        self.connList = []
        #Query the registry key set earlier, and add ODBC sources to list
        for i in range(0, winreg.QueryInfoKey(key)[0]):
            #Get the source name
            skey_name = winreg.EnumKey(key, i)
            #print(skey_name) #Verbose output
            #Add source name to list
            self.connList.append(skey_name)
            #If we needed sub-values (which we don't here)
            #skey = winreg.OpenKey(key, skey_name)
        key.Close()
                
        print(self.connList)
            
        for x in self.connList:
            self.dsnComboBox.addItem(x)
        
        self.show() # Show yourself
        
    def modelButtPressed(self):
        print('pressed the model button...')
        cur = self.mtConnect()
        if not cur:
            print('no connection')
            sys.exit()
        sql = "SELECT DISTINCT(i4203) FROM mt.inventory"
        
        try:
            result = mt_ODBC.execQuery(cur, sql, True)
        except pyodbc.Error as err:
            result = "%s Failed to Execute: \n %s" % (err)
        #print(result)
        resultList = []
        for x in result:
            resultList.append(str(x[0]))
            
        #result = sorted(resultList, key=lambda item: (int(item.partition(' ')[0])
        #                       if item[0].isdigit() else float('inf'), item))
        result = ioMan.sorted_nicely(resultList)
        #sprint(result)
        #for x in result:
        #    self.modelComboBox.addItem(x)
        cur.close()
        
        model = QtGui.QStandardItemModel()
        for i,word in enumerate(result):
            item = QtGui.QStandardItem(word)
            model.setItem(i, 0, item)
            
        self.searchComboBox.setModel(model)
        self.searchComboBox.setModelColumn(0)
        self.modelHLayout.addWidget(self.searchComboBox)
        
    def beginButtPressed(self):
        print('pressed the start button...')
        #con = conDB('DSN=Playground;UID=mt;PWD=mt')

        tmpD = self.getFieldData()
        
        requiredValues = ['customer number', 'manufacturer',
            'Serial# start value', 'Serial# end value', 'model']
        for x in requiredValues:
            if len(tmpD[x])<1:
                print('Required information not received.\nThe following values are required:\n')
                [print(x+' : '+self.infoDict[x]) for x in requiredValues]
                return
        # if len(custNum)<1 or len(mfgName)<1 or len(snStart)<1
         # or len(snEnd)<1 or len(modelNumber)<1:
            # print('Required information not received.\nThe following values are required:\n')
            # [print(x+' : '+self.infoDict[x]) for x in requiredValues]
            # return
        
        [print(i+' : '+x) for i, x in self.infoDict.items()]

        con = self.mtConnect()
        if not con:
            print('no connection')
            return
        sql = "SELECT * FROM VALLINKDATA WHERE ROOTDATA = '"+tmpD['model']+"'"
        
        try:
            result = mt_ODBC.execQuery(con, sql, True)
        except:
            result = "Failed to Execute"
        resultList = []
        for x in result:
            resultList.append(x)
        print(resultList)
        result = resultList[0]
        print(result)
        self.infoDict['description'] = result[2]
        self.infoDict['department'] = result[3]
        self.infoDict['cert code'] = result[7]
        self.infoDict['cert cost'] = result[10]
        
        sql = "SELECT ktag FROM customers WHERE K4601 = '"+tmpD['customer number']+"'"
        
        try:
            result = mt_ODBC.execQuery(con, sql, True).fetchone()
        except:
            result = "Failed to Execute"
        print(result)
        self.infoDict['ktag'] = result[0]
        if len(self.infoDict['Control# start'])<1:
            self.infoDict['Control# start'] = self.infoDict['customer number']+\
                                        self.infoDict['Serial# start value']
        [print(i+' : '+x) for i, x in self.infoDict.items()]
        for i, x in self.infoDict.items():
            try:
                msgDetails = msgDetails+'\n'+i+' : '+x
            except:
                msgDetails = i+' : '+x
        numberOfAssets = int(tmpD['Serial# end value'])-int(tmpD['Serial# start value'])+1
        counter = 0
        confMsg = 'Are you sure you want to create '+str(numberOfAssets)+' assets?'
        # msg = QtWidgets.QMessageBox(self, 'Message', confMsg,
                                        # QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        msg = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Question, 'Message', confMsg,
                                        QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        msg.setDetailedText(msgDetails)
        reply = msg.exec_()
        if reply == QtWidgets.QMessageBox.No:
            print('action cancelled by user\n')
            return
        while counter<numberOfAssets:
            #serialNum = int(tmpD['Serial# start value'])
            serialNum = int(tmpD['Serial# start value']) + counter
            serialNumber = tmpD['Serial# Prefix'] + str(serialNum)
            #controlNumber = tmpD['Control# start'] + str(counter)
            
            controlNumber = tmpD['customer number'] + str(serialNum)
            idNumber = ''
            sql = """INSERT INTO mt.Inventory (I4201, I4202, I4203, I4204, I4206,
                I4207, I4210, I4215, I4218, I4222, I4224, I4228, I4229, I4231, I4246,
                idsrc, ktag) VALUES('"""+controlNumber+"', '"+tmpD['manufacturer']+ \
                "', '"+tmpD['model']+"', '"+tmpD['description']+"', '"+ \
                serialNumber+"', '"+idNumber+"', '', '1', '"+tmpD['cert code']+ \
                "', '"+tmpD['cert cost']+"', '"+today+"', 'M', '12', '"+tmpD['Name to appear on cert']+ \
                "', '"+tmpD['department']+"', 'MAX', '"+tmpD['ktag']+"')"
            print(sql)
            try:
                mt_ODBC.execQuery(con, sql, True)
            except:
                result = "Failed to Execute"
            counter = counter + 1
        
        con.close()
        return
        
    def getFieldData(self):
        custNum = self.customerLineEdit.text()
        mfgName = self.mfgLineEdit.text()
        snPrefix = self.snPrefixLineEdit.text()
        snStart = self.snStartLineEdit.text()
        snEnd = self.snEndLineEdit.text()
        idPrefix = self.idPrefixLineEdit.text()
        idStart = self.idStartLineEdit.text()
        idEnd = self.idEndLineEdit.text()
        controlNumStart = self.controlNumLineEdit.text()
        altName = self.altNameLineEdit.text()
        #this wasn't working right. my function needs work (ExtendedCombo.currentData)
        #modelNumber = self.searchComboBox.currentData()
        modelNumber = self.searchComboBox.currentText()
        
        self.infoDict = {'customer number': custNum, 'manufacturer': mfgName,
            'Serial# start value': snStart, 'Serial# end value': snEnd,
            'Serial# Prefix': snPrefix, 'ID# prefix': idPrefix,
            'ID# start': idStart, 'ID# end': idEnd,
            'Control# start': controlNumStart,
            'Name to appear on cert': altName, 'model': modelNumber}

        return self.infoDict
        
    def mtConnect(self):
        dsn = self.dsnComboBox.currentText()
        try:
            con = mt_ODBC.conDB('DSN='+dsn+';UID=mt;PWD=mt')
        except:
            print('could not connect to '+dsn)
            return None
        return con

if __name__ == '__main__':
    import sys
    import os

    theCurrentDatetime = datetime.now()
    today = theCurrentDatetime.strftime('%m/%d/%y')
    
    ioMan = mt_FileMan.mtIOMan
    logFile = ioMan.startLog(ioMan)
    
    QtCore.pyqtRemoveInputHook()
    app = QtWidgets.QApplication(sys.argv) # Create QApplication instance
    window = MainUI() # Create MainUI instance
    sys.exit(app.exec_(), sys.argv) # Start the app
