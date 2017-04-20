'''
Created on Apr 19, 2017

@author: rid
'''


from xlrd.formula import num2strg
from PyQt5 import QtWidgets


class GuiTools(object):
    '''
    classdocs
    '''


    def __init__(self, parent):
        '''
        Constructor
        '''
        super(GuiTools,self).__init__()
        self.parent = parent
        self.mainLayout = None
    
    @staticmethod
    def layout_widgets(layout):
        return (layout.itemAt(i).widget() for i in range(layout.count()))


    def setEnabled(self,en):
        if(self.mainLayout == None):
            return
        for obj in GuiTools.layout_widgets(self.mainLayout):
            if hasattr(obj, 'isEnabled'):
                obj.setEnabled(en)

    def getRegOrNone(self,regName):
        if hasattr(self.parent.BIDI, regName):
            return getattr(self.parent.BIDI,regName)
        return None

    def onChangeComboBox(self):
        
        ComboBox = self.parent.sender()
        regName = str(ComboBox.accessibleName())
        content_Str = str(ComboBox.currentText())
        self.parent.statusBar().showMessage(regName + ' was changed to ' + content_Str) 
        
        BIDI_REG = self.getRegOrNone(regName)
    
        if BIDI_REG:
            BIDI_REG.set( content_Str)
    
    def onChangeSpinBox(self):
        
        SpinBox = self.parent.sender()
        regName = str(SpinBox.accessibleName())
        newContent = SpinBox.value()
        self.parent.statusBar().showMessage(SpinBox.accessibleName() + ' swas changed to ' + num2strg(newContent)) 
        
        
        BIDI_REG = self.getRegOrNone(regName)
        
        if BIDI_REG:
            if SpinBox.__class__== QtWidgets.QDoubleSpinBox:
                BIDI_REG.set( float(newContent) )
            else:
                BIDI_REG.set( int(newContent) )
            
    def onChangeCheckBox(self):
        
        CheckBox = self.parent.sender()
        regName = str(CheckBox.accessibleName())
        self.parent.statusBar().showMessage(regName + ' was changed to ' +  num2strg(CheckBox.isChecked()))
        
        
        BIDI_REG = self.getRegOrNone(regName)
        newContent = int(CheckBox.isChecked())
                  
        if BIDI_REG:
            #print BIDI_REG
            BIDI_REG.set( newContent)
            