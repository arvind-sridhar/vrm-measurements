#!/usr/bin/env python
# -*- coding: utf-8 -*- 

'''
Created on Apr 12, 2017

@author: rid
'''


from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *

from threading import Thread
from GF1408_tools import GF1408_BIDI


import hammerhead
from xlrd.formula import num2strg
import xlwt



class GF1408_CONST():
    HAMMERHEAD_CONNECT  = "Connect"
    HAMMERHEAD_INIT     = "Init"
    EXIT = "Exit"
    DPWM = "DPWM Control"
    EN_DPWM = "Enable DPWM"
    RST_DPWM = "Reset DPWM"
    DUTY = "Duty Cycle"
    DT_N = "D-Time(N)"
    DT_P = "D-Time(P)"
    PHASE = "Phase"
    SHIFT = "Shift"
    EN_ALLPHASES = "Enable all phases"
    
    DUTY_BITS = 5
    DT_BITS_N = 3
    DT_BITS_P = 3
    DT_STEP_N = 100 #ps
    DT_STEP_P = 100 #ps
    # TODO: Confirm deadtime
    
    LOADCTRL = "Load Control"
    EN_LOADCTRL = "Load clock enable"
    EN_LOADPROG = "Slow change"
    LOADCLK = "Load clock"
    LOADEN = "Set Load"
    # TODO: Confirm Load unit
    LOAD_BITS = 32
    LOAD_UNITS = u' × 13Ω'

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
        
        self.statusBar()
        self.setGeometry( 25, 20,self.WINDOW_SIZE[0],self.WINDOW_SIZE[1])
        
        
        self.setFixedSize(self.WINDOW_SIZE[0],self.WINDOW_SIZE[1])
        self.setWindowTitle(self.WINDOW_NAME)
        self.show()
    
    def initButtons(self):
        v0Box, v0Layout = self.addVWidget()
                
        DPWMBox = self.getDPWMBox()
            
        h0Box, h0Layout = self.addHWidget()
        v0Layout.addWidget(h0Box)          
        h0Layout.addWidget(self.getHammerHeadBox())
        h0Layout.addWidget(self.getDPWMBox())
        h0Layout.addWidget(self.getLoadBox())
         
        v0Box.setMaximumHeight(275)
        #v0Box.setMaximumWidth(100)
        return v0Box        
    
    def getHammerHeadBox(self):
        
        btnConnectHammerhead = QtGui.QPushButton(GF1408_CONST.HAMMERHEAD_CONNECT, self)
        btnConnectHammerhead.clicked.connect(self.onClickButton)
        btnConnectHammerhead.setFixedSize(75,28)

        btnInitHammerhead = QtGui.QPushButton(GF1408_CONST.HAMMERHEAD_INIT, self)
        btnInitHammerhead.clicked.connect(self.onClickButton)
        btnInitHammerhead.setFixedSize(75,28)
        btnInitHammerhead.setEnabled(True);
        
        
        # Make Instance accessible
        self.btnConnectHammerhead = btnConnectHammerhead;
        self.btnInitHammerhead = btnInitHammerhead;
        
        box = QVBoxLayout();
        box.addWidget(btnConnectHammerhead);
        box.addWidget(btnInitHammerhead);
        box.addStretch(1);
        
        gb_Hammerhead=QtGui.QGroupBox('Hammerhead')
        gb_Hammerhead.setLayout(box)
        gb_Hammerhead.setMaximumWidth(100)
        gb_Hammerhead.setFixedHeight(100)
        
        return gb_Hammerhead
    
    def getDPWMBox(self):
        
        CheckBox_ENDPWM = QtGui.QCheckBox(GF1408_CONST.EN_DPWM,self) # Enable DPWM
        CheckBox_ENDPWM.setAccessibleName(GF1408_CONST.EN_DPWM)
        CheckBox_RSTDPWM = QtGui.QCheckBox(GF1408_CONST.RST_DPWM,self) # Reset DPWM
        CheckBox_RSTDPWM.setAccessibleName(GF1408_CONST.RST_DPWM)
        
        Label_DUTY = QtGui.QLabel(GF1408_CONST.DUTY,self)
        
        BitWidth = GF1408_CONST.DUTY_BITS # Duty Cycle
        Scale_Dec = 2
        DoubleSpinBox_DUTY = QtGui.QDoubleSpinBox(self)
        DoubleSpinBox_DUTY.setMaximumWidth(80)
        DoubleSpinBox_DUTY.setDecimals(BitWidth-1-Scale_Dec)
        DoubleSpinBox_DUTY.setSingleStep(10**Scale_Dec*2**(-1*(BitWidth-1)))
        DoubleSpinBox_DUTY.setRange(0,10**(Scale_Dec)*(1-2**(-1*(BitWidth-1))))
        DoubleSpinBox_DUTY.setSuffix(' %')
        DoubleSpinBox_DUTY.setAccessibleName(GF1408_CONST.DUTY)
        
        # Deadtime N and P
        
        DT_SUFFIX = ' ps'
        DT_MAXWIDTH = 80
        def getDTSpinBox(SingleStep,Bits,name):
            SpinBox_DT = QtGui.QSpinBox(self)
            SpinBox_DT.setMaximumWidth(DT_MAXWIDTH)
            SpinBox_DT.setSingleStep(SingleStep)
            SpinBox_DT.setRange(SingleStep,2**Bits*SingleStep)
            SpinBox_DT.setSuffix(DT_SUFFIX)
            SpinBox_DT.setAccessibleName(name)
            return SpinBox_DT
            
            
        SpinBox_DTN = getDTSpinBox(GF1408_CONST.DT_STEP_N, GF1408_CONST.DT_BITS_N, GF1408_CONST.DT_N)
        SpinBox_DTP = getDTSpinBox(GF1408_CONST.DT_STEP_P, GF1408_CONST.DT_BITS_P, GF1408_CONST.DT_P)
        
        Label_DTN = QtGui.QLabel(GF1408_CONST.DT_N + ":",self)
        Label_DTP = QtGui.QLabel(GF1408_CONST.DT_P+ ":",self)
        
        CheckBox_ENPHASES = QtGui.QCheckBox(GF1408_CONST.EN_ALLPHASES,self) # Enable all phases
        CheckBox_ENPHASES.setAccessibleName(GF1408_CONST.EN_ALLPHASES)
        # EN_PHASE
        def getEN_PHASE(name):
            CheckBox_ENPHx = QtGui.QCheckBox(name,self) 
            CheckBox_ENPHx.setAccessibleName(name+'_EN')
            ComboBox_ENPHx = QtGui.QComboBox(self)
            values = QtCore.QStringList()
            values << u"0°" << u"90°" << u"180°" << u"270°";
            ComboBox_ENPHx.setAccessibleName(name+'_SHIFT')
            ComboBox_ENPHx.addItems(values)
            return CheckBox_ENPHx,ComboBox_ENPHx
        
        
        # Grid Layout Positioning
        GridLayout = QtGui.QGridLayout();
        
        GridLayout.addWidget(CheckBox_ENDPWM ,0,0,1,2)
        GridLayout.addWidget(CheckBox_RSTDPWM,1,0,1,2)
        GridLayout.addWidget(Label_DUTY,2,0 )
        GridLayout.addWidget(DoubleSpinBox_DUTY,2,1 )
        GridLayout.addWidget(Label_DTN,9,0 )
        GridLayout.addWidget(Label_DTP,10,0 )
        GridLayout.addWidget(SpinBox_DTN,9,1 )
        GridLayout.addWidget(SpinBox_DTP,10,1 )
        GridLayout.addWidget(CheckBox_ENPHASES,3,0,1,2 )
        start_EN = 5
        for phase in range(1,5):
            CheckBox_ENPHx,ComboBox_ENPHx = getEN_PHASE(GF1408_CONST.PHASE +' '+ num2strg(phase))
            GridLayout.addWidget(CheckBox_ENPHx,start_EN+phase-1,0 )
            GridLayout.addWidget(ComboBox_ENPHx,start_EN+phase-1,1 )
            CheckBox_ENPHx.clicked.connect(self.onChangeCheckBox)
            ComboBox_ENPHx.activated.connect(self.onChangeComboBox)
          
        # Set bindings for buttons
        AllButtons = [CheckBox_ENDPWM, CheckBox_RSTDPWM,CheckBox_ENPHASES,DoubleSpinBox_DUTY,SpinBox_DTN,SpinBox_DTP ]
        for button in AllButtons:
            if isinstance(button, QtGui.QCheckBox):
                button.clicked.connect(self.onChangeCheckBox)
            if hasattr(button, 'valueChanged'):
                button.valueChanged.connect(self.onChangeSpinBox)
        
        gb_DPWM=QtGui.QGroupBox(GF1408_CONST.DPWM)
        gb_DPWM.setLayout(GridLayout)
        gb_DPWM.setFixedWidth(175)
        gb_DPWM.setFixedHeight(280)
        
        return gb_DPWM
    
    def getLoadBox(self):
        
        CheckBox_ENLOAD = QtGui.QCheckBox(GF1408_CONST.EN_LOADCTRL,self) # Enable Clock
        CheckBox_ENLOAD.setAccessibleName(GF1408_CONST.EN_LOADCTRL)
        CheckBox_LOAD_SLOWCHANGE = QtGui.QCheckBox(GF1408_CONST.EN_LOADPROG,self) # Enable LOADPROG
        CheckBox_LOAD_SLOWCHANGE.setAccessibleName(GF1408_CONST.EN_LOADPROG)
        # Load CLK
        Label_LOADCLK = QtGui.QLabel(GF1408_CONST.LOADCLK + ":",self)
        ComboBox_LOADCLK = QtGui.QComboBox(self)  
        values = QtCore.QStringList()
        values << "CK2" << "CK4" << "CK8" << "CK16";
        ComboBox_LOADCLK.setAccessibleName(GF1408_CONST.LOADCLK)
        ComboBox_LOADCLK.addItems(values)
        
        
        # Load Itself
        Label_LOADEN = QtGui.QLabel(GF1408_CONST.LOADEN + ":",self)
        SpinBox_LOADEN = QtGui.QSpinBox(self)
        SpinBox_LOADEN.setMaximumWidth(80)
        SpinBox_LOADEN.setRange(0,GF1408_CONST.LOAD_BITS-1)
        SpinBox_LOADEN.setSuffix(GF1408_CONST.LOAD_UNITS)
        SpinBox_LOADEN.setAccessibleName(GF1408_CONST.LOADEN)
        
        GridLayout = QtGui.QGridLayout();
        GridLayout.addWidget(CheckBox_ENLOAD ,0,0,1,2);
        GridLayout.addWidget(CheckBox_LOAD_SLOWCHANGE ,1,0,1,2);
        GridLayout.addWidget(Label_LOADCLK ,2,0);
        GridLayout.addWidget(ComboBox_LOADCLK ,2,1);
        GridLayout.addWidget(Label_LOADEN ,3,0);
        GridLayout.addWidget(SpinBox_LOADEN ,3,1);
        
        gb_LOAD=QtGui.QGroupBox(GF1408_CONST.LOADCTRL)
        gb_LOAD.setLayout(GridLayout)
        gb_LOAD.setFixedWidth(175)
        gb_LOAD.setFixedHeight(125)
        
        # Set Events
        CheckBox_ENLOAD.clicked.connect(self.onChangeCheckBox)
        CheckBox_LOAD_SLOWCHANGE.clicked.connect(self.onChangeCheckBox)
        ComboBox_LOADCLK.activated.connect(self.onChangeComboBox)
        SpinBox_LOADEN.valueChanged.connect(self.onChangeSpinBox)
        
        return gb_LOAD
    
    def addVWidget(self):
        Box = QWidget()
        Layout = QVBoxLayout()
        Box.setLayout(Layout)
        Box.setContentsMargins(QtCore.QMargins(0, 0, 0, 0))
        Layout.layout().setContentsMargins(0, 0, 0, 0)
        return Box, Layout   
    
    def addHWidget(self):
        Box = QWidget()
        Layout = QHBoxLayout()
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
        
        '''
        try: 
            self.allOff()
        except Exception as e:
            self.status('Fail 1')
        '''
        
        if self.sender().text() == GF1408_CONST.HAMMERHEAD_CONNECT:
                self.connectHammerhead() 
        
        try:
            '''
            self.devices = devices.Devices()
            self.devices.printInstrList()
            self.addr0 = '-'
            self.addr1 = '-'
            self.addr2 = '-'
            self.hammerheadIsInitialized = False
            '''
            
              
            if self.sender().text() == GF1408_CONST.HAMMERHEAD_INIT:
                self.initHammerhead()                   
            if self.sender().text() == GF1408_CONST.EXIT:
                self.close() 

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
      
    def connectHammerhead(self):
        
        self.btnConnectHammerhead.setEnabled(False);
           
        def async_connectHH():
            try:
                self.h.connect()
            except Exception as e:
                print(str(e))
            self.PYQT_SIGNAL.emit()
        
        def finishedConnect():
            self.btnConnectHammerhead.setEnabled( not self.h.isConnected);
            self.status('Fail' )
             
        self.PYQT_SIGNAL.connect(finishedConnect)
        Thread(target=async_connectHH).start() 

        
    