'''
Created on Apr 19, 2017

@author: rid
'''

import threading
from PyQt5 import QtWidgets,QtCore
from xlrd.formula import num2strg



class GuiTools(QtCore.QObject):
    '''
    classdocs
    '''


    def __init__(self,parent):
        '''
        Constructor
        '''
        super(GuiTools, self).__init__(parent)
        self.parent = parent
        self.mainLayout = None
        
        
        self.lock = threading.RLock()
    
    @staticmethod
    def layout_widgets(layout):
        return (layout.itemAt(i).widget() for i in range(layout.count()))


    def setEnabled(self, en, ignores=[]):
        if(self.mainLayout == None):
            return
        for obj in GuiTools.layout_widgets(self.mainLayout):
            if hasattr(obj, 'isEnabled') and obj not in ignores:
                obj.setEnabled(en)
                
    def getRegOrNone(self, regName):
        if hasattr(self.parent.BIDI, regName):
            return getattr(self.parent.BIDI, regName)
        return None

    def onChangeComboBox(self):
        
        ComboBox = self.parent.sender()
        regName = str(ComboBox.accessibleName())
        content_Str = str(ComboBox.currentText())
        self.parent.statusBar().showMessage(regName + ' was changed to ' + content_Str) 
        
        BIDI_REG = self.getRegOrNone(regName)
    
        if BIDI_REG:
            self.async_updateBIDIReg( BIDI_REG, content_Str)
    
    def onChangeSpinBox(self):
        
        SpinBox = self.parent.sender()
        regName = str(SpinBox.accessibleName())
        newContent = SpinBox.value()
        self.parent.statusBar().showMessage(SpinBox.accessibleName() + ' swas changed to ' + num2strg(newContent)) 
        
        
        BIDI_REG = self.getRegOrNone(regName)
        
        if BIDI_REG:
            if SpinBox.__class__ == QtWidgets.QDoubleSpinBox:
                newContent=float(newContent)
            else:
                newContent=int(newContent)
            self.async_updateBIDIReg( BIDI_REG, newContent)
            
    def onChangeCheckBox(self):
        
        CheckBox = self.parent.sender()
        regName = str(CheckBox.accessibleName())
        self.parent.statusBar().showMessage(regName + ' was changed to ' + num2strg(CheckBox.isChecked()))
        
        
        BIDI_REG = self.getRegOrNone(regName)
        newContent = int(CheckBox.isChecked())
                  
        if BIDI_REG:
            # print BIDI_REG
            self.async_updateBIDIReg( BIDI_REG, newContent)
        
        return CheckBox,regName,newContent
    
    
    def async_updateBIDIReg(self, BIDI_REG, newContent):
        
        def updateReg():
            
            with self.lock:
                BIDI_REG.set(newContent)
        
        threading.Thread(target=updateReg).start()
    
    
        
        