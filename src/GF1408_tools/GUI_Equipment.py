#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on Apr 18, 2017

@author: rid
'''


from threading import Timer
from threading import Thread
from PyQt5 import QtWidgets,QtCore,Qt
from PyQt5.QtCore import pyqtSignal
from GF1408_tools.GF1408_CONST import CONST
from GF1408_tools.GUI_Parent import GuiTools
from GF1408_tools.GF1408_MConfig import GF1408config
from GF1408_tools.GF1408_LogView import LogView
from PyQt5.Qt import QPushButton

from typing import List

class EquipmentGui_Class(GuiTools):
    '''
    Class modeling the equipment GUI components. 
    '''

    WIDTH = 350
    HEIGHT = 300

    MAX_VIN = 1600  # mV
    MAX_IIN = 200  # mA
    MAX_VD = 800  # mV
    MAX_ID = 250  # mA
    MAX_FAC = 800  # mV
    MAX_FDC = 0.0  # mV
    MAX_FF = 8000  # MHz
    
    PYQT_SIGNAL_HH = pyqtSignal()
    PYQT_SIGNAL_INST = pyqtSignal()
    PYQT_SIGNAL_LOG = pyqtSignal()

    def __init__(self, parent):
        
        super(EquipmentGui_Class, self).__init__(parent)
        
        Layout_Container = QtWidgets.QVBoxLayout()
        Layout_Inner = QtWidgets.QHBoxLayout()
        
        TabWidget = QtWidgets.QTabWidget(parent)
        
        Layout_Inner2 = QtWidgets.QVBoxLayout()
        GridLayout = QtWidgets.QGridLayout();

        BoxButtons = QtWidgets.QWidget()
        BoxButtons.setLayout(Layout_Inner)
        BoxButtons.setContentsMargins(QtCore.QMargins(0, 0, 0, 0))
        Layout_Inner.layout().setContentsMargins(0, 0, 0, 0)
        
        BoxControls = QtWidgets.QWidget()
        BoxControls.setLayout(Layout_Inner2)
        BoxControls.setContentsMargins(QtCore.QMargins(0, 0, 0, 0))
        Layout_Inner2.layout().setContentsMargins(0, 0, 0, 0)
        
        logView = LogView(parent);
        self.logView = logView
        
        self.PYQT_SIGNAL_LOG.connect(self.updateLog)
        
        TabWidget.addTab(BoxControls, "Controls")
        TabWidget.addTab(logView , "Log")

        Box3 = QtWidgets.QWidget()
        Box3.setLayout(GridLayout)
        Box3.setContentsMargins(QtCore.QMargins(0, 0, 0, 0))


        # Connect and Init Hammerhead
        Button_Connect = QtWidgets.QPushButton(CONST.HAMMERHEAD_CONNECT_AND_INIT, parent)
        Button_Connect.setAccessibleName(CONST.HAMMERHEAD_CONNECT_AND_INIT)
        Button_Connect.clicked.connect(self.onClickButton)

        Button_ConnectINST = QtWidgets.QPushButton(CONST.INSTRUMENTS_CONNECT_AND_INIT, parent)
        Button_ConnectINST.setAccessibleName(CONST.INSTRUMENTS_CONNECT_AND_INIT)
        Button_ConnectINST.clicked.connect(self.onClickButton)

        self.Button_Connect = Button_Connect
        self.Button_ConnectINST = Button_ConnectINST
        
        Layout_Inner.addWidget(Button_Connect)
        Layout_Inner.addWidget(Button_ConnectINST)
        
        Layout_Inner2.addWidget(Box3)
        
        Layout_Container.addWidget(BoxButtons)
        Layout_Container.addWidget(TabWidget)
        

        ################ Equipemt Table ################

        FONT = Qt.QFont("Times", 10, Qt.QFont.Serif);

        # Table Heading
        Label_State = QtWidgets.QLabel(CONST.ONOFF, parent)
        Label_State.setAlignment(QtCore.Qt.AlignLeft)
        Label_Name = QtWidgets.QLabel(CONST.NAME, parent)
        Label_Reference = QtWidgets.QLabel(CONST.REFERENCE, parent)
        Label_Reference.setAlignment(QtCore.Qt.AlignHCenter)
        Label_Value = QtWidgets.QLabel(CONST.VALUE, parent)
        Label_Value.setAlignment(QtCore.Qt.AlignHCenter)
        Label_Sync = QtWidgets.QLabel(CONST.SYNC, parent)
        Label_Sync.setAlignment(QtCore.Qt.AlignRight)

        POS = 0;
        GridLayout.addWidget(Label_State, POS, 0)
        GridLayout.addWidget(Label_Name, POS, 1)
        GridLayout.addWidget(Label_Reference, POS, 2)
        GridLayout.addWidget(Label_Value, POS, 3)
        GridLayout.addWidget(Label_Sync, POS, 4)
        POS = POS + 1;

        def createInstrumentGroup_SOURCE(_LABEL, _MAXVAL, _UNIT):
            Label = QtWidgets.QLabel(_LABEL, parent)
            Label.setFont(FONT)
            SpinBox = QtWidgets.QSpinBox()
            SpinBox.setSingleStep(10)
            SpinBox.setRange(0, _MAXVAL)
            SpinBox.setSuffix(_UNIT)
            SpinBox.setAlignment(QtCore.Qt.AlignRight)
            SpinBox.setAccessibleName(_LABEL)
            SpinBox.valueChanged.connect(self.onChangeSpinBox)
            Label_IST = QtWidgets.QLabel("-" + _UNIT, parent)
            Label_IST.setAlignment(QtCore.Qt.AlignHCenter)
            CheckBox_Sync = QtWidgets.QCheckBox("", parent)
            CheckBox_Sync.setAccessibleName(_LABEL + CONST.SYNC)
            CheckBox_Sync.setLayoutDirection(QtCore.Qt.RightToLeft)
            CheckBox_Sync.clicked.connect(self.onChangeCheckBox)
            _POS = POS;

            GridLayout.addWidget(Label, _POS, 1)
            GridLayout.addWidget(SpinBox, _POS, 2)
            GridLayout.addWidget(Label_IST, _POS, 3)
            GridLayout.addWidget(CheckBox_Sync, _POS, 4)
            _POS = _POS + 1;

            return _POS

        POS = createInstrumentGroup_SOURCE(CONST.EQ_VIN, self.MAX_VIN, CONST.UNIT_MV)
        POS = createInstrumentGroup_SOURCE(CONST.EQ_INMAX, self.MAX_IIN, CONST.UNIT_MA)
        POS = createInstrumentGroup_SOURCE(CONST.EQ_Vd, self.MAX_VD, CONST.UNIT_MV)
        POS = createInstrumentGroup_SOURCE(CONST.EQ_IdMAX, self.MAX_ID, CONST.UNIT_MA)
        POS = createInstrumentGroup_SOURCE(CONST.EQ_FREQ_AC, self.MAX_FAC, CONST.UNIT_MV)
        POS = createInstrumentGroup_SOURCE(CONST.EQ_FREQ_DC, self.MAX_FDC, CONST.UNIT_MV)
        POS = createInstrumentGroup_SOURCE(CONST.EQ_FREQ_F, self.MAX_FF, CONST.UNIT_MHZ)

        def createTurnOnBox(_name, _row, _size):
            CheckBox = QtWidgets.QCheckBox("", parent)
            CheckBox.setAccessibleName(_name)
            GridLayout.addWidget(CheckBox, _row, 0, _size, 1)
            CheckBox.clicked.connect(self.onChangeCheckBox)

        createTurnOnBox(CONST.VINon, 1, 2)
        createTurnOnBox(CONST.Vdon, 3, 2)
        createTurnOnBox(CONST.FGon, 5, 3)
        
        
        _POS = 5 + 4;
        createTurnOnBox(CONST.VOuton, _POS, 1)
        Label = QtWidgets.QLabel(CONST.EQ_VOUT, parent)
        Label.setFont(FONT)
        Label_IST = QtWidgets.QLabel("-" + CONST.UNIT_MV, parent)
        Label_IST.setAlignment(QtCore.Qt.AlignHCenter)
        CheckBox_Sync = QtWidgets.QCheckBox("", parent)
        CheckBox_Sync.setAccessibleName(CONST.VOuton + CONST.SYNC)
        CheckBox_Sync.setLayoutDirection(QtCore.Qt.RightToLeft)
        CheckBox_Sync.clicked.connect(self.onChangeCheckBox)

        GridLayout.addWidget(Label, _POS, 1)
        GridLayout.addWidget(Label_IST, _POS, 3)
        GridLayout.addWidget(CheckBox_Sync, _POS, 4)

        gb_Hammerhead = QtWidgets.QGroupBox(CONST.EQUIPMENT)
        gb_Hammerhead.setLayout(Layout_Container)
        gb_Hammerhead.setMaximumWidth(self.WIDTH)
        gb_Hammerhead.setAlignment(QtCore.Qt.AlignHCenter)

        self.GroupBox = gb_Hammerhead
        self.parent = parent
        self.mainLayout = Layout_Inner2
        
        

    def onClickButton(self):

        parent = self.parent
        parent.buttonClicked()  # print out pressed button
        name = parent.sender().accessibleName()
        
        if name == CONST.HAMMERHEAD_CONNECT_AND_INIT:
            self.connectHammerhead(parent.sender())            
        elif name == CONST.INSTRUMENTS_CONNECT_AND_INIT:
            self.connectInstruments(parent.sender())                
        else:
            print(parent.sender().accessibleName())
            
    def connectInstruments(self,button):
    
        parent = self.parent
        button.setEnabled(False);
        button.setText(CONST.CONNECTING)
        
        textList = [CONST.INSTRUMENTS_CONNECT_AND_INIT,CONST.INSTRUMENTS_DISCONNECT]
        fun = self.defineConnCheckFunction(parent.setup,"measSetupInit", button, textList, "isInitialized")
        
        self.PYQT_SIGNAL_INST.connect(fun)
        Thread(target=self.async_connectINST).start()
    
    def connectHammerhead(self, button):

        button.setEnabled(False)
        button.setText(CONST.CONNECTING)
        parent = self.parent
        
        textList = [CONST.HAMMERHEAD_CONNECT_AND_INIT,CONST.HAMMERHEAD_DISCONNECT]
        fun = self.defineConnCheckFunction(parent.h,"isConnected", button, textList, "isConnected")
        self.PYQT_SIGNAL_HH.connect(fun)
        Thread(target=self.async_connectHH).start()        
        
    def defineConnCheckFunction(self,_checkObj,_checkAttr:str, _button:QPushButton, _textList:List[str],_signalFun:str):
        '''
        Defines a function that checks the reult of the asynchronous connection process.
        The "Connect"-Button is updated accordingly and the parent GUI is notified of the (un-)successful
        Connection procedure
        
        :param _checkObj:    The Object on which the Connection Attribute is checked
        :param _checkAttr:   The connection attribute
        :param _button:      The Button which contains the text that is updated 
        :param _textList:    The different Button texts
        :param _signalFun:   The function name which is called on self.parent at the end
        '''
        
        def finishedConnect():
            
            parent = self.parent
            connected = getattr(_checkObj, _checkAttr)
            
            _button.setEnabled(True);
            newtext = _textList[0] 
            if(connected):
                parent.status('Connected')
                newtext = _textList[1]              
            else:
                parent.status('Disconnected')
            
            _button.setText(newtext)
            getattr(parent, _signalFun)(connected)
        
        return finishedConnect
    
    def async_connectHH(self):

        parent = self.parent
        try:
            if parent.h.isConnected:
                parent.h.disconnect()
            else:
                parent.h.connect()
                parent.h.init()
                t = Timer(0.1, self.readLog)
                t.start()
        except Exception as e:
            print(str(e))

        self.PYQT_SIGNAL_HH.emit()
        
        
        
        
    def async_connectINST(self):
        
        setup = self.parent.setup
        try:
            if(setup.measSetupInit):
                setup.closeAllInstr()
            else:
                setup.initAllInstr()
        except Exception as e:
            print(str(e))
        
        self.PYQT_SIGNAL_INST.emit()

    def setEnabled(self, en:bool)->None:
        
        super(EquipmentGui_Class, self).setEnabled(en,[self.Button_Connect,self.Button_ConnectINST])
    
    def readLog(self):
        
        self.parent.h.printTelnetNew()
        self.PYQT_SIGNAL_LOG.emit()
        
        if self.parent.h.isConnected:
            t = Timer(1, self.readLog)
            t.start()
        
        
    
    def updateLog(self):
        
       self.logView.setPlainText(self.parent.h.LOG)
        
    
    