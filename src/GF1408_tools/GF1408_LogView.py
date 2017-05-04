'''
Created on May 3, 2017

@author: rid
'''

from PyQt5 import QtWidgets,QtCore, QtGui

class LogView(QtWidgets.QWidget):
    '''
    classdocs
    '''


    def __init__(self, parent):
        '''
        Constructor
        '''
        super(LogView, self).__init__(parent)
        
        Layout_Log = QtWidgets.QHBoxLayout()
       
        textEdit = QtWidgets.QTextEdit(parent) 
        textEdit.setReadOnly(True)
        Layout_Log.addWidget(textEdit)
        
        self.setLayout(Layout_Log)
        self.setContentsMargins(QtCore.QMargins(0, 0, 0, 0))
        
        self.textEdit = textEdit
        
    def setPlainText(self, text_new):
        
        self.textEdit.setPlainText(text_new)
        cursor =  self.textEdit.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End);
        self.textEdit.setTextCursor(cursor);


    
    