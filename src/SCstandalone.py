#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
GUI to measure on-chip switched capacitor converter. Designed for stand alone converter on the emerald test site 
Toke Meyer Andersen, April 2013
"""

import sys, os
import hammerhead#
# import mplCanvas
# from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
import numpy as np
from PyQt4 import QtGui, QtCore

from PyQt4.QtGui import *
import xlwt
import xlrd
#from PyQt4.QtCore import *
import time
import subprocess

import hp
import agilent
import keithley
import agilentDC
import devices
#import keithleyOut

class prettyfloat(float):
    def __repr__(self):
        return "%0.2f" % self
    
    
def f3(x):
    return '{:.3f}'.format(x)
def f2(x):
    return '{:.2f}'.format(x)
def f1(x):
    return '{:.1f}'.format(x)
def f0(x):
    return '{:.0f}'.format(x)

class SCmeas(QtGui.QMainWindow):
    
    def __init__(self):
        super(SCmeas, self).__init__()
        self.AREA = 8.6347e-003 # (0.2594mm x 0.0333mm) converter area in mm^2
        
        self.DEFAULTVOUT = 850
        self.DEFAULTVIN = 1800
        self.DEFAULTFREQ = 100
        self.DEFAULTIINLIM = 150
        self.DEFAULTIOUTLIM = 150
        self.DEFAULTVOUTSWEEP = [700, 1150]
        self.DEFAULTFREQSWEEP = [20, 200]
        self.DEFAULTVGEAR = 890
        
        self.FREQLIM = [20, 200.1] # MHz
        self.IOUTLIM = [1, 3000] # mA
        self.IINLIM = [1, 1000] # mA
        self.VINLIM = [1700, 2200] # mV
        self.VOUTLIM = [500, 1350]
        
        self.ETAPLOT = [0, 100] # %
        self.RHOPLOT = [0, 10] # W/mm^2
        self.IOUTPLOT = [0, 50] # W/mm^2
        self.VOUTPLOT = [0, 1000] # W/mm^2
        
        self.DEFAULTSETTLETIME = 0.5
        self.DEFAULTPOINTS = [11, 16] # freq points, Vout points
        
        self.DEFAULTADJUSTVINVOUT = [True, True, True] # Vin adjust, Vout adjust, Vin & vout adjust
        
        self.clearDataLists()
        self.initUI()
        self.devices = devices.Devices()
        self.devices.printInstrList()
#        self.allInit()
           
    def initUI(self):    
        vMainBox, vMainLayout = self.addVWidget()
        self.setCentralWidget(vMainBox)    
        hMainBox, hMainLayout = self.addHWidget()
                   
        vMainLayout.addWidget(self.initButtons())
        vMainLayout.addWidget(hMainBox)
        hMainLayout.addWidget(self.setOnMeasButtons())
        hMainLayout.addWidget(self.setSweepButtons())
        
        self.statusBar()       
        self.setGeometry(25, 25, 1400, 700)
        self.setWindowTitle('Chip 2 Control Window')
        self.show()
    
    def initButtons(self):
        v0Box, v0Layout = self.addVWidget()
        
        btnInitHp = QtGui.QPushButton("Init HP", self)
        btnInitHp.clicked.connect(self.initClicked)
        btnInitAgilent = QtGui.QPushButton("Init Agilent", self)
        btnInitAgilent.clicked.connect(self.initClicked)
        btnInitKeithleyIn = QtGui.QPushButton("Init KeithleyIn", self)
        btnInitKeithleyIn.clicked.connect(self.initClicked)
        btnInitKeithleyOut = QtGui.QPushButton("Init KeithleyOut", self)
        btnInitKeithleyOut.clicked.connect(self.initClicked)
        btnInitSourceGear = QtGui.QPushButton("Init SourceGear", self)
        btnInitSourceGear.clicked.connect(self.initClicked)        
        btnInitAll = QtGui.QPushButton("Init all", self)
        btnInitAll.clicked.connect(self.initClicked)
        btnDefaultHp = QtGui.QPushButton("Default HP", self)
        btnDefaultHp.clicked.connect(self.defaultClicked)
        btnDefaultAgilent = QtGui.QPushButton("Default Agilent", self)
        btnDefaultAgilent.clicked.connect(self.defaultClicked)
        btnDefaultKeithleyIn = QtGui.QPushButton("Default KeithleyIn", self)
        btnDefaultKeithleyIn.clicked.connect(self.defaultClicked)
        btnDefaultKeithleyOut = QtGui.QPushButton("Default KeithleyOut", self)
        btnDefaultKeithleyOut.clicked.connect(self.defaultClicked)
        btnDefaultSourceGear = QtGui.QPushButton("Default SourceGear", self)
        btnDefaultSourceGear.clicked.connect(self.defaultClicked)          
        btnDefaultAll = QtGui.QPushButton("Default all", self)
        btnDefaultAll.clicked.connect(self.defaultClicked)    
        
        h0Box, h0Layout = self.addHWidget()
        v0Layout.addWidget(h0Box)          
        h0Layout.addWidget(btnInitHp)
        h0Layout.addWidget(btnInitAgilent)
        h0Layout.addWidget(btnInitKeithleyIn)
        h0Layout.addWidget(btnInitKeithleyOut)
        h0Layout.addWidget(btnInitSourceGear)
        h0Layout.addWidget(btnInitAll) 
        
        h1Box, h1Layout = self.addHWidget()
        v0Layout.addWidget(h1Box)  
        h1Layout.addWidget(btnDefaultHp)
        h1Layout.addWidget(btnDefaultAgilent)
        h1Layout.addWidget(btnDefaultKeithleyIn)
        h1Layout.addWidget(btnDefaultKeithleyOut)
        h1Layout.addWidget(btnDefaultSourceGear)
        h1Layout.addWidget(btnDefaultAll)
           
        v0Box.setMaximumHeight(100)
        v0Box.setMaximumWidth(700)
        return v0Box        
    
    def setOnMeasButtons(self):
        v0Box, v0Layout = self.addVWidget()

        self.leIinmax = QtGui.QLineEdit(str(self.DEFAULTIINLIM), self)
        self.leIinmax.setObjectName("Set max Iin [mA]")
        self.leIinmax.returnPressed.connect(self.setClicked)
        self.btnIinmax = QtGui.QPushButton("Set max Iin [mA]", self)
        self.btnIinmax.clicked.connect(self.setClicked)          
        self.lblIinmax = QtGui.QLabel('-', self)   
        v0Layout.addWidget(self.addHTripleWidget(self.leIinmax, self.btnIinmax, self.lblIinmax))   
        
        self.leIoutmax = QtGui.QLineEdit(str(self.DEFAULTIOUTLIM), self)
        self.leIoutmax.setObjectName("Set max Iout [mA]")
        self.leIoutmax.returnPressed.connect(self.setClicked)        
        self.btnIoutmax = QtGui.QPushButton("Set max Iout [mA]", self)
        self.btnIoutmax.clicked.connect(self.setClicked)            
        self.lblIoutmax = QtGui.QLabel('-', self) 
        v0Layout.addWidget(self.addHTripleWidget(self.leIoutmax, self.btnIoutmax, self.lblIoutmax))          
        
        self.leFreq = QtGui.QLineEdit(str(self.DEFAULTFREQ), self)
        self.leFreq.setObjectName("Set freq [MHz]")
        self.leFreq.returnPressed.connect(self.setClicked)        
        self.btnFreq = QtGui.QPushButton("Set freq [MHz]", self)
        self.btnFreq.clicked.connect(self.setClicked)            
        self.lblFreq = QtGui.QLabel('-', self)
        v0Layout.addWidget(self.addHTripleWidget(self.leFreq, self.btnFreq, self.lblFreq))       
        
        self.leVin = QtGui.QLineEdit(str(self.DEFAULTVIN), self)
        self.leVin.setObjectName("Set Vin [mV]")
        self.leVin.returnPressed.connect(self.setClicked)        
        self.btnVin = QtGui.QPushButton("Set Vin [mV]", self)
        self.btnVin.clicked.connect(self.setClicked)            
        self.lblVin = QtGui.QLabel('-', self)
        v0Layout.addWidget(self.addHTripleWidget(self.leVin, self.btnVin, self.lblVin)) 
        
        self.leVout = QtGui.QLineEdit(str(self.DEFAULTVOUT), self)
        self.leVout.setObjectName("Set Vout [mV]")
        self.leVout.returnPressed.connect(self.setClicked)
        self.btnVout = QtGui.QPushButton("Set Vout [mV]", self)
        self.btnVout.clicked.connect(self.setClicked)            
        self.lblVout = QtGui.QLabel('-', self) 
        v0Layout.addWidget(self.addHTripleWidget(self.leVout, self.btnVout, self.lblVout))       

        self.btnGear = QtGui.QPushButton("Toggle Gear", self)
        self.btnGear.clicked.connect(self.setClicked)            
        self.lblGear = QtGui.QLabel('-', self) 
        v0Layout.addWidget(self.addHTripleWidget(self.lblEmpty(), self.btnGear, self.lblGear))       
        
        self.btnMonChan = QtGui.QPushButton("Toggle mon chan", self)
        self.btnMonChan.clicked.connect(self.setClicked) 
        self.btnSetAll = QtGui.QPushButton("Set all", self)
        self.btnSetAll.clicked.connect(self.setClicked)        
        v0Layout.addWidget(self.addHTripleWidget(self.btnMonChan, self.btnSetAll, self.lblEmpty()))  
        
        v0Layout.addWidget(self.addHTripleWidget(self.lblEmpty(), self.lblEmpty(), self.lblEmpty()))                      
#------------------------------------------------------------------------------             

        self.btnFreqOn = QtGui.QPushButton("Freq on/off", self)
        self.btnFreqOn.clicked.connect(self.onClicked)            
        self.lblFreqOn = QtGui.QLabel('-', self) 
        v0Layout.addWidget(self.addHTripleWidget(self.lblEmpty(), self.btnFreqOn, self.lblFreqOn))     
        
        self.btnVinOn = QtGui.QPushButton("Vin on/off", self)
        self.btnVinOn.clicked.connect(self.onClicked)            
        self.lblVinOn = QtGui.QLabel('-', self)
        v0Layout.addWidget(self.addHTripleWidget(self.lblEmpty(), self.btnVinOn, self.lblVinOn))          
                 
        self.btnVoutOn = QtGui.QPushButton("Vout on/off", self)
        self.btnVoutOn.clicked.connect(self.onClicked)            
        self.lblVoutOn = QtGui.QLabel('-', self)
        v0Layout.addWidget(self.addHTripleWidget(self.lblEmpty(), self.btnVoutOn, self.lblVoutOn))       
        
        self.btnGearOn = QtGui.QPushButton("Gear on/off", self)
        self.btnGearOn.clicked.connect(self.onClicked)            
        self.lblGearOn = QtGui.QLabel('-', self)
        v0Layout.addWidget(self.addHTripleWidget(self.lblEmpty(), self.btnGearOn, self.lblGearOn))          
        
        self.btnAllOn = QtGui.QPushButton("All on", self)
        self.btnAllOn.clicked.connect(self.onClicked)             
        self.btnAllOff = QtGui.QPushButton("All off", self)
        self.btnAllOff.clicked.connect(self.onClicked)
        v0Layout.addWidget(self.addHTripleWidget(self.lblEmpty(), self.btnAllOn, self.btnAllOff))   

        v0Layout.addWidget(self.addHTripleWidget(self.lblEmpty(), self.lblEmpty(), self.lblEmpty()))            
#------------------------------------------------------------------------------         

        self.btnVink = QtGui.QPushButton("Meas Vink", self)
        self.btnVink.clicked.connect(self.measClicked)            
        self.lblVink = QtGui.QLabel('-', self)
        v0Layout.addWidget(self.addHTripleWidget(self.lblEmpty(), self.btnVink, self.lblVink))
        
        self.btnVoutk = QtGui.QPushButton("Meas Voutk", self)
        self.btnVoutk.clicked.connect(self.measClicked)            
        self.lblVoutk = QtGui.QLabel('-', self)  
        v0Layout.addWidget(self.addHTripleWidget(self.lblEmpty(), self.btnVoutk, self.lblVoutk))
    
        self.btnIin = QtGui.QPushButton("Meas Iin", self)
        self.btnIin.clicked.connect(self.measClicked)            
        self.lblIin = QtGui.QLabel('-', self)
        v0Layout.addWidget(self.addHTripleWidget(self.lblEmpty(), self.btnIin, self.lblIin))
        
        self.btnIout = QtGui.QPushButton("Meas Iout", self)
        self.btnIout.clicked.connect(self.measClicked)            
        self.lblIout = QtGui.QLabel('-', self) 
        v0Layout.addWidget(self.addHTripleWidget(self.lblEmpty(), self.btnIout, self.lblIout))
    
        self.btnExit = QtGui.QPushButton("Exit", self)
        self.btnExit.clicked.connect(self.exitClicked)        
        self.btnAll = QtGui.QPushButton("Meas All", self)
        self.btnAll.clicked.connect(self.measClicked)            
        self.lblAll = QtGui.QLabel('-', self) 
        v0Layout.addWidget(self.addHTripleWidget(self.btnExit, self.btnAll, self.lblAll))
        
        v0Box.setMaximumWidth(400)
        return v0Box 
    
    def setSweepButtons(self):
        v0Box, v0Layout = self.addVWidget() 
        
        h0Box, h0Layout = self.addHWidget() 
        v0Layout.addWidget(h0Box)
        
        self.leFmin = QtGui.QLineEdit(str(self.DEFAULTFREQSWEEP[0]), self)
        self.lblFmin = QtGui.QLabel('Fmin [MHz]', self)
        h0Layout.addWidget(self.addVTripleWidget(self.lblEmpty(), self.lblFmin, self.leFmin))
        
        self.leFmax = QtGui.QLineEdit(str(self.DEFAULTFREQSWEEP[1]), self) 
        self.lblFmax = QtGui.QLabel('Fmax [MHz]', self)     
        h0Layout.addWidget(self.addVTripleWidget(self.lblEmpty(), self.lblFmax, self.leFmax))
        
        self.leFreqPoints = QtGui.QLineEdit(str(self.DEFAULTPOINTS[0]), self) 
        self.lblFreqPoints = QtGui.QLabel('# frequency points', self)   
        h0Layout.addWidget(self.addVTripleWidget(self.lblEmpty(), self.lblFreqPoints, self.leFreqPoints))
        
        self.checkAdjustVin = QCheckBox("Adjust Vin", self)
        self.checkAdjustVin.setChecked(self.DEFAULTADJUSTVINVOUT[0])
        self.checkAdjustVout = QCheckBox("Adjust Vout", self)
        self.checkAdjustVout.setChecked(self.DEFAULTADJUSTVINVOUT[1])
#        self.checkAdjustVinVout = QCheckBox("Adjust Vin && Vout", self)
#        self.checkAdjustVinVout.setChecked(self.DEFAULTADJUSTVINVOUT[2])
#        self.checkAdjustVinVout.stateChanged.connect(self.measClicked)
        h0Layout.addWidget(self.addVTripleWidget(self.lblEmpty(), self.checkAdjustVin, self.checkAdjustVout))
        
#         self.checkPlotAllY = QCheckBox("Fit All Y axes", self)
#         self.checkPlotAllY.stateChanged.connect(self.plotClicked)     
#         self.checkPlotIncremental = QCheckBox("Plot incremental", self)
#         self.checkPlotIncremental.setChecked(False)
#         h0Layout.addWidget(self.addVTripleWidget(self.lblEmpty(), self.checkPlotAllY, self.checkPlotIncremental))        

        self.btnClearMessTable = QtGui.QPushButton("Clear table only", self)
        self.btnClearMessTable.clicked.connect(self.measClicked)
        self.btnClearSweep = QtGui.QPushButton("Clear table + plots", self)
        self.btnClearSweep.clicked.connect(self.measClicked)
        self.btnSweep = QtGui.QPushButton("Sweep fsw", self)
        self.btnSweep.clicked.connect(self.measClicked)
        h0Layout.addWidget(self.addVTripleWidget(self.btnClearMessTable, self.btnClearSweep, self.btnSweep))
        
        self.btnOpenMeasTable = QtGui.QPushButton("Open in Excel", self)
        self.btnOpenMeasTable.clicked.connect(self.measClicked)
        self.leSaveMeasTable = QtGui.QLineEdit("meas.xls", self)
        self.btnSaveMeasTable = QtGui.QPushButton("Save table", self)
        self.btnSaveMeasTable.clicked.connect(self.measClicked)
        h0Layout.addWidget(self.addVTripleWidget(self.btnOpenMeasTable, self.leSaveMeasTable, self.btnSaveMeasTable))
        
        h1Box, h1Layout = self.addHWidget() 
        v0Layout.addWidget(h1Box)
        
        self.leVoutmin = QtGui.QLineEdit(str(self.DEFAULTVOUTSWEEP[0]), self)
        self.lblVoutmin = QtGui.QLabel('Voutmin [mV]', self)
        h1Layout.addWidget(self.addVTripleWidget(self.lblEmpty(), self.lblVoutmin, self.leVoutmin))        
        
        self.leVoutmax = QtGui.QLineEdit(str(self.DEFAULTVOUTSWEEP[1]), self)
        self.lblVoutmax = QtGui.QLabel('Voutmax [mV]', self)
        h1Layout.addWidget(self.addVTripleWidget(self.lblEmpty(), self.lblVoutmax, self.leVoutmax))     

        self.leVoutPoints = QtGui.QLineEdit(str(self.DEFAULTPOINTS[1]), self)
        self.lblVoutPoints = QtGui.QLabel('# Vout points', self)
        h1Layout.addWidget(self.addVTripleWidget(self.lblEmpty(), self.lblVoutPoints, self.leVoutPoints))    
        
        self.leVgear = QtGui.QLineEdit(str(self.DEFAULTVGEAR), self)
        self.lblVgear = QtGui.QLabel('Vgear change [mV]', self)        
        h1Layout.addWidget(self.addVTripleWidget(self.lblEmpty(), self.lblVgear, self.leVgear))
        
        self.btnSweepVout = QtGui.QPushButton("Sweep Vout", self)
        self.btnSweepVout.clicked.connect(self.measClicked)
        h1Layout.addWidget(self.addVTripleWidget(self.lblEmpty(), self.lblEmpty(), self.btnSweepVout))                        
        
        self.btnOpenSweep = QtGui.QPushButton("Open sweep Excel", self)
        self.btnOpenSweep.clicked.connect(self.measClicked)
        self.leSweepVoutFsw = QtGui.QLineEdit("chip1.xls", self)
        self.btnSweepVoutFsw = QtGui.QPushButton("Sweep Vout && fsw", self)
        self.btnSweepVoutFsw.clicked.connect(self.measClicked)                 
        h1Layout.addWidget(self.addVTripleWidget(self.btnOpenSweep, self.leSweepVoutFsw, self.btnSweepVoutFsw))       
        h1Layout.addWidget(self.addVTripleWidget(self.lblEmpty(), self.lblEmpty(), self.lblEmpty()))                 
        
        tab = QTabWidget()
        tab.addTab(self.createTableTab(), 'Meas Table')
#         tab.addTab(self.createEtaRhoTab(), 'eta && rho plots')
#         tab.addTab(self.createIoutVoutTab(), 'Iout && Vout plots')
        v0Layout.addWidget(tab)
        #self.updateAllPlots()

        v0Box.setMaximumWidth(1050)
        return v0Box 

    def createTableTab(self):
        v0Box, v0Layout = self.addVWidget()
        self.hHeader = ["fsw [MHz]", "Iin [mA]", "Iout [mA]", "Vink [mV]", "Vins [mV]", "Voutk [mV]", "Vouts [mV]", "Rload [ohm]", "Pout [mW]", "Pin [mW]", "eta [%]", "rho [W/mm2]"]
        self.vHeader = range(100)
        self.measTbl = self.createTable(self.hHeader, self.vHeader, 80, 18)
        v0Layout.addWidget(self.measTbl)
        return v0Box
    
#     def createEtaRhoTab(self):
#         plotWidget, h0Layout = self.addHWidget()
#         etaPlotWidget, v0Layout = self.addVWidget()
#         rhoPlotWidget, v1Layout = self.addVWidget()
#         h0Layout.addWidget(etaPlotWidget)
#         h0Layout.addWidget(rhoPlotWidget)
#         self.checkEtaYAxis = QCheckBox("Fit eta Y axis", self)
#         self.checkEtaYAxis.setChecked(False)
#         self.checkEtaYAxis.stateChanged.connect(self.plotClicked)        
# 
#         self.etaPlot = mplCanvas.MplCanvas(etaPlotWidget, width=5, height=4, dpi=100)
#         self.etaMplToolbar = NavigationToolbar(self.etaPlot, etaPlotWidget)
#         v0Layout.addWidget(self.checkEtaYAxis)     
#         v0Layout.addWidget(self.etaPlot)
#         v0Layout.addWidget(self.etaMplToolbar)
#         
#         self.checkRhoYAxis = QCheckBox("Fit rho Y axis", self)
#         self.checkRhoYAxis.setChecked(False)
#         self.checkRhoYAxis.stateChanged.connect(self.plotClicked)              
#         
#         self.rhoPlot = mplCanvas.MplCanvas(rhoPlotWidget, width=5, height=4, dpi=100)
#         self.rhoMplToolbar = NavigationToolbar(self.rhoPlot, rhoPlotWidget)
#         v1Layout.addWidget(self.checkRhoYAxis)
#         v1Layout.addWidget(self.rhoPlot)
#         v1Layout.addWidget(self.rhoMplToolbar)  
# 
#         return plotWidget     
#     
#     def createIoutVoutTab(self):
#         plotWidget, h0Layout = self.addHWidget()
#         ioutPlotWidget, v0Layout = self.addVWidget()
#         voutPlotWidget, v1Layout = self.addVWidget()
#         h0Layout.addWidget(ioutPlotWidget)
#         h0Layout.addWidget(voutPlotWidget)
#         self.checkIoutYAxis = QCheckBox("Fit Iout Y axis", self)
#         self.checkIoutYAxis.setChecked(False)
#         self.checkIoutYAxis.stateChanged.connect(self.plotClicked)        
# 
#         self.ioutPlot = mplCanvas.MplCanvas(ioutPlotWidget, width=5, height=4, dpi=100)
#         self.ioutMplToolbar = NavigationToolbar(self.ioutPlot, ioutPlotWidget)
#         v0Layout.addWidget(self.checkIoutYAxis)     
#         v0Layout.addWidget(self.ioutPlot)
#         v0Layout.addWidget(self.ioutMplToolbar)
#         
#         self.checkVoutYAxis = QCheckBox("Fit Vout Y axis", self)
#         self.checkVoutYAxis.setChecked(False)
#         self.checkVoutYAxis.stateChanged.connect(self.plotClicked)              
#         
#         self.voutPlot = mplCanvas.MplCanvas(voutPlotWidget, width=5, height=4, dpi=100)
#         self.voutMplToolbar = NavigationToolbar(self.voutPlot, voutPlotWidget)
#         v1Layout.addWidget(self.checkVoutYAxis)
#         v1Layout.addWidget(self.voutPlot)
#         v1Layout.addWidget(self.voutMplToolbar)  
# 
#         return plotWidget          
        
    def addHTripleWidget(self, W1, W2, W3):
        hBox, hLayout = self.addHWidget()   
        W1.setMaximumWidth(100)
        W1.setMinimumWidth(100)
        W2.setMaximumWidth(100)
        W2.setMinimumWidth(100)
        W3.setMaximumWidth(100)
        W3.setMinimumWidth(100)
        hLayout.addWidget(W1)
        hLayout.addWidget(W2)
        hLayout.addWidget(W3)
        return hBox
    
    def addVTripleWidget(self, W1, W2, W3):
        vBox, vLayout = self.addVWidget()   
        W1.setMaximumWidth(100)
        W1.setMinimumWidth(100)
        W2.setMaximumWidth(100)
        W2.setMinimumWidth(100)
        W3.setMaximumWidth(100)
        W3.setMinimumWidth(100)
        vLayout.addWidget(W1)
        vLayout.addWidget(W2)
        vLayout.addWidget(W3)
        return vBox      
    def addVWidget(self):
        Box = QWidget(); 
        Layout = QVBoxLayout(); 
        Box.setLayout(Layout)
        Box.setContentsMargins(QtCore.QMargins(0, 0, 0, 0))
        Layout.layout().setContentsMargins(0, 0, 0, 0)
        return Box, Layout   
    def addHWidget(self):
        Box = QWidget(); 
        Layout = QHBoxLayout(); 
        Box.setLayout(Layout)
        Box.setContentsMargins(QtCore.QMargins(0, 0, 0, 0))
        Layout.layout().setContentsMargins(0, 0, 0, 0)
        return Box, Layout
    def lblEmpty(self):
        return QtGui.QLabel('', self) 
      
    def initClicked(self):
        self.buttonClicked()
        try:
            self.devices = devices.Devices()
            if self.sender().text() == "Init HP":
                self.hpInit()
            if self.sender().text() == "Init Agilent":
                self.agilentInit()
            if self.sender().text() == "Init KeithleyIn":
                self.keithleyInInit()
            if self.sender().text() == "Init KeithleyOut":
                self.keithleyOutInit()
            if self.sender().text() == "Init SourceGear":
                self.sourceGearInit()                
            if self.sender().text() == "Init all":
                self.allInit()        
            if self.sender().text() == "Exit":
                self.close()                                                                                             
        except Exception as e:
            print(str(e))                              
    def hpInit(self):
        self.hp = hp.Hp()
        print ('hp = ' + self.hp.initme(self.devices, '8131A'))      
        self.updateFreqLbl()
        self.updateFreqOn()
    def agilentInit(self):
        self.agilent = agilent.Agilent()
        print('agilent = ' + self.agilent.initme(self.devices, '34970A'))      
    def keithleyInInit(self):
        self.keithleyIn = keithley.Keithley()
        print('keithleyIn = ' + self.keithleyIn.initme(self.devices, '2400', self.DEFAULTVIN*1e-3, self.VINLIM[1]*1e-3))         
        self.lblVink.setText('-')    
        self.lblIin.setText('-')
        self.updateVinLbl()
        self.updateIinmaxLbl()
        self.updateVinOn()        
    def keithleyOutInit(self):
        self.keithleyOut = keithley.Keithley()
        print('keithleyOut = ' + self.keithleyOut.initme(self.devices, '2420', self.DEFAULTVOUT*1e-3, self.VOUTLIM[1]*1e-3))          
        self.lblVoutk.setText('-')
        self.lblIout.setText('-')
        self.updateVoutLbl()
        self.updateIoutmaxLbl()
        self.updateVoutOn()      
    def sourceGearInit(self):
        self.sourceGear = agilentDC.AgilentDC()
        print('sourceGear = ' + self.sourceGear.initme(self.devices, '3642'))    
        self.updateGearOn()
        self.updateGearLbl()
    def allInit(self):
        self.hpInit()   
        self.agilentInit() 
        self.keithleyInInit()   
        self.keithleyOutInit() 
        self.sourceGearInit()
        self.updateAllLbl()          
    def exitClicked(self):
        self.allOff()
        self.close()                        
   
#------------------------------------------------------------------------------            
    def defaultClicked(self):
        self.buttonClicked()
        try:
            if self.sender().text() == "Default HP":
                self.defaultHp()
            if self.sender().text() == "Default Agilent":
                self.defaultAgilent()
            if self.sender().text() == "Default KeithleyIn":
                self.defaultKeithleyIn()
            if self.sender().text() == "Default KeithleyOut":
                self.defaultKeithleyOut()
            if self.sender().text() == "Default SourceGear":
                self.defaultSourceGear()
            if self.sender().text() == "Default all":
                self.defaultAll()
        except Exception as e:
            print(str(e))   
            
    def defaultHp(self):
        self.hp.defaultSetup()
        self.leFreq.setText(str(self.DEFAULTFREQ))
        self.updateFreqLbl()
        self.updateFreqOn()      
    def defaultAgilent(self):
        self.agilent.defaultSetup()
    def defaultKeithleyIn(self):
        self.keithleyIn.defaultSetup()
        self.leVin.setText(str(self.DEFAULTVIN))
        self.updateVinLbl()
        self.updateIinmaxLbl()
        self.updateVinOn()        
    def defaultKeithleyOut(self):
        self.keithleyOut.defaultSetup()
        self.leVout.setText(str(self.DEFAULTVOUT))
        self.updateVoutLbl()
        self.updateIoutmaxLbl()
        self.updateVoutOn()   
    def defaultSourceGear(self):
        self.sourceGear.defaultSetup()
        self.updateGearLbl()
        self.updateGearOn()
    def defaultAll(self):
        self.defaultSourceGear()
        self.defaultKeithleyIn()
        time.sleep(1)
        self.defaultHp()
        time.sleep(1)   
        self.defaultAgilent()   
        self.defaultKeithleyOut()   
        
#------------------------------------------------------------------------------
    def onClicked(self):
        self.buttonClicked()
        try:
            if self.sender().text() == "Freq on/off":
                self.freqOnOff()
            if self.sender().text() == "Vin on/off":
                self.vinOnOff()
            if self.sender().text() == "Vout on/off":
                self.voutOnOff()
            if self.sender().text() == "Gear on/off":
                self.gearOnOff()
            if self.sender().text() == "All on":
                self.allOn()
            if self.sender().text() == "All off":
                self.allOff()                                                                            
        except Exception as e:
            print(str(e))   
            
    def freqOnOff(self):
        self.hp.setOutput('ON' if self.hp.getOutput() == 'OFF' else 'OFF')
        self.updateFreqOn() 
    def vinOnOff(self):   
        if self.keithleyOut.getOutput() == '1':
            self.keithleyIn.setOutput('ON' if self.keithleyIn.getOutput() == '0' else 'OFF')
            self.updateVinOn()        
    def voutOnOff(self):
        if self.keithleyIn.getOutput() == '0':
            self.keithleyOut.setOutput('ON' if self.keithleyOut.getOutput() == '0' else 'OFF')
            self.updateVoutOn()  
    def gearOnOff(self):   
        self.sourceGear.setOutput('ON' if self.sourceGear.getOutput() == '0' else 'OFF') 
        self.updateGearOn()         
    def allOn(self):
        self.hp.outputOn()
        time.sleep(1)
        self.keithleyOut.outputOn()
        time.sleep(1)
        self.keithleyIn.outputOn() 
        time.sleep(1)
        self.sourceGear.outputOn()
        self.updateAllLbl()
    def allOff(self):
        self.keithleyIn.outputOff()
        time.sleep(1)        
        self.sourceGear.outputOff()
        time.sleep(1)
        self.hp.outputOff()
        time.sleep(1)
        self.keithleyOut.outputOff()  
        self.updateAllLbl()
    def isAllOn(self):
        if self.hp.getOutput()=='ON' and self.keithleyIn.getOutput()=='1' and self.keithleyOut.getOutput()=='1' and self.sourceGear.getOutput()=='1':
            return True
        else:
            print 'Not all measurement equipment is turned on -> No measurements performed'
            return False

#------------------------------------------------------------------------------
    def setClicked(self):
        self.buttonClicked()
        try:
            Iinmax  = float(self.leIinmax.text())
            Ioutmax = float(self.leIoutmax.text())
            Freq    = float(self.leFreq.text())
            Vin     = float(self.leVin.text())
            Vout    = float(self.leVout.text())
            if self.sender().text() == "Set max Iin [mA]" or self.sender().objectName() == "Set max Iin [mA]":
                self.setIinmax(Iinmax)
            if self.sender().text() == "Set max Iout [mA]" or self.sender().objectName() == "Set max Iout [mA]":
                self.setIoutmax(Ioutmax)
            if self.sender().text() == "Set freq [MHz]" or self.sender().objectName() == "Set freq [MHz]":
                self.setFreq(Freq)
            if self.sender().text() == "Set Vin [mV]" or self.sender().objectName() == "Set Vin [mV]":
                self.setVin(Vin)
            if self.sender().text() == "Set Vout [mV]" or self.sender().objectName() == "Set Vout [mV]":
                self.setVout(Vout)
            if self.sender().text() == "Toggle Gear" or self.sender().objectName() == "Toggle Gear":
                self.toggleGear()
            if self.sender().text() == "Set all":
                self.setAll(Iinmax, Ioutmax, Freq, Vin, Vout)
            if self.sender().text() == "Toggle mon chan":
                self.setMonChan()                
        except Exception as e:
            print(str(e))            
    def setIinmax(self, Iinmax):
        if self.withinLim(Iinmax, self.IINLIM[1], self.IINLIM[0]):
            self.keithleyIn.setIlim(Iinmax*1e-3)
            self.updateIinmaxLbl()       
    def setIoutmax(self, Ioutmax):
        if self.withinLim(Ioutmax, self.IOUTLIM[1], self.IOUTLIM[0]):
            self.keithleyOut.setIlim(Ioutmax*1e-3)
            self.updateIoutmaxLbl()         
    def setFreq(self, Freq):
        if self.withinLim(Freq, self.FREQLIM[1], self.FREQLIM[0]):
            self.hp.setFreq(self.mhz2ns(Freq))
            self.updateFreqLbl()                
    def setVin(self, Vin):
        if self.withinLim(Vin, self.VINLIM[1], self.VINLIM[0]):        
            self.keithleyIn.setV(Vin*1e-3)
            self.updateVinLbl()    
            self.leVin.setText(str(f2(Vin)))
    def setVout(self, Vout):
        if self.withinLim(Vout, self.VOUTLIM[1], self.VOUTLIM[0]):  
            self.keithleyOut.setV(Vout*1e-3)
            self.updateVoutLbl() 
            self.leVout.setText(str(f2(Vout)))  
    def setGear(self, state):
        self.sourceGear.setV(1 if state == 'HIGH' or state == 1 else 0)
        self.updateGearLbl()
    def toggleGear(self):
        self.sourceGear.setV(0 if float(self.sourceGear.getV()) > 0.8 else 1)
        self.updateGearLbl()
    def setAll(self, Iinmax, Ioutmax, Freq, Vin, Vout):
        self.setIinmax(Iinmax)
        self.setIoutmax(Ioutmax) 
        self.setFreq(Freq)
        self.setVin(Vin)              
        self.setVout(Vout)
    def setMonChan(self):
        monChan = self.agilent.getMonChan() 
        if monChan[5:8] == '101':
            self.agilent.setMonChan(102)
        else:
            self.agilent.setMonChan(101)      
    
#     def plotClicked(self):
#         try:
#             if self.sender().text() == "Fit eta Y axis":
#                 self.updateEtaPlot()       
#             if self.sender().text() == "Fit rho Y axis":
#                 self.updateRhoPlot()     
#             if self.sender().text() == "Fit Iout Y axis":
#                 self.updateIoutPlot()   
#             if self.sender().text() == "Fit Vout Y axis":
#                 self.updateVoutPlot()     
#             if self.sender().text() == "Fit All Y axes":
#                 self.fitAllPlots()                                                                                                                                        
#         except Exception as e:
#             print(str(e))   
#     def updateEtaPlot(self):
#         if self.etaData:
#             self.etaPlot.setData(self.freqData, self.etaData) 
#             if int(max(self.etaData)*1.1) != 0:
#                 if self.checkEtaYAxis.isChecked():
#                     self.etaPlot.setYAxis(int(min(self.etaData)*0.9), int(max(self.etaData)*1.1), 10, 'eta [%]', 1)
#                 else:
#                     self.etaPlot.setYAxis(self.ETAPLOT[0], self.ETAPLOT[1], 10, 'eta [%]', 0)               
#     def updateRhoPlot(self):
#         if self.rhoData: 
#             self.rhoPlot.setData(self.freqData, self.rhoData)
#             if int(max(self.rhoData)*1.1) != 0:
#                 if self.checkRhoYAxis.isChecked():
#                     self.rhoPlot.setYAxis(int(min(self.rhoData)*0.9), int(max(self.rhoData)*1.1), 10, 'rho [W/mm^2]', 1)
#                 else:
#                     self.rhoPlot.setYAxis(self.RHOPLOT[0], self.RHOPLOT[1], 10, 'rho [W/mm^2]', 1)            
#     def updateIoutPlot(self):
#         if self.ioutData: 
#             self.ioutPlot.setData(self.freqData, self.ioutData)
#             if int(max(self.ioutData)*1.1) != 0:
#                 if self.checkIoutYAxis.isChecked():
#                     self.ioutPlot.setYAxis(int(min(self.ioutData)*0.9), int(max(self.ioutData)*1.1), 10, 'iout [mA]', 1)
#                 else:
#                     self.ioutPlot.setYAxis(self.IOUTPLOT[0], self.IOUTPLOT[1], 10, 'iout [mA]', 1)           
#     def updateVoutPlot(self):
#         if self.voutData:
#             self.voutPlot.setData(self.freqData, self.voutData) 
#             if int(max(self.voutData)*1.1) != 0:
#                 if self.checkVoutYAxis.isChecked():
#                     self.voutPlot.setYAxis(int(min(self.voutData)*0.9), int(max(self.voutData)*1.1), 10, 'vout [mV]', 1)
#                 else:
#                     self.voutPlot.setYAxis(self.VOUTPLOT[0], self.VOUTPLOT[1], 10, 'vout [mV]', 1)          
#     def fitAllPlots(self):
#         if self.checkPlotAllY.isChecked():
#             self.checkEtaYAxis.setChecked(True)
#             self.checkRhoYAxis.setChecked(True)
#             self.checkIoutYAxis.setChecked(True)
#             self.checkVoutYAxis.setChecked(True)
#         else:
#             self.checkEtaYAxis.setChecked(False)
#             self.checkRhoYAxis.setChecked(False)
#             self.checkIoutYAxis.setChecked(False)
#             self.checkVoutYAxis.setChecked(False)
#     def updateAllPlots(self):
#         QtGui.QApplication.processEvents()
#         self.updateEtaPlot()
#         self.updateRhoPlot()
#         QtGui.QApplication.processEvents() 
#         self.updateIoutPlot()
#         self.updateVoutPlot() 
          
#------------------------------------------------------------------------------                                    
    def measClicked(self):
        self.buttonClicked()
        try:
            if self.sender().text() == "Meas Vink":
                self.measVink()
            if self.sender().text() == "Meas Voutk":
                self.measVoutk()
            if self.sender().text() == "Meas Iin":                    
                self.measIin()
            if self.sender().text() == "Meas Iout":
                self.measIout()
            if self.sender().text() == "Meas All":
                self.measAll()
            if self.sender().text() == "Sweep fsw":
                self.measSweepFsw()   
            if self.sender().text() == "Clear table only":  
                self.clearTable(self.measTbl)                
            if self.sender().text() == "Clear table + plots":  
                self.clearSweep()
            if self.sender().text() == "Save table":  
                self.saveTable(self.measTbl, str(self.leSaveMeasTable.text()), str(self.leSaveMeasTable.text()))     
            if self.sender().text() == "Open in Excel":  
                self.openFile(self.leSaveMeasTable.text())           
            if self.sender().text() == "Sweep Vout":
                self.measSweepVout()   
            if self.sender().text() == "Sweep Vout && fsw":
                self.measSweepFreqVout()              
            if self.sender().text() == "Open sweep Excel":  
                self.openFile(self.leSweepVoutFsw.text())  
            if self.sender().text() == "Adjust Vin && Vout":  
                self.setAdjustVinVout()                
                
        except Exception as e:
            print(str(e))  
    def setAdjustVinVout(self):
        if self.checkAdjustVinVout.isChecked():
            self.checkAdjustVin.setChecked(True)
            self.checkAdjustVout.setChecked(True)   
        else:
            self.checkAdjustVin.setChecked(False)
            self.checkAdjustVout.setChecked(False)            
    def measVink(self):
        QtGui.QApplication.processEvents()
        Vink = self.agilent.measVink()
        self.lblVink.setText(f2(Vink*1e3) + ' mV')
        return Vink    
    def measVoutk(self):
        QtGui.QApplication.processEvents()
        Voutk = self.agilent.measVoutk()
        self.lblVoutk.setText(f2(Voutk*1e3) + ' mV')
        if Voutk*1e3 < self.VOUTLIM[0]:
            self.allOff()
            print 'Vout={0} mV is measured too low, all eqipment is turned off'.format(Voutk*1e3)
            return
        else:   
            return Voutk  
    def measIin(self):
        if self.keithleyIn.getOutput()=='1':
            QtGui.QApplication.processEvents()
            Iin = self.keithleyIn.measI()
            self.lblIin.setText(f2(Iin*1e3) + ' mA')
            return Iin 
        else:
            print 'KeithleyIn is not on -> no measurement performed ...'
    def measIout(self):
        if self.keithleyOut.getOutput()=='1':
            QtGui.QApplication.processEvents()
            Iout = -self.keithleyOut.measI()
            self.lblIout.setText(f2(Iout*1e3) + ' mA')
            return Iout
        else:
            print 'KeithleyOut is not on -> no measurement performed ...'
    def measAll(self):
        if self.isAllOn():
            Voutk = self.measVoutk()
            Vink = self.measVink()
            Iin = self.measIin()
            Iout = self.measIout()
            [eta, rho, Rload, Pin, Pout] = self.calc(Vink, Voutk, Iin, Iout)
            self.lblAll.setText(('eta = {0}% \n rho = {1} W/mm2'.format(f2(eta*100), f2(rho))))
            return Vink, Voutk, Iin, Iout
    def plotIncremental(self):
        return True if self.checkPlotIncremental.isChecked() else False
    def measSweepSingle(self, Freq, Vout, Vin):
#                rowData = [Freq[i], i, i, i, i, i, i, i, i, i]
#                self.updateTableRow(self.measTbl, i, rowData)  
#                self.freqData.append(Freq[i])
#                self.etaData.append(i+10)
#                self.rhoData.append(i)
#                self.ioutData.append(2*i)
#                self.voutData.append(4*i + 10)
        self.setFreq(Freq)
        QtGui.QApplication.processEvents()
        time.sleep(self.DEFAULTSETTLETIME)
        if self.checkAdjustVout.isChecked() == False:
            self.setVout(Vout)
        if self.checkAdjustVin.isChecked() == False:
            self.setVin(Vin)
            
        if self.checkAdjustVin.isChecked():
            self.adjustVin(Vin)
        if self.checkAdjustVout.isChecked():
            self.adjustVout(Vout)
        if self.checkAdjustVin.isChecked():
            self.adjustVin(Vin)
        if self.checkAdjustVout.isChecked():
            self.adjustVout(Vout)
        QtGui.QApplication.processEvents() 
        time.sleep(self.DEFAULTSETTLETIME)   
        if self.checkAdjustVin.isChecked():
            self.adjustVin(Vin)
        if self.checkAdjustVout.isChecked():
            self.adjustVout(Vout)    
        QtGui.QApplication.processEvents() 
        time.sleep(self.DEFAULTSETTLETIME)
        [Vink, Voutk, Iin, Iout] = self.measAll()
        [eta, rho, Rload, Pin, Pout] = self.calc(Vink, Voutk, Iin, Iout)
        rowData = [f1(Freq), f2(Iin*1e3), f2(Iout*1e3), f1(Vink*1e3), f1(float(self.keithleyIn.getV())*1e3), f1(Voutk*1e3), f1(float(self.keithleyOut.getV())*1e3), f2(Rload), f2(Pin*1e3), f2(Pout*1e3), f2(eta*100), f2(rho)]
        self.freqData.append(Freq)
        self.etaData.append(eta)
        self.rhoData.append(rho)
        self.ioutData.append(Iout)
        self.voutData.append(Voutk)
        return rowData    
    def measSweepFsw(self):
        if self.isAllOn() == False: return
        if self.checkFreqVoutLimits() == False: return
        VoutOld = float(self.leVout.text())
        VinOld = float(self.leVin.text())      
        FreqOld = self.ns2mhz(self.hp.getFreq())  
        Fmin = float(self.leFmin.text())
        Fmax    = float(self.leFmax.text())   
        
        Freq = np.logspace(np.log10(Fmin), np.log10(Fmax), num=self.leFreqPoints.text(), base = 10)
        Vout = float(self.leVout.text())
        Vin = float(self.leVin.text())
        
        self.clearSweep()
#         self.etaPlot.setXAxis(Fmin, Fmax, 10, 'fsw [MHz]', 0)
#         self.rhoPlot.setXAxis(Fmin, Fmax, 10, 'fsw [MHz]', 0)
#         self.ioutPlot.setXAxis(Fmin, Fmax, 10, 'fsw [MHz]', 0)
#         self.voutPlot.setXAxis(Fmin, Fmax, 10, 'fsw [MHz]', 0)        
        
        for i in range(0,len(Freq)):
            QtGui.QApplication.processEvents()
            self.updateTableRow(self.measTbl, i, self.measSweepSingle(Freq[i], Vout, Vin))
#             if self.plotIncremental():
#                 self.updateAllPlots()         
#        if not self.plotIncremental():
        self.setVin(VinOld)
        self.setVout(VoutOld)   
#         self.updateAllPlots()
        self.setFreq(FreqOld)
    def measSweepVout(self):
        if self.isAllOn() == False: return
        if self.checkFreqVoutLimits() == False: return
        VoutOld = float(self.leVout.text())
        VinOld = float(self.leVin.text())
        Voutmin = float(self.leVoutmin.text())
        Voutmax = float(self.leVoutmax.text())
        VgearChange = float(self.leVgear.text())
        Vout = np.linspace(Voutmin, Voutmax , num=self.leVoutPoints.text())
        Vin = float(self.leVin.text())
        Freq = float(self.leFreq.text())
        
        self.clearSweep()
#         self.etaPlot.setXAxis(Voutmin, Voutmax, 10, 'Vout [mV]', 0)
#         self.rhoPlot.setXAxis(Voutmin, Voutmax, 10, 'Vout [mV]', 0)
#         self.ioutPlot.setXAxis(Voutmin, Voutmax, 10, 'Vout [mV]', 0)
#         self.voutPlot.setXAxis(Voutmin, Voutmax, 10, 'Not in use', 0)
        
        for i in range(0,len(Vout)):
            QtGui.QApplication.processEvents()   
            self.sourceGear.setV(1 if Vout[i]>=VgearChange else 0)
            self.updateGearLbl()
            self.updateTableRow(self.measTbl, i, self.measSweepSingle(Freq, Vout[i], Vin))               
#             if self.plotIncremental():
#                 self.updateAllPlots()
#            if not self.plotIncremental():
#         self.updateAllPlots()         
        self.setVin(VinOld)
        self.setVout(VoutOld)   
#        self.keithleyOut.setV(VoutOld)
        self.setGear('HIGH' if VoutOld>=VgearChange else 'LOW') 
    def measSweepFreqVout(self):
        if self.isAllOn() == False: return
        if self.checkFreqVoutLimits() == False: return
        if self.confirmOverwrite(str(self.leSweepVoutFsw.text())):
            FreqOld = self.ns2mhz(self.hp.getFreq())
            VoutOld = float(self.leVout.text())
            VinOld = float(self.leVin.text())            
            Vin = float(self.leVin.text())
            Fmin = float(self.leFmin.text())
            Fmax    = float(self.leFmax.text())
            Freq = np.logspace(np.log10(Fmin), np.log10(Fmax), num=self.leFreqPoints.text(), base = 10)
            Voutmin = float(self.leVoutmin.text())
            Voutmax = float(self.leVoutmax.text())
            VgearChange = float(self.leVgear.text())
            Vout = np.linspace(Voutmin, Voutmax , num=self.leVoutPoints.text())   
            xlsfiles = list()
            
            for i in range(0,len(Vout)):
                self.setGear('HIGH' if Vout[i]>=VgearChange else 'LOW')
                self.clearSweep()
                self.etaPlot.setXAxis(Fmin, Fmax, 10, 'fsw [MHz]', 0)
                self.rhoPlot.setXAxis(Fmin, Fmax, 10, 'fsw [MHz]', 0)
                self.ioutPlot.setXAxis(Fmin, Fmax, 10, 'fsw [MHz]', 0)
                self.voutPlot.setXAxis(Fmin, Fmax, 10, 'fsw [MHz]', 0)
                for j in range(0,len(Freq)):
                    QtGui.QApplication.processEvents()   
                    self.updateTableRow(self.measTbl, j, self.measSweepSingle(Freq[j], Vout[i], Vin))
#                    if self.plotIncremental():
#                        self.updateAllPlots()
#                self.updateAllPlots()
                self.saveTable(self.measTbl, 'Vout{0}.xls'.format(f0(Vout[i])), 'Vout=%s' % f1(Vout[i]))
                xlsfiles.append('Vout{0}.xls'.format(f0(Vout[i])))
            
            self.setFreq(FreqOld)    
            self.setVin(VinOld)
            self.setVout(VoutOld)   
            self.setGear('HIGH' if VoutOld>=VgearChange else 'LOW') 
            self.allOff()
            
            self.combine_xls(self.leSweepVoutFsw.text(), xlsfiles)
            self.removeFile(xlsfiles)   
            print '{0} was saved and all intermediate files {1} were deleted'.format(self.leSweepVoutFsw.text(), xlsfiles)
                                     
    def checkFreqVoutLimits(self):
            Fmin = float(self.leFmin.text())
            Fmax    = float(self.leFmax.text())        
            if Fmin < self.FREQLIM[0]:
                print '{0} < min = {1} -> not processed'.format(Fmin, self.FMINLIM[0]); return False
            elif Fmax > self.FREQLIM[1]:
                print '{0} > max = {1} -> not processed'.format(Fmax, self.FMAXLIM[1]); return False
            elif Fmax < Fmin:
                print 'Fmax < Fmin -> not processed'; return False         
            FreqPoints  = int(self.leFreqPoints.text())
            if FreqPoints > 100:
                FreqPoints = 100; print ('Freq points set to %s' % FreqPoints)
            elif FreqPoints < 1:
                FreqPoints = 1; print ('Freq points set to %s' % FreqPoints)
                
            Voutmin = float(self.leVoutmin.text())
            Voutmax = float(self.leVoutmax.text())
            if Voutmin < self.VOUTLIM[0]:
                print '{0} < min = {1} -> not processed'.format(Voutmin, self.VOUTLIM[0]); return False
            elif Voutmax > self.VOUTLIM[1]:
                print '{0} > max = {1} -> not processed'.format(Voutmax, self.VOUTLIM[1]); return False
            elif Voutmax < Voutmin:
                print 'Voutmax < Voutmin -> not processed'; return False
            VoutPoints  = int(self.leVoutPoints.text())
            if VoutPoints > 100:
                VoutPoints = 100; print ('Vout points set to %s' % VoutPoints)
            elif VoutPoints < 1:
                VoutPoints = 1; print ('Vout points set to %s' % VoutPoints)               
            return True           
        
    def adjustVin(self, Vintarget):
        Vink = float(self.measVink())
#        print Vintarget, Vink*1e3, float(self.leVin.text()) + (Vintarget - Vink*1e3)
        self.setVin(float(self.leVin.text()) + (Vintarget - Vink*1e3))
    def adjustVout(self, Vouttarget):
        Voutk = float(self.measVoutk())
#        print Vouttarget, Voutk*1e3, float(self.leVout.text()) + (Vouttarget - Voutk*1e3)
        self.setVout( float(self.leVout.text()) + (Vouttarget - Voutk*1e3))
    def adjustVinVout(self, Vintarget, Vouttarget):
        self.adjustVin(Vintarget)
        self.adjustVout(Vouttarget)

    def clearDataLists(self):
        self.freqData = list()
        self.etaData = list()
        self.rhoData = list()
        self.ioutData = list()
        self.voutData = list()
    def clearSweep(self):
        self.clearTable(self.measTbl)
        self.clearDataLists()
#         self.etaPlot.clearFig()
#         self.rhoPlot.clearFig()
#         self.ioutPlot.clearFig()
#         self.voutPlot.clearFig()
          
#------------------------------------------------------------------------------ 
    def createTable(self, hHeader, vHeader, colW, rowH):
        tbl = QTableWidget(len(vHeader), len(hHeader), self)
        for i in range(0, len(hHeader)):
            tbl.setHorizontalHeaderItem(i, QTableWidgetItem(str(hHeader[i])))
            tbl.setColumnWidth(i, colW)
        for i in range(0, len(vHeader)):
            tbl.setVerticalHeaderItem(i, QTableWidgetItem(str(vHeader[i])))
            tbl.setRowHeight(i, rowH)
        tbl.setRowCount(len(vHeader))
        tbl.setColumnCount(len(hHeader))
        self.clearTable(tbl)
        return tbl

    def updateTableRow(self, table, row, rowData):
        for i in range(0, len(rowData)):
            item = QTableWidgetItem(str(rowData[i]))
            item.setFlags(QtCore.Qt.ItemIsEnabled) # makes cells read-only
            table.setItem(row, i, item)            
                                      
    def tableIsEmpty(self, table):
        for i in range(0, table.rowCount()):
            for j in range(0, table.columnCount()):
                if table.item(i, j).text() != '':
                    return False
        return True     

    def cellIsEmpty(self, table, row, column):
        if table.item(row, column).text() == '':
            return True
        return False                    
                
    def clearTable(self, table):
        for i in range(0, table.rowCount()):
            for j in range(0, table.columnCount()):
                item = QTableWidgetItem(str(''))
                item.setFlags(QtCore.Qt.ItemIsEnabled) # makes cells read-only
                table.setItem(i, j, item) 
                
    def saveTable(self, table, filename, sheetname):
        if self.tableIsEmpty(table) == True:
            print('Table is empty -> not processed')
        else:
            if self.confirmOverwrite(filename):
                wbk = xlwt.Workbook()
                sheet = wbk.add_sheet(sheetname, cell_overwrite_ok=True)
                for i in range(0, table.rowCount()):
                    for j in range(0, table.columnCount()):
                        if self.cellIsEmpty(table, i, j) == False:
                            sheet.write(0, j, self.hHeader[j])                                  
                            sheet.write(i+1, j, float(table.item(i, j).text()))
                wbk.save(filename)
                print '%s was saved' % filename
                
    def combine_xls(self, filename, xlsfiles):
        wbk = xlwt.Workbook()
        for m in range(len(xlsfiles)):
            file_read = xlrd.open_workbook(xlsfiles[m])
            sh_read = file_read.sheet_by_index(0)
#            sh_write = wbk.add_sheet(str.split(str.split(xlsfiles[m],'.')[0],'_')[2])
            sh_write = wbk.add_sheet(str.split(xlsfiles[m],'.')[0])
            for j in range(len(sh_read.col_values(0))):
                for i in range(len(sh_read.row_values(0))):
                    sh_write.write(j,i,sh_read.cell(j,i).value)
        wbk.save(filename)              
                                 
#------------------------------------------------------------------------------    
    def updateIinmaxLbl(self):
        self.lblIinmax.setText(f0(float(self.keithleyIn.getIlim())*1e3) + ' mA')
    def updateIoutmaxLbl(self):
        self.lblIoutmax.setText(f0(float(self.keithleyOut.getIlim())*1e3) + ' mA') 
    def updateFreqLbl(self):
        self.lblFreq.setText(f2(self.ns2mhz(self.hp.getFreq())) + ' MHz')
    def updateVinLbl(self):
        self.lblVin.setText(f2(float(self.keithleyIn.getV())*1e3) + ' mV') 
    def updateVoutLbl(self):
        self.lblVout.setText(f2(float(self.keithleyOut.getV())*1e3) + ' mV')
    def updateGearLbl(self):     
        self.lblGear.setText('HIGH' if float(self.sourceGear.getV()) > 0.8 else 'LOW')      
    def updateFreqOn(self):
        self.lblFreqOn.setText('ON' if self.hp.getOutput()=='ON' else 'OFF')
    def updateVinOn(self):
        self.lblVinOn.setText('ON' if self.keithleyIn.getOutput()=='1' else 'OFF')
    def updateVoutOn(self):
        self.lblVoutOn.setText('ON' if self.keithleyOut.getOutput()=='1' else 'OFF')
    def updateGearOn(self):
        self.lblGearOn.setText('ON' if self.sourceGear.getOutput()=='1' else 'OFF')   
    def updateAllLbl(self):
        self.updateIinmaxLbl()
        self.updateIoutmaxLbl()
        self.updateFreqLbl()
        self.updateVinLbl()
        self.updateVoutLbl()
        self.updateGearLbl()
        self.updateFreqOn()
        self.updateVinOn()
        self.updateVoutOn()
        self.updateGearOn()     

#------------------------------------------------------------------------------        
    def buttonClicked(self):
        sender = self.sender()
        self.statusBar().showMessage(sender.text() + ' was pressed')            

#------------------------------------------------------------------------------        
    def calc(self, Vin, Vout, Iin, Iout):
        Pin = Vin*Iin
        Pout = Vout*Iout     
        Rload = Vout/Iout
        eta = Pout/Pin
        rho = Pout/self.AREA
        return eta, rho, Rload, Pin, Pout
        
    def closeEvent(self, event):
        print("Turning off and disconnecting devices ... \nClosing Window ... ")
        try:
            self.keithleyIn.close()
            self.hp.close()
            self.agilent.close()
            self.keithleyOut.close()  
        except Exception as e:
            print(str(e))   
    
    def withinLim(self, val, Max, Min):
        if  val > Max:
            print ('{0} > max = {1} -> not processed'.format(val, Max))
            WithinLim = False 
        elif val < Min:
            print ('{0} < min = {1} -> not processed'.format(val, Min))
            WithinLim = False 
        else:
            WithinLim = True
        return WithinLim
          
    def ns2mhz(self, ns):
        return 1/float(ns)*1e-6
    def mhz2ns(self, mhz):
        return 1/float(mhz)*1e-6    

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()
        if e.key() == QtCore.Qt.Key_Space:
            self.allOff()
        
    def confirmOverwrite(self, filename):
        if os.path.isfile(filename):
            quit_msg = "Overwrite %s?" % filename
            reply = QtGui.QMessageBox.question(self, 'Message', 
            quit_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.Yes:
                self.removeFile(filename)
                print 'Old %s was deleted' % filename  
                return True
            else:
                print '%s was not overwritten' % filename 
                return False 
        else: 
            return True

    def removeFile(self, files):
        if type(files) is list:
            for i in range(0,len(files)):
                os.remove(files[i])
        else:
            os.remove(files)
                    
    def openFile(self, filename):
        if os.path.isfile(filename):
            os.startfile(os.getcwd() +'\\' + filename)
        else:
            print('%s does not exist' % filename)
            
def main():
    
    app = QtGui.QApplication(sys.argv)
    SCCtrl = SCmeas()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
    
    
