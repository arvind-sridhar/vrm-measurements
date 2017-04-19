#!/usr/bin/env python
# -*- coding: utf-8 -*- 
'''
Created on Apr 18, 2017

@author: rid
'''

from threading import Thread
from PyQt4 import QtGui,QtCore
from GF1408_CONST import CONST
import PyQt4

class EquipmentGui_Class(object):
    '''
    classdocs
    '''
    
    WIDTH = 250
    HEIGHT = 300
    
    MAX_VIN = 1600 #mV
    MAX_IIN = 200 #mA
    MAX_VD = 800
    MAX_ID = 250
    MAX_FAC = 0.8
    MAX_FDC = 0.0
    MAX_FF = 8000

    def __init__(self, parent):
        
        GridLayout = QtGui.QGridLayout();
        
        # Connect and Init Hammerhead
        Button_Connect = QtGui.QPushButton(CONST.HAMMERHEAD_CONNECT_AND_INIT, parent)
        Button_Connect.setAccessibleName(CONST.HAMMERHEAD_CONNECT_AND_INIT)
        Button_Connect.clicked.connect(self.onClickButton)
        
        GridLayout.addWidget(Button_Connect,0,0,1,4);
        ##################
        # Equipemt Table #
        ##################
        
        
        FONT=QtGui.QFont( "Times", 10, QtGui.QFont.Serif);
        
        # Table Heading
        Label_Name = QtGui.QLabel(CONST.NAME,parent)
        Label_Reference = QtGui.QLabel(CONST.REFERENCE,parent)
        Label_Reference.setAlignment(QtCore.Qt.AlignHCenter)
        Label_Value = QtGui.QLabel(CONST.VALUE,parent)
        Label_Value.setAlignment(QtCore.Qt.AlignHCenter)
        Label_Sync = QtGui.QLabel(CONST.SYNC,parent)
        Label_Sync.setAlignment(QtCore.Qt.AlignRight)
        
        GridLayout.addWidget(Label_Name,1,0)
        GridLayout.addWidget(Label_Reference,1,1)
        GridLayout.addWidget(Label_Value,1,2)
        GridLayout.addWidget(Label_Sync,1,3)
        
        POS = 2;
        def createInstrumentGroup(_LABEL,_MAXVAL,_UNIT):
            Label = QtGui.QLabel(_LABEL,parent)
            Label.setFont(FONT)
            SpinBox = QtGui.QSpinBox()
            SpinBox.setSingleStep(10)
            SpinBox.setRange(0,_MAXVAL)
            SpinBox.setSuffix(_UNIT)
            SpinBox.setAlignment(QtCore.Qt.AlignRight)
            SpinBox.setAccessibleName(_LABEL)
            Label_IST = QtGui.QLabel("1600"+_UNIT,parent)
            CheckBox_Sync = QtGui.QCheckBox("",parent)
            CheckBox_Sync.setAccessibleName(_LABEL+CONST.SYNC)
            CheckBox_Sync.setLayoutDirection(QtCore.Qt.RightToLeft)            
            _POS = POS;
                     
            GridLayout.addWidget(Label,_POS,0)
            GridLayout.addWidget(SpinBox,_POS,1)
            GridLayout.addWidget(Label_IST,_POS,2)
            GridLayout.addWidget(CheckBox_Sync,_POS,3)
            _POS = _POS+1;
            
            return _POS
        
        POS=createInstrumentGroup(CONST.EQ_VIN,self.MAX_VIN,CONST.UNIT_MV)
        POS=createInstrumentGroup(CONST.EQ_INMAX,self.MAX_IIN,CONST.UNIT_MA)
        POS=createInstrumentGroup(CONST.EQ_Vd,self.MAX_VD,CONST.UNIT_MV)
        POS=createInstrumentGroup(CONST.EQ_IdMAX,self.MAX_ID,CONST.UNIT_MA)
        POS=createInstrumentGroup(CONST.EQ_FREQ_AC,self.MAX_FAC,CONST.UNIT_MV)
        POS=createInstrumentGroup(CONST.EQ_FREQ_DC,self.MAX_FDC,CONST.UNIT_MV)
        POS=createInstrumentGroup(CONST.EQ_FREQ_F,self.MAX_FF,CONST.UNIT_MHZ)
        
        gb_Hammerhead = QtGui.QGroupBox(CONST.EQUIPMENT)
        gb_Hammerhead.setLayout(GridLayout)
        gb_Hammerhead.setMaximumWidth(self.WIDTH)
        gb_Hammerhead.setAlignment(QtCore.Qt.AlignHCenter)
        
        self.GroupBox = gb_Hammerhead
        self.parent = parent
    
    def onClickButton(self):
        
        parent = self.parent
        parent.buttonClicked()  # print out pressed button
        
        '''
        try: 
            self.allOff()
        except Exception as e:
            self.status('Fail 1')
        '''
        
        if parent.sender().accessibleName() == CONST.HAMMERHEAD_CONNECT_AND_INIT:
            self.connectHammerhead(parent.sender()) 
        
        try:
            if parent.sender().text() == CONST.HAMMERHEAD_INIT:
                self.initHammerhead()                   
            if parent.sender().text() == CONST.EXIT:
                self.close() 

        except Exception as e:
            print(str(e))  
        
    def connectHammerhead(self,button):
        
        button.setEnabled(False);
        parent = self.parent
        connected = parent.h.isConnected
        
        def finishedConnect():
        
            button.setEnabled(True);
            if(connected):
                parent.status('Connected')
                newtext = CONST.HAMMERHEAD_DISCONNECT
            else:
                parent.status('Disconnected')
                newtext = CONST.HAMMERHEAD_CONNECT_AND_INIT
                
            button.setText(newtext)  
        
        parent.PYQT_SIGNAL.connect(finishedConnect)
        Thread(target=self.async_connectHH).start() 
        parent.isConnected(connected)
    
    def async_connectHH(self):

        parent = self.parent            
        try:
            if parent.h.isConnected:
                parent.h.disconnect()
            else:
                parent.h.connect()
                parent.h.init()
        except Exception as e:
            print(str(e))
            
        parent.PYQT_SIGNAL.emit()

    
