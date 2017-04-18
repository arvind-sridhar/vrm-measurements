#!/usr/bin/env python
# -*- coding: utf-8 -*- 

'''
Created on Apr 18, 2017

@author: rid
'''


from PyQt4 import QtGui, QtCore
from GF1408_CONST import *
from xlrd.formula import num2strg

class DPWMControl_Class(object):
    '''
    classdocs
    '''


    def __init__(self, parent):
        '''
        Constructor
        '''
        
        CheckBox_ENDPWM = QtGui.QCheckBox(GF1408_CONST.EN_DPWM,parent) # Enable DPWM
        CheckBox_ENDPWM.setAccessibleName(GF1408_CONST.EN_DPWM)
        CheckBox_RSTDPWM = QtGui.QCheckBox(GF1408_CONST.RST_DPWM,parent) # Reset DPWM
        CheckBox_RSTDPWM.setAccessibleName(GF1408_CONST.RST_DPWM)
        
        Label_DUTY = QtGui.QLabel(GF1408_CONST.DUTY,parent)
        
        BitWidth = GF1408_CONST.DUTY_BITS # Duty Cycle
        Scale_Dec = 2
        DoubleSpinBox_DUTY = QtGui.QDoubleSpinBox(parent)
        DoubleSpinBox_DUTY.setMaximumWidth(80)
        DoubleSpinBox_DUTY.setDecimals(BitWidth-1-Scale_Dec)
        DoubleSpinBox_DUTY.setSingleStep(10**Scale_Dec*2**(-1*(BitWidth-1)))
        DoubleSpinBox_DUTY.setRange(0,10**(Scale_Dec)*(1-2**(-1*(BitWidth-1))))
        DoubleSpinBox_DUTY.setSuffix(' %')
        DoubleSpinBox_DUTY.setAccessibleName(GF1408_CONST.DUTY)
        DoubleSpinBox_DUTY.lineEdit().setReadOnly(True)
        
        
        # Deadtime N and P
        
        DT_SUFFIX = ' ps'
        DT_MAXWIDTH = 80
        def getDTSpinBox(SingleStep,Bits,name):
            SpinBox_DT = QtGui.QSpinBox(parent)
            SpinBox_DT.setMaximumWidth(DT_MAXWIDTH)
            SpinBox_DT.setSingleStep(SingleStep)
            SpinBox_DT.setRange(SingleStep,2**Bits*SingleStep)
            SpinBox_DT.setSuffix(DT_SUFFIX)
            SpinBox_DT.setAccessibleName(name)
            SpinBox_DT.lineEdit().setReadOnly(True)
            return SpinBox_DT
            
            
        SpinBox_DTN = getDTSpinBox(GF1408_CONST.DT_STEP_N, GF1408_CONST.DT_BITS_N, GF1408_CONST.DT_N)
        SpinBox_DTP = getDTSpinBox(GF1408_CONST.DT_STEP_P, GF1408_CONST.DT_BITS_P, GF1408_CONST.DT_P)
        
        Label_DTN = QtGui.QLabel(GF1408_CONST.DT_N + ":",parent)
        Label_DTP = QtGui.QLabel(GF1408_CONST.DT_P+ ":",parent)
        
        CheckBox_ENPHASES = QtGui.QCheckBox(GF1408_CONST.EN_ALLPHASES,parent) # Enable all phases
        CheckBox_ENPHASES.setAccessibleName(GF1408_CONST.EN_ALLPHASES)
        # EN_PHASE
        def getEN_PHASE(name):
            CheckBox_ENPHx = QtGui.QCheckBox(name,parent) 
            CheckBox_ENPHx.setAccessibleName(name+'_EN')
            ComboBox_ENPHx = QtGui.QComboBox(parent)
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
            CheckBox_ENPHx.clicked.connect(parent.onChangeCheckBox)
            ComboBox_ENPHx.activated.connect(parent.onChangeComboBox)
          
        # Set bindings for buttons
        AllButtons = [CheckBox_ENDPWM, CheckBox_RSTDPWM,CheckBox_ENPHASES,DoubleSpinBox_DUTY,SpinBox_DTN,SpinBox_DTP ]
        for button in AllButtons:
            if isinstance(button, QtGui.QCheckBox):
                button.clicked.connect(parent.onChangeCheckBox)
            if hasattr(button, 'valueChanged'):
                button.valueChanged.connect(parent.onChangeSpinBox)
        
        gb_DPWM=QtGui.QGroupBox(GF1408_CONST.DPWM)
        gb_DPWM.setLayout(GridLayout)
        gb_DPWM.setFixedWidth(175)
        gb_DPWM.setFixedHeight(280)
        
        self.GroupBox = gb_DPWM
    