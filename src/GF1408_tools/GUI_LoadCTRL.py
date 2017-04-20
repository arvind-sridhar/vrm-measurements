#!/usr/bin/env python
# -*- coding: utf-8 -*- 
'''
Created on Apr 18, 2017

@author: rid
'''



from PyQt4 import QtGui, QtCore
from GF1408_CONST import CONST
from GF1408_tools import GUI_Parent

class LoadControl_Class(GUI_Parent.GuiTools):
    '''
    classdocs
    '''
    WIDTH = 350
    HEIGHT = 150


    def __init__(self, parent):
        
        super(LoadControl_Class,self).__init__(parent)
        
        CheckBox_ENLOAD = QtGui.QCheckBox(CONST.EN_LOADCTRL,parent) # Enable Clock
        CheckBox_ENLOAD.setAccessibleName(CONST.EN_LOADCTRL)
        CheckBox_LOAD_SLOWCHANGE = QtGui.QCheckBox(CONST.EN_LOADPROG,parent) # Enable LOADPROG
        CheckBox_LOAD_SLOWCHANGE.setAccessibleName(CONST.EN_LOADPROG)
        # Load CLK
        Label_LOADCLK = QtGui.QLabel(CONST.LOADCLK + ":",parent)
        ComboBox_LOADCLK = QtGui.QComboBox(parent)  
        values = QtCore.QStringList()
        values << "CK2" << "CK4" << "CK8" << "CK16";
        ComboBox_LOADCLK.setAccessibleName(CONST.LOADCLK)
        ComboBox_LOADCLK.addItems(values)
        
        
        # Load 
        Label_LOADEN = QtGui.QLabel(CONST.LOADEN + ":",parent)
        SpinBox_LOADEN = QtGui.QSpinBox(parent)
        SpinBox_LOADEN.setMaximumWidth(80)
        SpinBox_LOADEN.setRange(0,CONST.LOAD_BITS)
        SpinBox_LOADEN.setSuffix(CONST.LOAD_UNITS)
        SpinBox_LOADEN.setAccessibleName(parent.BIDI.LOAD_EN.name)
        
        GridLayout = QtGui.QGridLayout();
        GridLayout.addWidget(CheckBox_ENLOAD ,0,0,1,2);
        GridLayout.addWidget(CheckBox_LOAD_SLOWCHANGE ,1,0,1,2);
        GridLayout.addWidget(Label_LOADCLK ,0,2);
        GridLayout.addWidget(ComboBox_LOADCLK ,0,3);
        GridLayout.addWidget(Label_LOADEN ,1,2);
        GridLayout.addWidget(SpinBox_LOADEN ,1,3);
        
        gb_LOAD=QtGui.QGroupBox(CONST.LOADCTRL)
        gb_LOAD.setLayout(GridLayout)
        gb_LOAD.setFixedWidth( self.WIDTH)
        gb_LOAD.setFixedHeight(125)
        gb_LOAD.setAlignment( QtCore.Qt.AlignHCenter )
        # Set Events
        CheckBox_ENLOAD.clicked.connect(self.onChangeCheckBox)
        CheckBox_LOAD_SLOWCHANGE.clicked.connect(self.onChangeCheckBox)
        ComboBox_LOADCLK.activated.connect(self.onChangeComboBox)
        SpinBox_LOADEN.valueChanged.connect(self.onChangeSpinBox)
        
        # Assignments
        self.GroupBox = gb_LOAD
        self.mainLayout = GridLayout
        
       
       
        