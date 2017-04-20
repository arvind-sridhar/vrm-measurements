#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on Apr 18, 2017

@author: rid
'''

from threading import Thread

from PyQt5 import QtWidgets, QtCore, Qt

from GF1408_tools.GF1408_CONST import CONST
from GF1408_tools.GUI_Parent import GuiTools


class EquipmentGui_Class( GuiTools ):
    '''
    classdocs
    '''

    WIDTH = 350
    HEIGHT = 300

    MAX_VIN = 1600  # mV
    MAX_IIN = 200  # mA
    MAX_VD = 800
    MAX_ID = 250
    MAX_FAC = 800
    MAX_FDC = 0.0
    MAX_FF = 8000

    def __init__( self, parent ):

        Layout1 = QtWidgets.QVBoxLayout()
        Layout_Inner = QtWidgets.QHBoxLayout()

        GridLayout = QtWidgets.QGridLayout();

        Box = QtWidgets.QWidget()
        Box.setLayout( Layout_Inner )
        Box.setContentsMargins( QtCore.QMargins( 0, 0, 0, 0 ) )
        Layout_Inner.layout().setContentsMargins( 0, 0, 0, 0 )

        Box2 = QtWidgets.QWidget()
        Box2.setLayout( GridLayout )
        Box2.setContentsMargins( QtCore.QMargins( 0, 0, 0, 0 ) )


        # Connect and Init Hammerhead
        Button_Connect = QtWidgets.QPushButton( CONST.HAMMERHEAD_CONNECT_AND_INIT, parent )
        Button_Connect.setAccessibleName( CONST.HAMMERHEAD_CONNECT_AND_INIT )
        Button_Connect.clicked.connect( self.onClickButton )

        Button_ConnectINST = QtWidgets.QPushButton( CONST.INSTRUMENTS_CONNECT_AND_INIT, parent )
        Button_ConnectINST.setAccessibleName( CONST.INSTRUMENTS_CONNECT_AND_INIT )
        Button_ConnectINST.clicked.connect( self.onClickButton )

        Layout_Inner.addWidget( Button_Connect )
        Layout_Inner.addWidget( Button_ConnectINST )
        Layout1.addWidget( Box )
        Layout1.addWidget( Box2 )

        ################ Equipemt Table ################

        FONT = Qt.QFont( "Times", 10, Qt.QFont.Serif );

        # Table Heading
        Label_State = QtWidgets.QLabel( CONST.ONOFF, parent )
        Label_State.setAlignment( QtCore.Qt.AlignLeft )
        Label_Name = QtWidgets.QLabel( CONST.NAME, parent )
        Label_Reference = QtWidgets.QLabel( CONST.REFERENCE, parent )
        Label_Reference.setAlignment( QtCore.Qt.AlignHCenter )
        Label_Value = QtWidgets.QLabel( CONST.VALUE, parent )
        Label_Value.setAlignment( QtCore.Qt.AlignHCenter )
        Label_Sync = QtWidgets.QLabel( CONST.SYNC, parent )
        Label_Sync.setAlignment( QtCore.Qt.AlignRight )

        POS = 0;
        GridLayout.addWidget( Label_State, POS, 0 )
        GridLayout.addWidget( Label_Name, POS, 1 )
        GridLayout.addWidget( Label_Reference, POS, 2 )
        GridLayout.addWidget( Label_Value, POS, 3 )
        GridLayout.addWidget( Label_Sync, POS, 4 )
        POS = POS + 1;

        def createInstrumentGroup_SOURCE( _LABEL, _MAXVAL, _UNIT ):
            Label = QtWidgets.QLabel( _LABEL, parent )
            Label.setFont( FONT )
            SpinBox = QtWidgets.QSpinBox()
            SpinBox.setSingleStep( 10 )
            SpinBox.setRange( 0, _MAXVAL )
            SpinBox.setSuffix( _UNIT )
            SpinBox.setAlignment( QtCore.Qt.AlignRight )
            SpinBox.setAccessibleName( _LABEL )
            SpinBox.valueChanged.connect( self.onChangeSpinBox )
            Label_IST = QtWidgets.QLabel( "-" + _UNIT, parent )
            Label_IST.setAlignment( QtCore.Qt.AlignHCenter )
            CheckBox_Sync = QtWidgets.QCheckBox( "", parent )
            CheckBox_Sync.setAccessibleName( _LABEL + CONST.SYNC )
            CheckBox_Sync.setLayoutDirection( QtCore.Qt.RightToLeft )
            CheckBox_Sync.clicked.connect( self.onChangeCheckBox )
            _POS = POS;

            GridLayout.addWidget( Label, _POS, 1 )
            GridLayout.addWidget( SpinBox, _POS, 2 )
            GridLayout.addWidget( Label_IST, _POS, 3 )
            GridLayout.addWidget( CheckBox_Sync, _POS, 4 )
            _POS = _POS + 1;

            return _POS

        POS = createInstrumentGroup_SOURCE( CONST.EQ_VIN, self.MAX_VIN, CONST.UNIT_MV )
        POS = createInstrumentGroup_SOURCE( CONST.EQ_INMAX, self.MAX_IIN, CONST.UNIT_MA )
        POS = createInstrumentGroup_SOURCE( CONST.EQ_Vd, self.MAX_VD, CONST.UNIT_MV )
        POS = createInstrumentGroup_SOURCE( CONST.EQ_IdMAX, self.MAX_ID, CONST.UNIT_MA )
        POS = createInstrumentGroup_SOURCE( CONST.EQ_FREQ_AC, self.MAX_FAC, CONST.UNIT_MV )
        POS = createInstrumentGroup_SOURCE( CONST.EQ_FREQ_DC, self.MAX_FDC, CONST.UNIT_MV )
        POS = createInstrumentGroup_SOURCE( CONST.EQ_FREQ_F, self.MAX_FF, CONST.UNIT_MHZ )

        def createTurnOnBox( _name, _row, _size ):
            CheckBox = QtWidgets.QCheckBox( "", parent )
            CheckBox.setAccessibleName( _name )
            GridLayout.addWidget( CheckBox, _row, 0, _size, 1 )
            CheckBox.clicked.connect( self.onChangeCheckBox )

        createTurnOnBox( CONST.VINon, 1, 2 )
        createTurnOnBox( CONST.Vdon, 3, 2 )
        createTurnOnBox( CONST.FGon, 5, 3 )


        _POS = 5 + 4;
        createTurnOnBox( CONST.VOuton, _POS, 1 )
        Label = QtWidgets.QLabel( CONST.EQ_VOUT, parent )
        Label.setFont( FONT )
        Label_IST = QtWidgets.QLabel( "-" + CONST.UNIT_MV, parent )
        Label_IST.setAlignment( QtCore.Qt.AlignHCenter )
        CheckBox_Sync = QtWidgets.QCheckBox( "", parent )
        CheckBox_Sync.setAccessibleName( CONST.VOuton + CONST.SYNC )
        CheckBox_Sync.setLayoutDirection( QtCore.Qt.RightToLeft )
        CheckBox_Sync.clicked.connect( self.onChangeCheckBox )

        GridLayout.addWidget( Label, _POS, 1 )
        GridLayout.addWidget( Label_IST, _POS, 3 )
        GridLayout.addWidget( CheckBox_Sync, _POS, 4 )

        gb_Hammerhead = QtWidgets.QGroupBox( CONST.EQUIPMENT )
        gb_Hammerhead.setLayout( Layout1 )
        gb_Hammerhead.setMaximumWidth( self.WIDTH )
        gb_Hammerhead.setAlignment( QtCore.Qt.AlignHCenter )

        self.GroupBox = gb_Hammerhead
        self.parent = parent

    def onClickButton( self ):

        parent = self.parent
        parent.buttonClicked()  # print out pressed button

        '''
        try: 
            self.allOff()
        except Exception as e:
            self.status('Fail 1')
        '''

        if parent.sender().accessibleName() == CONST.HAMMERHEAD_CONNECT_AND_INIT:
            self.connectHammerhead( parent.sender() )

        try:
            if parent.sender().text() == CONST.HAMMERHEAD_INIT:
                self.initHammerhead()
            if parent.sender().text() == CONST.EXIT:
                self.close()

        except Exception as e:
            print( str( e ) )

    def connectHammerhead( self, button ):

        button.setEnabled( False );
        parent = self.parent
        connected = parent.h.isConnected

        def finishedConnect():

            button.setEnabled( True );
            if( connected ):
                parent.status( 'Connected' )
                newtext = CONST.HAMMERHEAD_DISCONNECT
            else:
                parent.status( 'Disconnected' )
                newtext = CONST.HAMMERHEAD_CONNECT_AND_INIT

            button.setText( newtext )

        parent.PYQT_SIGNAL.connect( finishedConnect )
        Thread( target = self.async_connectHH ).start()
        parent.isConnected( connected )

    def async_connectHH( self ):

        parent = self.parent
        try:
            if parent.h.isConnected:
                parent.h.disconnect()
            else:
                parent.h.connect()
                parent.h.init()
        except Exception as e:
            print( str( e ) )

        parent.PYQT_SIGNAL.emit()


