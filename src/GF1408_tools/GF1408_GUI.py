#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Apr 12, 2017

@author: rid
'''

from PyQt5 import QtWidgets, QtCore
from xlrd.formula import num2strg

from GF1408_tools.BIDI_REGISTERS import BIDI_REGISTERS
from GF1408_tools.GF1408_CONST import *
from GF1408_tools.GUI_DPWM import DPWMControl_Class
from GF1408_tools.GUI_Equipment import EquipmentGui_Class
from GF1408_tools.GUI_LoadCTRL import LoadControl_Class


class GF1408_GUI(QtWidgets.QMainWindow):

    WINDOW_SIZE = (370, 725)
    WINDOW_NAME = 'CarrICool GF1408 - Control Window'

    PYQT_SIGNAL = QtCore.pyqtSignal()

    def __init__(self, _BIDI:BIDI_REGISTERS, _hammerhead):
        super(GF1408_GUI, self).__init__()
        
        self.h = _hammerhead
        self.BIDI = _BIDI
        self.initUI()

    def initUI(self):
    
        vMainBox, vMainLayout = self.addVWidget()
        self.setCentralWidget(vMainBox)
        vMainLayout.addWidget(self.getGUIElements())
        vMainLayout.layout().setContentsMargins(10, 10, 10, 10)

        # Init Window
        self.statusBar()
        self.setGeometry(50, 50, self.WINDOW_SIZE[0], self.WINDOW_SIZE[1])
        self.setFixedSize(self.WINDOW_SIZE[0], self.WINDOW_SIZE[1])
        # self.setFixedSize(vMainLayout.layout().sizeHint() )

        self.setWindowTitle(self.WINDOW_NAME)
        self.show()

    def getGUIElements(self):

        v0Box, v0Layout = self.addVWidget()

        self.Load_GUI = LoadControl_Class(self)
        self.HammerHead_GUI = EquipmentGui_Class(self)
        self.DPWM_GUI = DPWMControl_Class(self)

        # TODO: remove comment
        # self.DPWM_GUI.setEnabled(False)
        # self.Load_GUI.setEnabled(False)

        v0Layout.addWidget(self.HammerHead_GUI.GroupBox)
        v0Layout.addWidget(self.DPWM_GUI.GroupBox)
        v0Layout.addWidget(self.Load_GUI.GroupBox)
        return v0Box

    def addVWidget(self):
        Box = QtWidgets.QWidget()
        Layout = QtWidgets.QVBoxLayout()
        Box.setLayout(Layout)
        Box.setContentsMargins(QtCore.QMargins(0, 0, 0, 0))
        Layout.layout().setContentsMargins(0, 0, 0, 0)
        return Box, Layout

    def addHWidget(self):
        Box = QtWidgets.QWidget()
        Layout = QtWidgets.QHBoxLayout()
        Box.setLayout(Layout)
        Box.setContentsMargins(QtCore.QMargins(0, 0, 0, 0))
        Layout.layout().setContentsMargins(0, 0, 0, 0)
        return Box, Layout

    def buttonClicked(self):
        sender = self.sender()
        self.statusBar().showMessage(sender.text() + ' was pressed')

    def status(self, text:str) -> None:
        self.statusBar().showMessage(text)

    def onClickButton(self):

        self.buttonClicked()  # print out pressed button
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
        self.statusBar().showMessage(sender.accessibleName() + ' was changed to ' + num2strg(sender.isChecked()))


    def closeEvent (self, eventQCloseEvent):
        answer = QtWidgets.QMessageBox.question (
            self,
            'Exit',
            'Are you sure you want to quit ?',
            QtWidgets.QMessageBox.Yes,
            QtWidgets.QMessageBox.No)
        if (answer == QtWidgets.QMessageBox.Yes) or (False):
            self.h.disconnect()
            eventQCloseEvent.accept()
        else:
            eventQCloseEvent.ignore()

    def isConnected(self, connected:bool):
        self.DPWM_GUI.setEnabled(connected)
        self.Load_GUI.setEnabled(connected)
