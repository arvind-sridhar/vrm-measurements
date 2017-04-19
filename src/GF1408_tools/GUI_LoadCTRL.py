#!/usr/bin/env python
# -*- coding: utf-8 -*- 
'''
Created on Apr 18, 2017

@author: rid
'''



from PyQt4 import QtGui, QtCore
from GF1408_CONST import *
from GF1408_tools import GUI_Parent

class LoadControl_Class(GUI_Parent.GuiTools):
    '''
    classdocs
    '''
    

    def __init__(self, parent):
        
        super(LoadControl_Class,self).__init__(parent)
        
        CheckBox_ENLOAD = QtGui.QCheckBox(GF1408_CONST.EN_LOADCTRL,parent) # Enable Clock
        CheckBox_ENLOAD.setAccessibleName(GF1408_CONST.EN_LOADCTRL)
        CheckBox_LOAD_SLOWCHANGE = QtGui.QCheckBox(GF1408_CONST.EN_LOADPROG,parent) # Enable LOADPROG
        CheckBox_LOAD_SLOWCHANGE.setAccessibleName(GF1408_CONST.EN_LOADPROG)
        # Load CLK
        Label_LOADCLK = QtGui.QLabel(GF1408_CONST.LOADCLK + ":",parent)
        ComboBox_LOADCLK = QtGui.QComboBox(parent)  
        values = QtCore.QStringList()
        values << "CK2" << "CK4" << "CK8" << "CK16";
        ComboBox_LOADCLK.setAccessibleName(GF1408_CONST.LOADCLK)
        ComboBox_LOADCLK.addItems(values)
        
        
        # Load 
        Label_LOADEN = QtGui.QLabel(GF1408_CONST.LOADEN + ":",parent)
        SpinBox_LOADEN = QtGui.QSpinBox(parent)
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
        CheckBox_ENLOAD.clicked.connect(parent.onChangeCheckBox)
        CheckBox_LOAD_SLOWCHANGE.clicked.connect(parent.onChangeCheckBox)
        ComboBox_LOADCLK.activated.connect(parent.onChangeComboBox)
        SpinBox_LOADEN.valueChanged.connect(parent.onChangeSpinBox)
        
        # Assignments
        self.GroupBox = gb_LOAD
        self.mainLayout = GridLayout