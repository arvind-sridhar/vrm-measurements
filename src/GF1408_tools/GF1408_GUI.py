#!/usr/bin/env python
# -*- coding: utf-8 -*- 

'''
Created on Apr 12, 2017

@author: rid
'''

from GF1408_CONST import CONST
from PyQt4 import QtGui, QtCore
from GF1408_tools import GF1408_BIDI,GUI_Parent
from GUI_LoadCTRL import LoadControl_Class
from GUI_Hammerhead import EquipmentGui_Class
from GUI_DPWM import DPWMControl_Class


import hammerhead
from xlrd.formula import num2strg



class GF1408_GUI(QtGui.QMainWindow):
    
    WINDOW_SIZE=(500,500)
    WINDOW_NAME='CarrICool GF1408 - Control Window'
    
    PYQT_SIGNAL = QtCore.pyqtSignal()
    
    def __init__(self):
        super(GF1408_GUI, self).__init__()
        self.h = hammerhead.Hammerhead()
        self.initUI()
        #self.BIDI = GF1408_BIDI()
        
    def initUI(self):
        
        vMainBox, vMainLayout = self.addVWidget()
        self.setCentralWidget(vMainBox)    
        hMainBox, hMainLayout = self.addHWidget()
        vMainLayout.addWidget(self.initButtons())
        vMainLayout.addWidget(hMainBox)
        #hMainLayout.addWidget(self.setOnMeasButtons())
        #hMainLayout.addWidget(self.setSweepButtons())
        
        
        # Initi Window
        self.statusBar()
        self.setGeometry( 25, 20,self.WINDOW_SIZE[0],self.WINDOW_SIZE[1])
        self.setFixedSize(self.WINDOW_SIZE[0],self.WINDOW_SIZE[1])
        self.setWindowTitle(self.WINDOW_NAME)
        self.show()
    
    def initButtons(self):
        
        v0Box, v0Layout = self.addVWidget()
        h0Box, h0Layout = self.addHWidget()   
        
        self.Load_GUI = LoadControl_Class(self)
        self.HammerHead_GUI = EquipmentGui_Class(self)
        self.DPWM_GUI = DPWMControl_Class(self)
        
        # TODO: remove comment
        #self.DPWM_GUI.setEnabled(False)
        #self.Load_GUI.setEnabled(False)
        
        v0Layout.addWidget(self.HammerHead_GUI.GroupBox)
        v0Layout.addWidget(self.Load_GUI.GroupBox)
        
        h0Layout.addWidget(v0Box)
        h0Layout.addWidget(self.DPWM_GUI.GroupBox)
         
        h0Box.setMaximumWidth(500)
        #v0Box.setMaximumWidth(100)
        return h0Box        
    
    def addVWidget(self):
        Box = QtGui.QWidget()
        Layout = QtGui.QVBoxLayout()
        Box.setLayout(Layout)
        Box.setContentsMargins(QtCore.QMargins(0, 0, 0, 0))
        Layout.layout().setContentsMargins(0, 0, 0, 0)
        return Box, Layout   
    
    def addHWidget(self):
        Box = QtGui.QWidget()
        Layout = QtGui.QHBoxLayout()
        Box.setLayout(Layout)
        Box.setContentsMargins(QtCore.QMargins(0, 0, 0, 0))
        Layout.layout().setContentsMargins(0, 0, 0, 0)
        return Box, Layout
    
    def buttonClicked(self):
        sender = self.sender()
        self.statusBar().showMessage(sender.text() + ' was pressed')         
    
    def status(self, text):
        self.statusBar().showMessage(text)  
        
    def onClickButton(self):
        
        self.buttonClicked() # print out pressed button
        try:
            
            if self.sender().text() == CONST.HAMMERHEAD_INIT:
                self.initHammerhead()                   
            elif self.sender().text() == CONST.EXIT:
                self.close() 
            else:
                print(self.sender()) 
        except Exception as e:
            print(str(e))  


    def onChangeComboBox(self):
        
        
        sender = self.sender()
        self.statusBar().showMessage(sender.accessibleName() + ' was changed to ' + sender.currentText()) 
    
    def onChangeSpinBox(self):
        sender = self.sender()
        self.statusBar().showMessage(sender.accessibleName() + ' was changed to ' + num2strg(sender.value())) 
      
    # Hammer Head Functions
    
    def onChangeCheckBox(self):
        sender = self.sender()
        self.statusBar().showMessage(sender.accessibleName() + ' was changed to ' +  num2strg(sender.isChecked())) 
      
    
    def closeEvent (self, eventQCloseEvent):
        answer = QtGui.QMessageBox.question (
            self,
            'Exit',
            'Are you sure you want to quit ?',
            QtGui.QMessageBox.Yes,
            QtGui.QMessageBox.No)
        if (answer == QtGui.QMessageBox.Yes) or (False):
            self.h.disconnect()
            eventQCloseEvent.accept()
        else:
            eventQCloseEvent.ignore()   
    
    def isConnected(self,connected):
        self.DPWM_GUI.setEnabled(connected)
        self.Load_GUI.setEnabled(connected)
        