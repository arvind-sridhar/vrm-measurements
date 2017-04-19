#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Apr 18, 2017

@author: rid
'''


from GF1408_CONST import CONST
from GUI_Parent import GuiTools
from PyQt4 import QtGui, QtCore
from xlrd.formula import num2strg


class DPWMControl_Class( GuiTools ):
    '''
    classdocs
    '''
    WIDTH = 350
    HEIGHT = 150

    def __init__( self, parent ):
        '''
        Constructor
        '''
        super( DPWMControl_Class, self ).__init__( parent )
        CheckBox_ENDPWM = QtGui.QCheckBox( CONST.EN_DPWM, parent )  # Enable DPWM
        CheckBox_ENDPWM.setAccessibleName( CONST.EN_DPWM )
        CheckBox_RSTDPWM = QtGui.QCheckBox( CONST.RST_DPWM, parent )  # Reset DPWM
        CheckBox_RSTDPWM.setAccessibleName( CONST.RST_DPWM )

        Label_DUTY = QtGui.QLabel( CONST.DUTY, parent )

        BitWidth = CONST.DUTY_BITS  # Duty Cycle
        Scale_Dec = 2
        DoubleSpinBox_DUTY = QtGui.QDoubleSpinBox( parent )
        DoubleSpinBox_DUTY.setMaximumWidth( 80 )
        DoubleSpinBox_DUTY.setDecimals( BitWidth - 1 - Scale_Dec )
        DoubleSpinBox_DUTY.setSingleStep( 10 ** Scale_Dec * 2 ** ( -1 * ( BitWidth - 1 ) ) )
        DoubleSpinBox_DUTY.setRange( 0, 10 ** ( Scale_Dec ) * ( 1 - 2 ** ( -1 * ( BitWidth - 1 ) ) ) )
        DoubleSpinBox_DUTY.setSuffix( ' %' )
        DoubleSpinBox_DUTY.setAccessibleName( CONST.DUTY )
        DoubleSpinBox_DUTY.lineEdit().setReadOnly( True )


        # Deadtime N and P

        DT_SUFFIX = ' ps'
        DT_MAXWIDTH = 80
        def getDTSpinBox( SingleStep, Bits, name ):
            SpinBox_DT = QtGui.QSpinBox( parent )
            SpinBox_DT.setMaximumWidth( DT_MAXWIDTH )
            SpinBox_DT.setSingleStep( SingleStep )
            SpinBox_DT.setRange( SingleStep, 2 ** Bits * SingleStep )
            SpinBox_DT.setSuffix( DT_SUFFIX )
            SpinBox_DT.setAccessibleName( name )
            SpinBox_DT.lineEdit().setReadOnly( True )
            return SpinBox_DT


        SpinBox_DTN = getDTSpinBox( CONST.DT_STEP_N, CONST.DT_BITS_N, CONST.DT_N )
        SpinBox_DTP = getDTSpinBox( CONST.DT_STEP_P, CONST.DT_BITS_P, CONST.DT_P )

        Label_DTN = QtGui.QLabel( CONST.DT_N + ":", parent )
        Label_DTP = QtGui.QLabel( CONST.DT_P + ":", parent )

        CheckBox_ENPHASES = QtGui.QCheckBox( CONST.EN_ALLPHASES, parent )  # Enable all phases
        CheckBox_ENPHASES.setAccessibleName( CONST.EN_ALLPHASES )
        # EN_PHASE
        def getEN_PHASE( name ):
            CheckBox_ENPHx = QtGui.QCheckBox( name, parent )
            CheckBox_ENPHx.setAccessibleName( name + '_EN' )
            ComboBox_ENPHx = QtGui.QComboBox( parent )
            values = QtCore.QStringList()
            values << u"0°" << u"90°" << u"180°" << u"270°";
            ComboBox_ENPHx.setAccessibleName( name + '_SHIFT' )
            ComboBox_ENPHx.addItems( values )
            return CheckBox_ENPHx, ComboBox_ENPHx

        
        start_EN = 1
        colPadd = 3
        # Grid Layout Positioning
        GridLayout = QtGui.QGridLayout();

        GridLayout.addWidget( CheckBox_ENDPWM , 0, 0, 1, 2 )
        GridLayout.addWidget( CheckBox_RSTDPWM, 1, 0, 1, 2 )
        GridLayout.addWidget( Label_DUTY, 2, 0 )
        GridLayout.addWidget( DoubleSpinBox_DUTY, 2, 1 )
        GridLayout.addWidget( Label_DTN, 3, 0 )
        GridLayout.addWidget( Label_DTP, 4, 0 )
        GridLayout.addWidget( SpinBox_DTN, 3, 1 )
        GridLayout.addWidget( SpinBox_DTP, 4, 1 )
        GridLayout.addWidget( CheckBox_ENPHASES, start_EN-1, 0+colPadd, 1, 2 )


        
        self.CheckBox_ENPH = [None] * 4
        self.ComboBox_ENPH = [None] * 4
        for phase in range( 1, 5 ):
            CheckBox_ENPHx, ComboBox_ENPHx = getEN_PHASE( CONST.PHASE + ' ' + num2strg( phase ) )
            GridLayout.addWidget( CheckBox_ENPHx, start_EN + phase - 1, 0+colPadd )
            GridLayout.addWidget( ComboBox_ENPHx, start_EN + phase - 1, 1+colPadd )
            CheckBox_ENPHx.clicked.connect( self.onChangeCheckBox )
            ComboBox_ENPHx.activated.connect( self.onChangeComboBox )
            self.CheckBox_ENPH[phase - 1] = CheckBox_ENPHx
            self.ComboBox_ENPH[phase - 1] = ComboBox_ENPHx

        # Set bindings for buttons
        AllButtons = [CheckBox_ENDPWM, CheckBox_RSTDPWM, CheckBox_ENPHASES, DoubleSpinBox_DUTY, SpinBox_DTN, SpinBox_DTP ]
        for button in AllButtons:
            if isinstance( button, QtGui.QCheckBox ):
                button.clicked.connect( self.onChangeCheckBox )
            if hasattr( button, 'valueChanged' ):
                button.valueChanged.connect( self.onChangeSpinBox )

        gb_DPWM = QtGui.QGroupBox( CONST.DPWM )
        gb_DPWM.setLayout( GridLayout )
        gb_DPWM.setFixedWidth( self.WIDTH )
        #gb_DPWM.setFixedHeight( self.HEIGHT )
        gb_DPWM.setAlignment( QtCore.Qt.AlignHCenter )
        
        self.GroupBox = gb_DPWM
        self.mainLayout = GridLayout
