#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
GUI to measure on-chip switched capacitor converter. Designed for 1mm2 converter on the champlain test site 
Toke Meyer Andersen, September 2014
"""

import sys, os
import hammerhead#
#import mplCanvas
#from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
import numpy as np
from PyQt4 import QtGui, QtCore

from PyQt4.QtGui import *
import xlwt
import xlrd
import time
#import subprocess

from INSTRUMENTS import devices

#
class SCmeas(QtGui.QMainWindow):
    def __init__(self):
        super(SCmeas, self).__init__()
        self.AREA = 1.9680 # converter area incl controller excl load in mm^2 - 4*(0.78*0.8-4*0.1*0.33)
        
        self.DEFAULTMODERLOADVOUT = 'Rsense'
        self.DEFAULTVIN = 2000 # mV
        self.DEFAULTVREF = 850 # mV
        self.DEFAULTVINHALFREF = 850 # mV        
        self.DEFAULTVLOGIC = 1000 # mV
        self.DEFAULTFREQ = 4000 # MHz
        self.DEFAULTFREQAMPLITUDE = 500 # mV
        self.DEFAULTFREQOFFSET = 500 # mV
        self.DEFAULTVRES = 1000 # mV
        
        self.DEFAULTIINLIM = 8000
#         self.DEFAULTVOUTSWEEP = [1100, 1100]
#         self.DEFAULTFREQSWEEP = [20, 200]
        self.DEFAULTVGEAR = 890
        
        self.DEFAULTENABLE = 1
        self.DEFAULTLOAD = 0
        self.DEFAULTLOADPROG = 0
        self.DEFAULTGEARPROG = 1
        self.DEFAULTGEARFIXED = 0
        self.DEFAULTSELECTN = 0
        self.DEFAULTOFFSETENABLE = 0
        self.DEFAULTOFFSET = 5 
        
        
        self.FREQLIM = [10, 4000.1] # MHz
        self.FREQAMPLITUDELIM = [100, 1000] # mV
        self.FREQOFFSETLIM = [100, 1000] # mV
        self.IOUTLIM = [1, 3000] # mA
        self.IINLIM = [1, 10000] # mA
        self.VINLIM = [1500, 3200] # mV
        self.VOUTMINLIM = 500
        self.VREFLIM = [500, 1250] # mV
        self.VINHALFREFLIM = [200, 1200] # mV        
        self.VLOGICLIM = [800, 1200] # mV
        
        self.ETAPLOT = [0, 100] # %
        self.RHOPLOT = [0, 10] # W/mm^2
        self.IOUTPLOT = [0, 50] # W/mm^2
        self.VOUTPLOT = [0, 1000] # W/mm^2
        
#         self.DEFAULTSETTLETIME = 3
        DEFAULTSLEEPTIME = 0.5
        self.DEFAULTRETENTION = 0;
        self.DEFAULTADJUSTVIN = True
        self.DEFAULTVINTARGET = 1800 # mV
        self.DEFAULTADJUSTVREF = True
        self.DEFAULTVREFMIN = 700 # mV
        self.DEFAULTVREFMAX = 1100 # mV
        self.DEFAULTVREFSTEP = 50 # mV
        self.DEFAULTRLOADRANGE = [1, 31]
        self.DEFAULTRLOADSTEP = 1
        
        self.initUI()
        self.devices = devices.Devices()
        self.devices.printInstrList()
#         self.allInit()
    def initUI(self):
        vMainBox, vMainLayout = self.addVWidget()
        self.setCentralWidget(vMainBox)    
        hMainBox, hMainLayout = self.addHWidget()
                   
        vMainLayout.addWidget(self.initButtons())
        vMainLayout.addWidget(hMainBox)
        hMainLayout.addWidget(self.setOnMeasButtons())
        hMainLayout.addWidget(self.setSweepButtons())
        
        self.statusBar()
#         self.setGeometry(25, 25, 1400, 700)
        self.showMaximized()
        self.setWindowTitle('10W SCVR Control Window')
        self.show()
    
    def initButtons(self):
        v0Box, v0Layout = self.addVWidget()
        
        btnInitHp = QtGui.QPushButton("Init Freq", self)
        btnInitHp.clicked.connect(self.initClicked)
        btnInitAgilent = QtGui.QPushButton("Init Agilent", self)
        btnInitAgilent.clicked.connect(self.initClicked)
        btnInitKeithleyIn = QtGui.QPushButton("Init KeithleyIn", self)
        btnInitKeithleyIn.clicked.connect(self.initClicked)
        btnInitKeithleyOut = QtGui.QPushButton("Init KeithleyOut", self)
        btnInitKeithleyOut.clicked.connect(self.initClicked)
        btnInitKeithleyVoutk = QtGui.QPushButton("Init KeithleyVoutk", self)
        btnInitKeithleyVoutk.clicked.connect(self.initClicked)        
        btnInitVref = QtGui.QPushButton("Init Vref", self)
        btnInitVref.clicked.connect(self.initClicked)
        btnInitVinhalfref = QtGui.QPushButton("Init Vinhalfref", self)
        btnInitVinhalfref.clicked.connect(self.initClicked)
        btnInitVlogic = QtGui.QPushButton("Init Vlogic", self)
        btnInitVlogic.clicked.connect(self.initClicked)
        btnConnectHammerhead = QtGui.QPushButton("Conn. hammerhead", self)
        btnConnectHammerhead.clicked.connect(self.initClicked)
        btnInitHammerhead = QtGui.QPushButton("Init hammerhead", self)
        btnInitHammerhead.clicked.connect(self.initClicked)
        btnInitAll = QtGui.QPushButton("Init all", self)
        btnInitAll.clicked.connect(self.initClicked)
        
        h0Box, h0Layout = self.addHWidget()
        v0Layout.addWidget(h0Box)          
        h0Layout.addWidget(btnInitHp)
        h0Layout.addWidget(btnInitAgilent)
        h0Layout.addWidget(btnInitKeithleyIn)
        h0Layout.addWidget(btnInitKeithleyOut)
        h0Layout.addWidget(btnInitKeithleyVoutk)
        h0Layout.addWidget(btnInitVref)
        h0Layout.addWidget(btnInitVinhalfref)        
        h0Layout.addWidget(btnInitVlogic)
        h0Layout.addWidget(btnConnectHammerhead)
        h0Layout.addWidget(btnInitHammerhead)
        h0Layout.addWidget(btnInitAll) 
                   
        v0Box.setMaximumHeight(100)
        v0Box.setMaximumWidth(950)
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
        
        self.leFreq = QtGui.QLineEdit(str(self.DEFAULTFREQ), self)
        self.leFreq.setObjectName("Set freq [MHz]")
        self.leFreq.returnPressed.connect(self.setClicked)        
        self.btnFreq = QtGui.QPushButton("Set freq [MHz]", self)
        self.btnFreq.clicked.connect(self.setClicked)            
        self.lblFreq = QtGui.QLabel('-', self)
        v0Layout.addWidget(self.addHTripleWidget(self.leFreq, self.btnFreq, self.lblFreq))    
        
        self.leFreqAmplitude = QtGui.QLineEdit(str(self.DEFAULTFREQAMPLITUDE), self)
        self.leFreqAmplitude.setObjectName("Set freq mag [mV]")
        self.leFreqAmplitude.returnPressed.connect(self.setClicked)        
        self.btnFreqAmplitude = QtGui.QPushButton("Set freq mag [mV]", self)
        self.btnFreqAmplitude.clicked.connect(self.setClicked)            
        self.lblFreqAmplitude = QtGui.QLabel('-', self)
        v0Layout.addWidget(self.addHTripleWidget(self.leFreqAmplitude, self.btnFreqAmplitude, self.lblFreqAmplitude))           
        
        self.leFreqOffset = QtGui.QLineEdit(str(self.DEFAULTFREQOFFSET), self)
        self.leFreqOffset.setObjectName("Set freq offset [mV]")
        self.leFreqOffset.returnPressed.connect(self.setClicked)        
        self.btnFreqOffset = QtGui.QPushButton("Set freq offset [mV]", self)
        self.btnFreqOffset.clicked.connect(self.setClicked)            
        self.lblFreqOffset = QtGui.QLabel('-', self)
        v0Layout.addWidget(self.addHTripleWidget(self.leFreqOffset, self.btnFreqOffset, self.lblFreqOffset))              

        self.leVref = QtGui.QLineEdit(str(self.DEFAULTVREF), self)
        self.leVref.setObjectName("Set Vref [mV]")
        self.leVref.returnPressed.connect(self.setClicked)        
        self.btnVref = QtGui.QPushButton("Set Vref [mV]", self)
        self.btnVref.clicked.connect(self.setClicked)            
        self.lblVref = QtGui.QLabel('-', self)
        v0Layout.addWidget(self.addHTripleWidget(self.leVref, self.btnVref, self.lblVref))       
        
        self.leVinhalfref = QtGui.QLineEdit(str(self.DEFAULTVINHALFREF), self)
        self.leVinhalfref.setObjectName("Set Vinhalfref [mV]")
        self.leVinhalfref.returnPressed.connect(self.setClicked)        
        self.btnVinhalfref = QtGui.QPushButton("Set Vrefinhalf [mV]", self)
        self.btnVinhalfref.clicked.connect(self.setClicked)            
        self.lblVinhalfref = QtGui.QLabel('-', self)
        v0Layout.addWidget(self.addHTripleWidget(self.leVinhalfref, self.btnVinhalfref, self.lblVinhalfref))             
        
        self.leVlogic = QtGui.QLineEdit(str(self.DEFAULTVLOGIC), self)
        self.leVlogic.setObjectName("Set Vlogic [mV]")
        self.leVlogic.returnPressed.connect(self.setClicked)
        self.btnVlogic = QtGui.QPushButton("Set Vlogic [mV]", self)
        self.btnVlogic.clicked.connect(self.setClicked)
        self.lblVlogic = QtGui.QLabel('-', self)
        v0Layout.addWidget(self.addHTripleWidget(self.leVlogic, self.btnVlogic, self.lblVlogic))    
        
        self.leVin = QtGui.QLineEdit(str(self.DEFAULTVIN), self)
        self.leVin.setObjectName("Set Vin [mV]")
        self.leVin.returnPressed.connect(self.setClicked)        
        self.btnVin = QtGui.QPushButton("Set Vin [mV]", self)
        self.btnVin.clicked.connect(self.setClicked)            
        self.lblVin = QtGui.QLabel('-', self)
        v0Layout.addWidget(self.addHTripleWidget(self.leVin, self.btnVin, self.lblVin))                           

        self.btnMonChan = QtGui.QPushButton("Toggle mon chan", self)
        self.btnMonChan.clicked.connect(self.setClicked) 
        self.btnSetAll = QtGui.QPushButton("Set all", self)
        self.btnSetAll.clicked.connect(self.setClicked)        
        v0Layout.addWidget(self.addHTripleWidget(self.btnMonChan, self.btnSetAll, self.lblEmpty()))  

        v0Layout.addWidget(self.addHTripleWidget(self.lblEmpty(), self.lblEmpty(), self.lblEmpty()))                      
#------------------------------------------------------------------------------                          
        
        self.btnVlogicOn = QtGui.QPushButton("Vlogic on/off", self)
        self.btnVlogicOn.clicked.connect(self.onClicked)            
        self.lblVlogicOn = QtGui.QLabel('-', self)
        v0Layout.addWidget(self.addHTripleWidget(self.lblEmpty(), self.btnVlogicOn, self.lblVlogicOn))
        
        self.btnFreqOn = QtGui.QPushButton("Freq on/off", self)
        self.btnFreqOn.clicked.connect(self.onClicked)            
        self.lblFreqOn = QtGui.QLabel('-', self) 
        v0Layout.addWidget(self.addHTripleWidget(self.lblEmpty(), self.btnFreqOn, self.lblFreqOn))              
                
        self.btnVrefOn = QtGui.QPushButton("Vref on/off", self)
        self.btnVrefOn.clicked.connect(self.onClicked)            
        self.lblVrefOn = QtGui.QLabel('-', self)
        v0Layout.addWidget(self.addHTripleWidget(self.lblEmpty(), self.btnVrefOn, self.lblVrefOn))    
        
        self.btnVinhalfrefOn = QtGui.QPushButton("Vinhalfref on/off", self)
        self.btnVinhalfrefOn.clicked.connect(self.onClicked)            
        self.lblVinhalfrefOn = QtGui.QLabel('-', self)
        v0Layout.addWidget(self.addHTripleWidget(self.lblEmpty(), self.btnVinhalfrefOn, self.lblVinhalfrefOn))            
        
        self.btnVinOn = QtGui.QPushButton("Vin on/off", self)
        self.btnVinOn.clicked.connect(self.onClicked)            
        self.lblVinOn = QtGui.QLabel('-', self)
        v0Layout.addWidget(self.addHTripleWidget(self.lblEmpty(), self.btnVinOn, self.lblVinOn))                   
        
        self.btnAllOn = QtGui.QPushButton("All on/ Init regs", self)
        self.btnAllOn.clicked.connect(self.onClicked)             
        self.btnAllOff = QtGui.QPushButton("All off", self)
        self.btnAllOff.clicked.connect(self.onClicked)
        v0Layout.addWidget(self.addHTripleWidget(self.lblEmpty(), self.btnAllOn, self.btnAllOff))    

        v0Layout.addWidget(self.addHTripleWidget(self.lblEmpty(), self.lblEmpty(), self.lblEmpty()))

        self.leEnable = QtGui.QLineEdit(str(self.DEFAULTENABLE), self)
        self.leEnable.setObjectName("Set Enable")
        self.leEnable.returnPressed.connect(self.setClicked)  
        self.leLoad = QtGui.QLineEdit(str(self.DEFAULTLOAD), self)
        self.leLoad.setObjectName("Set Load")
        self.leLoad.returnPressed.connect(self.setClicked)
        self.lblEnable = QtGui.QLabel('Enable: -', self)
        self.lblLoad = QtGui.QLabel('Load: -', self)      
        self.btnSetEnableLoadReg = QtGui.QPushButton("Set EL Reg", self)
        self.btnSetEnableLoadReg.clicked.connect(self.setClicked)        
        v0Layout.addWidget(self.addHTripleWidget(self.lblEnable, self.lblLoad, self.lblEmpty()))
        v0Layout.addWidget(self.addHTripleWidget(self.leEnable, self.leLoad, self.btnSetEnableLoadReg))           

        self.leLoadProg = QtGui.QLineEdit(str(self.DEFAULTLOADPROG), self)
        self.leLoadProg.setObjectName("LoadProg")
        self.leLoadProg.returnPressed.connect(self.setClicked)  
        self.leGearProg = QtGui.QLineEdit(str(self.DEFAULTGEARPROG), self)
        self.leGearProg.setObjectName("GearProg")
        self.leGearProg.returnPressed.connect(self.setClicked)
        self.leGearFixed = QtGui.QLineEdit(str(self.DEFAULTGEARFIXED), self)
        self.leGearFixed.setObjectName("GearFixed")        
        self.leGearFixed.returnPressed.connect(self.setClicked)
        
        self.lblLoadProg = QtGui.QLabel('LoadProg: -', self)
        self.lblGearProg = QtGui.QLabel('GearProg: -', self) 
        self.lblGearFixed = QtGui.QLabel('GearFixed: -', self)
        v0Layout.addWidget(self.addHTripleWidget(self.lblLoadProg, self.lblGearProg, self.lblGearFixed))
        v0Layout.addWidget(self.addHTripleWidget(self.leLoadProg, self.leGearProg, self.leGearFixed))            
        
        self.leSelectn = QtGui.QLineEdit(str(self.DEFAULTSELECTN), self)
        self.leSelectn.setObjectName("Selectn")
        self.leSelectn.returnPressed.connect(self.setClicked)  
        self.leOffsetEnable = QtGui.QLineEdit(str(self.DEFAULTOFFSETENABLE), self)
        self.leOffsetEnable.setObjectName("Set Offset Enable")
        self.leOffsetEnable.returnPressed.connect(self.setClicked)
        self.leOffset = QtGui.QLineEdit(str(self.DEFAULTOFFSET), self)
        self.leOffset.setObjectName("Set Offset")        
        self.leOffset.returnPressed.connect(self.setClicked)        

        self.lblSelectn = QtGui.QLabel('Selectn: -', self)
        self.lblOffsetEnable = QtGui.QLabel('Offset Enable: -', self) 
        self.lblOffset = QtGui.QLabel('Offset: -', self)       
        v0Layout.addWidget(self.addHTripleWidget(self.lblSelectn, self.lblOffsetEnable, self.lblOffset))
        v0Layout.addWidget(self.addHTripleWidget(self.leSelectn, self.leOffsetEnable, self.leOffset))               

  
        self.btnResetRegs = QtGui.QPushButton("Reset regs", self)
        self.btnResetRegs.clicked.connect(self.setClicked)                  
        self.btnConfig = QtGui.QPushButton("Set Config Reg", self)
        self.btnConfig.clicked.connect(self.setClicked)                
        v0Layout.addWidget(self.addHTripleWidget(self.lblEmpty(), self.btnResetRegs, self.btnConfig))

        v0Layout.addWidget(self.addHTripleWidget(self.lblEmpty(), self.lblEmpty(), self.lblEmpty()))    
       
#------------------------------------------------------------------------------         
        self.checkMeasAllAdjustVin = QCheckBox("Adj.Vin @ All", self)
        self.checkMeasAllAdjustVin.setChecked(self.DEFAULTADJUSTVIN)
        self.btnTargetVink = QtGui.QPushButton("Adjust Vink to", self)
        self.btnTargetVink.clicked.connect(self.measClicked) 
        self.leTargetVink = QtGui.QLineEdit(str(self.DEFAULTVINTARGET), self)
        self.leTargetVink.setObjectName("Adjust Vink to")
        self.leTargetVink.returnPressed.connect(self.measClicked)
        v0Layout.addWidget(self.addHTripleWidget(self.checkMeasAllAdjustVin, self.btnTargetVink, self.leTargetVink))
        
        self.checkMeasAllAdjustVout = QCheckBox("Adj.Vout @ All", self)
        self.checkMeasAllAdjustVout.setChecked(self.DEFAULTADJUSTVREF)   
        self.btnTargetVoutk = QtGui.QPushButton("Adjust Voutk to", self)
        self.btnTargetVoutk.clicked.connect(self.measClicked)
        self.leTargetVoutk = QtGui.QLineEdit(str(self.DEFAULTVREF), self)
        self.leTargetVoutk.setObjectName("Adjust Voutk to")     
        self.leTargetVoutk.returnPressed.connect(self.measClicked)
        v0Layout.addWidget(self.addHTripleWidget(self.checkMeasAllAdjustVout, self.btnTargetVoutk, self.leTargetVoutk))            
    
        self.btnIin = QtGui.QPushButton("Meas Iin", self)
        self.btnIin.clicked.connect(self.measClicked)            
        self.lblIin = QtGui.QLabel('-', self)
        self.leRetention = QtGui.QLineEdit(str(self.DEFAULTRETENTION), self)
        self.leRetention.setObjectName("Retention")
        self.leRetention.returnPressed.connect(self.measClicked)        
        v0Layout.addWidget(self.addHTripleWidget(self.leRetention, self.btnIin, self.lblIin))      
        
        self.btnVink = QtGui.QPushButton("Meas Vink", self)
        self.btnVink.clicked.connect(self.measClicked)            
        self.lblVink = QtGui.QLabel('-', self)
        self.lblRetention = QtGui.QLabel('Retention: {0}'.format(self.DEFAULTRETENTION), self)
        v0Layout.addWidget(self.addHTripleWidget(self.lblRetention, self.btnVink, self.lblVink))
        
        self.btnToggleRloadVout = QtGui.QPushButton("toggle Rload/Vout", self)
        self.btnToggleRloadVout.clicked.connect(self.measClicked)        
        self.btnRloadVout = QtGui.QPushButton("Meas Rload" if self.DEFAULTMODERLOADVOUT == 'Rsense' else "Meas Voutk", self)
        self.btnRloadVout.clicked.connect(self.measClicked)            
        self.lblRloadVout = QtGui.QLabel('-', self) 
        v0Layout.addWidget(self.addHTripleWidget(self.btnToggleRloadVout, self.btnRloadVout, self.lblRloadVout))           
  
        self.btnAll = QtGui.QPushButton("Meas All", self)
        self.btnAll.clicked.connect(self.measClicked)            
        self.lblAll = QtGui.QLabel('-', self) 
        v0Layout.addWidget(self.addHTripleWidget(self.lblEmpty(), self.btnAll, self.lblAll))
        
        self.btnExit = QtGui.QPushButton("Exit", self)
        self.btnExit.clicked.connect(self.exitClicked)       
        v0Layout.addWidget(self.addHTripleWidget(self.btnExit, self.lblEmpty(), self.lblEmpty()))
        
        v0Box.setMaximumWidth(400)
        return v0Box 
    
    def setSweepButtons(self):
        v0Box, v0Layout = self.addVWidget() 
        
        h0Box, h0Layout = self.addHWidget() 
        v0Layout.addWidget(h0Box)
         
        self.lblTemp = QtGui.QLabel('Temp [C]', self) 
        self.leTemp = QtGui.QLineEdit("25", self)
        self.leTemp.setObjectName("RloadoverTemp")
        self.leTemp.returnPressed.connect(self.measClicked) 
        self.btnRloadoverTemp = QtGui.QPushButton("RloadoverTemp", self)
        self.btnRloadoverTemp.clicked.connect(self.measClicked)
        h0Layout.addWidget(self.addVTripleWidget(self.lblTemp, self.leTemp,self.btnRloadoverTemp))
        
        self.btnClearMessTable = QtGui.QPushButton("Clear table only", self)
        self.btnClearMessTable.clicked.connect(self.measClicked)
        self.btnSweep = QtGui.QPushButton("Sweep Load", self)
        self.btnSweep.clicked.connect(self.measClicked)        
        h0Layout.addWidget(self.addVTripleWidget(self.btnClearMessTable, self.lblEmpty(), self.btnSweep))
        
        self.btnOpenMeasTable = QtGui.QPushButton("Open in Excel", self)
        self.btnOpenMeasTable.clicked.connect(self.measClicked)
        self.leSaveMeasTable = QtGui.QLineEdit("meas.xls", self)
        self.btnSaveMeasTable = QtGui.QPushButton("Save table", self)
        self.btnSaveMeasTable.clicked.connect(self.measClicked)
        h0Layout.addWidget(self.addVTripleWidget(self.btnOpenMeasTable, self.leSaveMeasTable, self.btnSaveMeasTable))
        
        self.leVgear = QtGui.QLineEdit(str(self.DEFAULTVGEAR), self)
        self.lblVgear = QtGui.QLabel('Vgear change [mV]', self)
        h0Layout.addWidget(self.addVTripleWidget(self.lblEmpty(), self.lblVgear, self.leVgear))
                
        self.leRloadMin = QtGui.QLineEdit(str(self.DEFAULTRLOADRANGE[0]), self)
        self.leRloadMax = QtGui.QLineEdit(str(self.DEFAULTRLOADRANGE[1]), self)
        self.leRloadStep = QtGui.QLineEdit(str(self.DEFAULTRLOADSTEP), self)
        h0Layout.addWidget(self.addVTripleWidget(self.leRloadMin, self.leRloadMax, self.leRloadStep)) 
        
        self.lblRloadMin = QtGui.QLabel('Rload min', self)
        self.lblRloadMax = QtGui.QLabel('Rload max', self)
        self.lblRloadStep = QtGui.QLabel('Rload step', self)
        h0Layout.addWidget(self.addVTripleWidget(self.lblRloadMin, self.lblRloadMax, self.lblRloadStep))         
        
        self.leVrefMin = QtGui.QLineEdit(str(self.DEFAULTVREFMIN), self)
        self.leVrefMax = QtGui.QLineEdit(str(self.DEFAULTVREFMAX), self)
        self.leVrefStep = QtGui.QLineEdit(str(self.DEFAULTVREFSTEP), self)
        h0Layout.addWidget(self.addVTripleWidget(self.leVrefMin, self.leVrefMax, self.leVrefStep))        
        
        self.lblVrefMin = QtGui.QLabel('Vref/Vout min [mV]', self)
        self.lblVrefMax = QtGui.QLabel('Vref/Vout max [mV]', self)
        self.lblVrefStep = QtGui.QLabel('Vref/Vout step [mV]', self)
        h0Layout.addWidget(self.addVTripleWidget(self.lblVrefMin, self.lblVrefMax, self.lblVrefStep))   
                
#        self.btnOpenSweep = QtGui.QPushButton("Open sweep Excel", self)
#        self.btnOpenSweep.clicked.connect(self.measClicked)
        self.lblChipNumber = QtGui.QLabel('Chip Name', self)
        self.leSweepLoadVref = QtGui.QLineEdit("Chip1", self)
        self.btnSweepLoadVrefVout = QtGui.QPushButton("Sweep Load && Vref", self)
        self.btnSweepLoadVrefVout.clicked.connect(self.measClicked)
        h0Layout.addWidget(self.addVTripleWidget(self.lblChipNumber, self.leSweepLoadVref, self.btnSweepLoadVrefVout))
        
        self.lblMeasEverythingVin = QtGui.QLabel('Vintarget list', self)
        self.leMeasEverythingVin = QtGui.QLineEdit(str(self.DEFAULTVIN), self)
        self.lblMeasEverythingFreq = QtGui.QLabel('Freq list', self)
        self.leMeasEverythingFreq = QtGui.QLineEdit(str(self.DEFAULTFREQ), self)
        self.btnMeasEverything = QtGui.QPushButton("Meas Everything!", self)
        self.btnMeasEverything.clicked.connect(self.measClicked)
        h0Layout.addWidget(self.addVTripleWidget(self.lblMeasEverythingVin, self.lblMeasEverythingFreq, self.lblEmpty()))
        h0Layout.addWidget(self.addVTripleWidget(self.leMeasEverythingVin, self.leMeasEverythingFreq, self.btnMeasEverything))
        
        tab = QTabWidget()
        tab.addTab(self.createTableTab(), 'Meas Table')
        v0Layout.addWidget(tab)

#        v0Box.setMaximumWidth(1050)
        return v0Box 

    def createTableTab(self):
        v0Box, v0Layout = self.addVWidget()
        self.hHeader = ["fast_ck [MHz]", "Iin [mA]", "Iout [mA]", "Vink [mV]", "Vins [mV]", "Voutk [mV]", "Vref [mV]", "Rload [ohm]", "Pin [mW]", "Pout [mW]", "eta [%]", "rho [W/mm2]", "", ""]
        self.vHeader = range(self.DEFAULTRLOADRANGE[0], 100)
        self.rowNumber = self.DEFAULTRLOADRANGE[0]
#         self.vHeader = range(0, 100)
#         self.rowNumber = 0
        self.measTbl = self.createTable(self.hHeader, self.vHeader, 80, 18)
        v0Layout.addWidget(self.measTbl)
        return v0Box    
        
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
            self.allOff()
        except Exception as e:
            self.status('')
        try:
            self.devices = devices.Devices()
#             self.devices.printInstrList()
            self.addr0 = '-'
            self.addr1 = '-'
            self.hammerheadIsInitialized = False
#             self.Rload = list() # Moved under 'all init' 
#             self.columnNumber = 0 # Moved under 'all init' 
            if self.sender().text() == "Init Freq":
                self.freqInit()
            if self.sender().text() == "Init Agilent":
                self.agilentInit()
            if self.sender().text() == "Init KeithleyIn":
                self.keithleyInInit()
#            if self.sender().text() == "Init KeithleyOut":
#                self.keithleyOutInit()
            if self.sender().text() == "Init KeithleyVoutk":
                self.keithleyVoutkInit()
            if self.sender().text() == "Init KeithleyOut":
                self.keithleyOutInit()
            if self.sender().text() == "Init Vref":
                self.vrefInit()     
            if self.sender().text() == "Init Vinhalfref":
                self.vinhalfrefInit()                     
            if self.sender().text() == "Init Vlogic":
                self.vlogicInit()                              
            if self.sender().text() == "Conn. hammerhead":
                self.connectHammerhead()   
            if self.sender().text() == "Init hammerhead":
                self.initHammerhead()                   
            if self.sender().text() == "Init all":
                self.allInit()    
            if self.sender().text() == "Exit":
                self.close()  
        except Exception as e:
            print(str(e))                              
    def freqInit(self):
        self.freq = agilent8648D.Agilent8648D()
        print ('freq = ' + self.freq.initme(self.devices, '8648D', self.DEFAULTFREQ, self.DEFAULTFREQAMPLITUDE))
        self.freqOffset = agilentDC.AgilentDC()
        print ('freqOffset = ' + self.freqOffset.initme(self.devices, 7, self.DEFAULTFREQOFFSET*1e-3, 0.02))
        self.leFreq.setText(str(self.DEFAULTFREQ))
        self.leFreqAmplitude.setText(str(self.DEFAULTFREQAMPLITUDE))
        self.leFreqOffset.setText(str(self.DEFAULTFREQOFFSET))
        self.updateFreqLbl()
        self.updateFreqAmplitudeLbl()
        self.updateFreqOffsetLbl()
        self.updateFreqOn()
    def agilentInit(self):
        self.agilent = agilent.Agilent() 
        self.lblVink.setText('-')  
        print('agilent = ' + self.agilent.initme(self.devices, '34970A'))      
    def keithleyInInit(self):
#         self.keithleyIn = keithley.Keithley()
#         print('keithleyIn = ' + self.keithleyIn.initme(self.devices, '2420', 'Isense', self.DEFAULTVIN*1e-3, self.VINLIM[1]*1e-3))         
#         self.keithleyIn.setIlim(self.DEFAULTIINLIM*1e-3)
#         self.keithleyIn.setIrange(3 if self.DEFAULTIINLIM >= 1000 else 1)
        self.keithleyIn = agilentDC.AgilentDC()
        print('keithleyIn = ' + self.keithleyIn.initme(self.devices, 'E3633', self.DEFAULTVIN*1e-3, self.DEFAULTIINLIM*1e-3))         
        self.keithleyIn.setIlim(self.IINLIM[1]*1e-3)
        self.keithleyIn.setVlim(self.VINLIM[1]*1e-3)
        self.leVin.setText(str(self.DEFAULTVIN))
        self.lblVink.setText('-')
        self.lblIin.setText('-')
        self.updateVinLbl()
        self.updateIinmaxLbl()
        self.updateVinOn()           
    def keithleyOutInit(self):
        self.keithleyOut = keithley.Keithley()
        self.lblRloadVout.setText('-')
        self.modeRloadVout = self.DEFAULTMODERLOADVOUT
        print('keithleyOut = ' + self.keithleyOut.initme(self.devices, '2400', self.modeRloadVout, 0, 2))
        if self.modeRloadVout == 'Vsense':
            self.modeRloadVout = 'Rsense'
        elif self.modeRloadVout == 'Rsense':
            self.modeRloadVout = 'Vsense'
        self.measToggleRloadVout()
    def keithleyVoutkInit(self):
        self.keithleyVoutk = keithley.Keithley()
        print('keithleyVoutk = ' + self.keithleyVoutk.initme(self.devices, '2420', "Vsense", self.DEFAULTVREF, self.DEFAULTVREFMAX))
    def vrefInit(self):
        self.vref = agilentDC.AgilentDC()
        print('Vref = ' + self.vref.initme(self.devices, 12, self.DEFAULTVREF*1e-3, 0.030))    
        self.leVref.setText(str(self.DEFAULTVREF))
        self.updateVrefOn()
    def vinhalfrefInit(self):
        self.vinhalfref = agilentDC.AgilentDC()
        print('Vinhalfref = ' + self.vinhalfref.initme(self.devices, 11, self.DEFAULTVINHALFREF*1e-3, 0.030))    
        self.leVinhalfref.setText(str(self.DEFAULTVINHALFREF))
        self.updateVinhalfrefOn()        
        self.updateVinhalfrefLbl()        
    def vlogicInit(self):
        self.vlogic = agilentDC.AgilentDC()
        print('Vlogic = ' + self.vlogic.initme(self.devices, 10, self.DEFAULTVLOGIC*1e-3, 0.1))    
        self.leVlogic.setText(str(self.DEFAULTVLOGIC))
        self.updateVlogicOn()
        self.updateVlogicLbl()           
    def connectHammerhead(self):
        self.h = hammerhead.Hammerhead()
        self.h.connect()
        self.status("connected")        
    def initHammerhead(self):
        self.h.init()
        self.status('Initialized.')   
        self.hammerheadIsInitialized = True         
    def allInit(self):
        self.Rload = list()
        self.columnNumber = 0
        self.freqInit()   
        self.agilentInit() 
        self.keithleyInInit()   
        self.keithleyVoutkInit()
        self.keithleyOutInit() 
        self.vrefInit()
        self.vinhalfrefInit()
        self.vlogicInit()
        self.connectHammerhead()
        self.initHammerhead()
        self.updateAllLbl()
    def exitClicked(self):
        try: 
            self.allOff()
        except Exception as e:
            self.status('...')
        self.status('Exiting...')
        self.close()                  
#------------------------------------------------------------------------------

    def onClicked(self):
        self.buttonClicked()
        try:
            if self.sender().text() == "Freq on/off":
                self.freqOnOff()
            if self.sender().text() == "Vin on/off":
                self.vinOnOff()
            if self.sender().text() == "Vref on/off":
                self.vrefOnOff()
            if self.sender().text() == "Vinhalfref on/off":
                self.vinhalfrefOnOff()                
            if self.sender().text() == "Vlogic on/off":
                self.vlogicOnOff()                                
            if self.sender().text() == "All on/ Init regs":
                self.allOn()
            if self.sender().text() == "All off":
                self.allOff()                                                                            
        except Exception as e:
            print(str(e))   
    def freqOnOff(self):
        if self.freqIsOn()==False:
            self.freq.setOutput('ON')
            self.freqOffset.setOutput('ON')
        elif self.freqIsOn() and self.vinIsOn():
            self.status('Vin is on. Freq is not turned off')
        else:            
            self.freq.setOutput('OFF')
            self.freqOffset.setOutput('OFF')            
        self.updateFreqOn() 
    def vinOnOff(self):
        if not self.modeRloadVout == 'Vsense':
            self.measToggleRloadVout()
            time.sleep(0.1)
        if self.lblEnable.text() == 'Enable: {0}'.format(self.DEFAULTENABLE) and self.lblLoad.text() == 'Load: 0' and self.vinIsOn() == False:
            if self.freqIsOn() and self.vlogicIsOn() and self.vrefIsOn():
                self.keithleyIn.outputOn()
                self.updateVinOn()
                self.setEnable(0)
                self.setEnable(1)
                time.sleep(0.25)
                self.measVoutk()
                self.measIin()
                self.measVink()
            else: self.status('Freq, freqOffset or Vlogic is not on -> no registers are written ...')  
        elif self.vinIsOn():
            self.keithleyIn.outputOff()
            self.setLoad(0)
        else: self.status('addr0={0} is not correctly initialized -> Vin is not turned on'.format(self.addr0))
        self.updateVinOn()   
    def vrefOnOff(self):  
        if self.vrefIsOn() == False:
            self.vref.setOutput('ON')
        elif self.vrefIsOn() and self.vinIsOn():
            self.status('Vin is on. Vref is not turned off')
        else: self.vref.setOutput('OFF')
        self.updateVrefOn()  
        self.updateVrefLbl()     
    def vinhalfrefOnOff(self):  
        if self.vinhalfrefIsOn() == False:
            self.vinhalfref.setOutput('ON')
        elif self.vinhalfrefIsOn() and self.vinIsOn():
            self.status('Vin is on. Vinhalfref is not turned off')
        else: self.vinhalfref.setOutput('OFF')
        self.updateVinhalfrefOn()  
        self.updateVinhalfrefLbl()             
    def vlogicOnOff(self):   
        if self.vlogicIsOn() == False:
            if self.freqIsOn() == False: self.freqOnOff()
            time.sleep(1)
            self.vlogic.setOutput('ON')
            self.updateVlogicOn()
            time.sleep(1)
            
            self.resetRegs()
#            self.resetRegs()
        elif self.vlogicIsOn() and self.vinIsOn():
            self.status('Vin is on. Vlogic is not turned off')
        else: self.vlogic.setOutput('OFF')
        self.updateVlogicOn()
    def allOn(self):
        self.allOff()
        time.sleep(0.25)
        self.freqOnOff()
        time.sleep(0.25)
        self.vlogicOnOff()
        self.vrefOnOff()
        self.vinhalfrefOnOff()        
        time.sleep(0.25)
        self.leVin.setText(str(self.DEFAULTVIN))
        self.setVin(self.DEFAULTVIN)
        self.vinOnOff()
    def allOff(self):
        self.keithleyIn.outputOff()
        self.updateAllLbl()
        time.sleep(1)        
        self.vref.outputOff()
        self.vinhalfref.outputOff()      
        self.freq.outputOff()
        self.freqOffset.outputOff()
        self.vlogic.outputOff()  
        self.updateAllLbl()
    def isAllOn(self):
        if self.freqIsOn() and self.vrefIsOn() and self.vinhalfrefIsOn() and self.vlogicIsOn() and self.vinIsOn():
            return True
        else:
            self.status('Not all measurement equipment is turned on -> No measurements performed')
            return False
    def vinIsOn(self):
        return (True if self.keithleyIn.getOutput() == '1' else False)
    def freqIsOn(self):
        return (True if self.freq.getOutput() == '1' and self.freqOffset.getOutput() == '1' else False)    
    def vrefIsOn(self):
        return (True if self.vref.getOutput() == '1' else False)
    def vinhalfrefIsOn(self):
        return (True if self.vinhalfref.getOutput() == '1' else False)    
    def vlogicIsOn(self):
        return (True if self.vlogic.getOutput() == '1' else False)    
    def resetRegs(self):
        if self.vlogicIsOn() and self.freqIsOn():
#             self.setFreq(1000)
#             self.h.init()
            self.leEnable.setText(str(0))
            self.setLoad(0)
            self.setEnableLoadReg()
            self.setEnableLoadReg()
            self.setEnableLoadReg()
            self.setEnableLoadReg()
            time.sleep(0.5)
            self.leLoad.setText(str(self.DEFAULTLOAD))
            self.leLoadProg.setText(str(self.DEFAULTLOADPROG))
            self.leGearProg.setText(str(self.DEFAULTGEARPROG))
            self.leGearFixed.setText(str(self.DEFAULTGEARFIXED))
            self.leSelectn.setText(str(self.DEFAULTSELECTN))
            self.leOffsetEnable.setText(str(self.DEFAULTOFFSETENABLE))  
            self.leOffset.setText(str(self.DEFAULTOFFSET))
            self.setEnableLoadReg()
            self.setConfig()  
            self.leEnable.setText(str(self.DEFAULTENABLE)) 
            self.setEnableLoadReg()  
#             self.setFreq(self.DEFAULTFREQ)  
            self.leRetention.setText(str(self.DEFAULTRETENTION))
            self.measRetention()    
            return True
        else: self.status('Freq, freqOffset or Vlogic is not on -> no registers are written ...')   
        
#------------------------------------------------------------------------------
    def setClicked(self):
        self.buttonClicked()
        try:
            if not str(self.sender().objectName()):
                textObject = str(self.sender().text())
            else:
                textObject = str(self.sender().objectName())
#             print textObject 
            Iinmax  = float(self.leIinmax.text())
            Freq    = float(self.leFreq.text())
            FreqAmplitude = float(self.leFreqAmplitude.text())
            FreqOffset = float(self.leFreqOffset.text())
            Vin     = float(self.leVin.text())
            Vref = float(self.leVref.text())
            Vinhalfref = float(self.leVinhalfref.text())            
            Vlogic = float(self.leVlogic.text())
            if textObject == "Set max Iin [mA]":
                self.setIinmax(Iinmax)
            if textObject == "Set freq [MHz]":
                self.setFreq(Freq)
            if textObject == "Set freq mag [mV]":
                self.setFreqAmplitude(FreqAmplitude)                    
            if textObject == "Set freq offset [mV]":
                self.setFreqOffset(FreqOffset)                
            if textObject == "Set Vin [mV]":
                self.setVin(Vin)
            if textObject == "Set Vref [mV]":
                self.setVref(Vref)
            if textObject == "Set Vinhalfref [mV]":
                self.setVinhalfref(Vinhalfref)                
            if textObject == "Set Vlogic [mV]":
                self.setVlogic(Vlogic)                
            if any(textObject in s for s in ["Set EL Reg", "Set Enable", "Set Load"]):
                self.setEnableLoadReg(meas=True)           
            if any(textObject in s for s in ["Set Config Reg", "LoadProg", "GearProg", "GearFixed", "Selectn", "Set Offset Enable", "Offset"]):
                self.setConfig()
            if textObject == "Reset regs":
                self.resetRegs()                                     
            if textObject == "Set all":
                self.setAll(Iinmax, Freq, Vin)
            if textObject == "Toggle mon chan":
                self.toggleMonChan()                                        
        except Exception as e:
            print(str(e))            
    def setIinmax(self, Iinmax):
        if self.withinLim(Iinmax, self.IINLIM[1], self.IINLIM[0]):
#             self.keithleyIn.setIlim(Iinmax*1e-3)
            self.keithleyIn.setI(Iinmax*1e-3)
            self.updateIinmaxLbl()       
    def setFreq(self, Freq):
        if self.withinLim(Freq, self.FREQLIM[1], self.FREQLIM[0]):
            self.freq.setFreq(Freq)
            self.updateFreqLbl()
            self.leFreq.setText(str(f0(Freq)))
    def setFreqAmplitude(self, FreqAmplitude):
        if self.withinLim(FreqAmplitude, self.FREQAMPLITUDELIM[1], self.FREQAMPLITUDELIM[0]):
            self.freq.setAmplitude(FreqAmplitude)
            self.updateFreqAmplitudeLbl()         
    def setFreqOffset(self, FreqOffset):
        if self.withinLim(FreqOffset, self.FREQOFFSETLIM[1], self.FREQOFFSETLIM[0]):
            self.freqOffset.setV(FreqOffset*1e-3)
            self.updateFreqOffsetLbl()                                  
    def setVin(self, Vin):
        if self.withinLim(Vin, self.VINLIM[1], self.VINLIM[0]):        
            self.keithleyIn.setV(Vin*1e-3)
            self.updateVinLbl()
            self.leVin.setText(str(f2(Vin)))
    def setVref(self, Vref):
        if self.withinLim(Vref, self.VREFLIM[1], self.VREFLIM[0]):       
            self.vref.setV(Vref*1e-3)
            self.updateVrefLbl()
            self.leVref.setText(str(f2(Vref))) 
#             self.measVref()
    def setVinhalfref(self, Vinhalfref):
        if self.withinLim(Vinhalfref, self.VINHALFREFLIM[1], self.VINHALFREFLIM[0]):       
            self.vinhalfref.setV(Vinhalfref*1e-3)
            self.updateVinhalfrefLbl()
            self.leVinhalfref.setText(str(f2(Vinhalfref)))            
    def setVlogic(self, Vlogic):
        if self.withinLim(Vlogic, self.VLOGICLIM[1], self.VLOGICLIM[0]):       
            self.vlogic.setV(Vlogic*1e-3)
            self.updateVlogicLbl()                     
    def setAll(self, Iinmax, Freq, Vin):
        self.setIinmax(Iinmax)
        self.setFreq(Freq)
        self.setVin(Vin)              
        self.setEnableLoadReg()
    def toggleMonChan(self):
        monChan = self.agilent.getMonChan() 
        if monChan == '101':
            self.agilent.setMonChan(102)
        elif monChan == '102':
            self.agilent.setMonChan(103)
        else: self.agilent.setMonChan(101)     
    def regWithinLim(self, leUnit, minVal, maxVal):
        val = int(leUnit.text())
        if val < minVal:
            self.status('{0} < {1} is not allowed'.format(val, minVal)); return False;
        elif val > maxVal:
            self.status('{0} > {1} is not allowed'.format(val, maxVal)); return False      
        else: return True                           
    def setEnableLoadReg(self, meas=False):
        if self.vlogicIsOn():
            if self.hammerheadIsInitialized:
#                 if self.regWithinLim(int(self.leEnable.text()), 0, 1) and self.regWithinLim(int(self.leLoad.text()), 0, 31):
                if self.regWithinLim(self.leEnable, 0, 1) and self.regWithinLim(self.leLoad, 0, 31):
                    Enable = '{0:1b}'.format(int(self.leEnable.text()))
                    Load = '{0:05b}'.format(int(self.leLoad.text()))
                    self.addr0 = '000{0}00{1}'.format(Load, Enable)
#                     self.addr0 = '11111111111'
                    self.h.writerd(0, int(self.addr0,2))
                    self.status('{0} is written to the bidi addr 0'.format(self.addr0))
#                     if self.sender().text() == "Set ESL Reg" or self.sender().objectName() == "Set Enable" or self.sender().objectName() == "Set State" or self.sender().objectName() == "Set Load":
#                     if any(self.sender().text() in s for s in ["Set ESL Reg", "Set Enable", "Set Load"]):
                    if meas:
                        if self.modeRloadVout == 'Rsense':
                            self.measRload()
                        elif self.modeRloadVout == 'Vsense':
                            self.measVoutk()
                            self.measIin()
                            self.measVink()
                    self.updateEnableLbl()
                    self.updateLoadLbl()           
            else: self.status('Bidi is not initialized ...')   
        else: self.status('Vlogic is not on -> no registers are written ...')            
    def setConfig(self):
        if self.vlogicIsOn():
            if self.hammerheadIsInitialized:
#                 if self.regWithinLim(int(self.leLoadProg.text()), 0, 1) and self.regWithinLim(int(self.leGearProg.text()), 0, 1) and self.regWithinLim(int(self.leGearFixed.text()), 0, 1) and self.regWithinLim(int(self.leSelectn.text()), 0, 2)  and self.regWithinLim(int(self.leOffset.text()), 0, 5) and self.regWithinLim(int(self.leOffsetEnable.text()), 0, 1) :
                if self.regWithinLim(self.leLoadProg, 0, 1) and self.regWithinLim(self.leGearProg, 0, 1) and self.regWithinLim(self.leGearFixed, 0, 1) and self.regWithinLim(self.leSelectn, 0, 3)  and self.regWithinLim(self.leOffset, 0, 5) and self.regWithinLim(self.leOffsetEnable, 0, 1):
                    loadProg = '{0:1b}'.format(int(self.leLoadProg.text()))
                    gearProg = '{0:1b}'.format(int(self.leGearProg.text()))
                    gearFixed = '{0:1b}'.format(int(self.leGearFixed.text()))
                    selectn = '{0:02b}'.format(int(self.leSelectn.text()))
                    Offset = '{0:05b}'.format(2**int(self.leOffset.text())-1)    
                    OffsetEnable = '{0:1b}'.format(int(self.leOffsetEnable.text()))                                                 
                    self.addr1 = '00{0}{1}{2}{3}{4}{5}{6}'.format(OffsetEnable, Offset, selectn[0], selectn[1], gearFixed, gearProg, loadProg)
#                    self.h.write('{0:011b}'.format(1), int(self.addr1,2))
#                     self.addr1 = '11111111111'
                    self.h.writerd(1, int(self.addr1,2))
#                    print self.addr1
                    self.status('{0} is written to the bidi addr 1'.format(self.addr1))
                    
#                     if self.sender().text() == "Set Config Reg" or self.sender().objectName() == "Load Prog" or self.sender().objectName() == "Offset Enable" or self.sender().objectName() == "Offset":
#                     if any(self.sender().text() in s for s in ["Set Config Reg", "LoadProg", "GearProg", "GearFixed", "Selectn", "Offset Eneable", "Offset"]):
#                         if self.modeRloadVout == 'Rsense':
#                             self.measRload()
#                         elif self.modeRloadVout == 'Vsense':
#                             self.measVoutk()
#                             self.measIin()
#                             self.measVink()
                    self.updateConfigLbl()
            else: self.status('Bidi is not initialized ...')                        
        else: self.status('Vlogic is not on -> no registers are written ...')               
    def setLoad(self, Load, meas=False):
        self.leLoad.setText(str(Load))
        self.setEnableLoadReg()
    def setEnable(self, Enable):
        self.leEnable.setText(str(Enable))
        self.setEnableLoadReg()
    def setGear(self, Gear):
        self.leGearProg.setText(str(1))
        self.leGearFixed.setText(str(Gear))
        self.setConfig()             
          
#------------------------------------------------------------------------------                                    
    def measClicked(self):
        self.buttonClicked()
        try:
            if self.sender().text() == "Meas Vink":
                self.measVink()
            if self.sender().text() == "toggle Rload/Vout":
                self.measToggleRloadVout()
            if self.sender().text() == "Meas Rload":
                self.measRload()                         
            if self.sender().text() == "Meas Voutk":
                self.measVoutk()
            if self.sender().text() == "Meas Iin":                    
                self.measIin()
#            if self.sender().text() == "Adjust Vink to" or self.sender().objectName() == "Adjust Vink to" or self.sender().objectName() == "Set Offset Enable" or self.sender().objectName() == "Set Offset":
            if self.sender().text() == "Adjust Vink to" or self.sender().objectName() == "Adjust Vink to":
                self.measAdjustVink()
            if self.sender().text() == "Adjust Voutk to" or self.sender().objectName() == "Adjust Voutk to":
                self.measAdjustVinkVoutk()
            if self.sender().objectName() == "Retention":                    
                self.measRetention()                
            if self.sender().text() == "Meas All":
                self.measAll()
            if self.sender().text() == "Sweep Load":
                self.measSweepLoad()
            if self.sender().text() == "Sweep Load && Vref":
                self.measSweepLoadVrefVout(skipOverwrite = False)         
            if self.sender().text() == "Meas Everything!":
                self.measEverything()                
            if self.sender().text() == "Clear table only":  
                self.clearTable(self.measTbl)                
            if self.sender().text() == "Save table":  
                self.saveTable(self.measTbl, str(self.leSaveMeasTable.text()), str(self.leSaveMeasTable.text()))     
            if self.sender().text() == "Open in Excel":  
                self.openFile(self.leSaveMeasTable.text())    
            if self.sender().text() == "RloadoverTemp" or self.sender().objectName() == "RloadoverTemp":
                self.measRloadoverTemp()
#            if self.sender().text() == "Open sweep Excel":  
#                self.openFile(self.leSweepLoadVref.text())          
        except Exception as e:
            print(str(e))           
    def measVink(self):
        QtGui.QApplication.processEvents()
        Vink = self.agilent.measVink()
        self.lblVink.setText(f2(Vink*1e3) + ' mV')
        return Vink    
    def measVref(self):
        QtGui.QApplication.processEvents()
        Vref = self.agilent.measVref()
        self.lblVref.setText(f2(Vref*1e3) + ' mV')
        if self.modeRloadVout == 'Vsense':
            self.measVoutk()
        return Vref       
    def measToggleRloadVout(self):
        if self.modeRloadVout == 'Rsense':
            self.modeRloadVout = 'Vsense'
            self.btnRloadVout.setText('Meas Voutk')
        elif self.modeRloadVout == 'Vsense':
            self.modeRloadVout = 'Rsense'    
            self.keithleyIn.outputOff()       
            self.updateVinOn()
            self.btnRloadVout.setText('Meas Rload') 
            time.sleep(0.25)            
        self.keithleyOut.defaultSetup(self.modeRloadVout)            
    def measVoutk(self):
        if self.vinIsOn():
            QtGui.QApplication.processEvents()
            Voutk = self.keithleyOut.measV()
#             Voutk = self.agilent.measVoutk()
#             Voutk = self.keithleyVoutk.measV()
            self.lblRloadVout.setText(f2(Voutk*1e3) + ' mV')
            if Voutk*1e3 < self.VOUTMINLIM:
                self.allOff()
                print('Vout={0} mV is measured too low, all eqipment is turned off'.format(Voutk*1e3))
            else: return Voutk
        else: self.status('KeithleyIn is not on -> no measurement performed ...')
    def measIin(self):
        if self.vinIsOn():
            QtGui.QApplication.processEvents()
            Iin = self.keithleyIn.measI()
            self.lblIin.setText(f2(Iin*1e3) + ' mA')
            return Iin 
        else: self.status('KeithleyIn is not on -> no measurement performed ...')
    def measRload(self):
        QtGui.QApplication.processEvents()
        self.keithleyOut.outputOn()
        time.sleep(0.1)
        Rload1 = float(self.keithleyOut.measR())
        Rload2 = float(self.keithleyOut.measR())
        Rload3 = float(self.keithleyOut.measR())
        Rload = (Rload1 + Rload2 + Rload3)/3
        self.lblRloadVout.setText(f3(Rload) + ' Ohm')
        self.keithleyOut.outputOff()
        return Rload
    def measAllRload(self):
        QtGui.QApplication.processEvents()
        self.Rload = list() # reset the list
        if self.vinIsOn():
            self.vinOnOff()
        self.modeRloadVout = 'Vsense' # will be toggled to Rsense
        self.measToggleRloadVout()
        self.keithleyOut.outputOn()
        self.setEnable(1)
#        for i in range(self.DEFAULTRLOADRANGE[0], self.DEFAULTRLOADRANGE[1]+1): # i = 0..31
        for i in range(0, 31+1): # i = 0..31
            self.setLoad(i)
#             self.Rload.append(float(self.keithleyOut.measR()))
            self.Rload.append(self.measRload())
        self.setLoad(0)
        self.resetRegs()
        self.setGear(1 if int(self.leTargetVoutk.text()) >= int(self.leVgear.text()) else 0)
        self.keithleyOut.outputOff()
#     def adjustVin(self, Vintarget, sleepTime=0.5):
#         Vink = float(self.measVink())
#         self.setVin(float(self.leVin.text()) + (Vintarget - Vink*1e3))
#         time.sleep(sleepTime)
#         return Vink
#     def adjustVout(self, Vouttarget):
#         Voutk = float(self.measVoutk())
#         self.setVref( float(self.leVref.text()) + (Vouttarget - Voutk*1e3))
    def adjustVin(self, sleepTime=0.5):
        Vink_current = float(self.measVink())
        Vink_new = float(self.leVin.text()) + (float(self.leTargetVink.text()) - Vink_current*1e3)
        self.setVin(Vink_new)
        time.sleep(sleepTime)
        print ("Vink_current = ", Vink_current, "Vink_new = ", Vink_new)
#         return Vink
    def adjustVout(self):
        Voutk = float(self.measVoutk())
        Vref = float(self.leVref.text()) + (float(self.leTargetVoutk.text()) - Voutk*1e3)
        self.setVref(Vref)
        print ("Voutk = ", Voutk, "Vref = ", Vref)        
    def measAdjustVink(self):
        if self.vinIsOn():
#             Vin = float(self.leTargetVink.text())
            self.adjustVin()
            self.adjustVin()
            self.adjustVin()
            self.measVoutk()
            self.measIin()
        else: self.status('KeithleyIn is not on -> no measurement performed ...') 
    def measAdjustVinkVoutk(self, sleepTime=0.5):
        if self.vinIsOn():
            self.checkMeasAllAdjustVin.setChecked(True)
#             Vin = float(self.leTargetVink.text())
#             Vout = float(self.leTargetVoutk.text())
            for i in range(0, 2):
                self.adjustVin(sleepTime = i/2)
                self.adjustVout()
                self.adjustVout()
                self.adjustVin(sleepTime = i/2)
#                 time.sleep(i/2)
            self.measVink()
            self.measVoutk()
        else: self.status('KeithleyIn is not on -> no measurement performed ...')       
    def measRetention(self):
        self.retention = int(self.leRetention.text())
        self.updateRetentionLbl()   
        QtGui.QApplication.processEvents()  
        return self.retention        
                        
    def measAll(self):
        if self.isAllOn():
            
            ## Meas Rload all
            if not self.Rload: # if self.Rload is empty
                OldLoad = self.leLoad.text()
                self.measAllRload()
                self.vinOnOff()
                for i in range(0, int(OldLoad)+1):
                    self.setLoad(i)
                    self.adjustVin(sleepTime = 0)
                time.sleep(0.25)    
            Rload = self.Rload[int(self.leLoad.text())]    
                            
            if self.checkMeasAllAdjustVout.isChecked():
                self.measAdjustVinkVoutk()
            elif self.checkMeasAllAdjustVin.isChecked():
                self.measAdjustVink()
            for i in range(0, self.measRetention()+1):
                time.sleep(1)
                self.leRetention.setText(str(i))
                QtGui.QApplication.processEvents()
            Voutk = self.measVoutk()    
            Vink = self.measVink()
            Vref = self.vref.getV()
            Iin = self.measIin()
            Vins = self.keithleyIn.getV()            
            
#             ## Meas Rload seperately
#             OldLoad = int(self.leLoad.text())
#             self.measToggleRloadVout() # turns off Vin
#             Rload = self.measRload()
#             self.setVin(self.DEFAULTVIN)      
#             self.setLoad(0)      
#             self.measToggleRloadVout()                
#             self.keithleyIn.outputOn()
#             self.measVoutk()
#             self.updateVinOn()
#             for i in range(0, OldLoad+1):
#                 self.setLoad(i)
#                 if i % 3 == 0 or i == OldLoad+1: # speeding it up a bit with the slow input supply
#                     self.adjustVin(sleepTime=0)
#                 QtGui.QApplication.processEvents()

           
            
            [eta, rho, Pin, Pout, Iout] = self.calc(Vink, Voutk, Iin, Rload)
            rowData = [f1(float(self.leFreq.text())), f2(Iin*1e3), f2(Iout*1e3), f1(Vink*1e3), f1(Vins*1e3), f1(Voutk*1e3), 
                           f1(Vref*1e3), f4(Rload), f2(Pin*1e3), f2(Pout*1e3), f2(eta*100), f2(rho)]                
            self.updateTableRow(self.measTbl, self.rowNumber, rowData)
            self.rowNumber = self.rowNumber+1
            return Vink, Voutk, Vref, Iin, Iout, Rload, eta, rho, Pin, Pout
    def calc(self, Vin, Vout, Iin, Rload):
        Pin = Vin*Iin
        Pout = Vout*Vout/Rload
        Iout = Vout/Rload
        eta = Pout/Pin
        rho = Pout/self.AREA
        return eta, rho, Pin, Pout, Iout
#    def measSweepSingle(self):
#        QtGui.QApplication.processEvents()
#        [Vink, Voutk, Iin, Iout, Rload, eta, rho, Pin, Pout] = self.measAll()
#        rowData = [f1(float(self.leFreq.text())), f2(Iin*1e3), f2(Iout*1e3), f1(Vink*1e3), f1(float(self.keithleyIn.getV())*1e3), f1(Voutk*1e3), 
#                   f1(float(self.vref.getV())*1e3), f2(Rload), f2(Pin*1e3), f2(Pout*1e3), f2(eta*100), f2(rho)]
#        return rowData
    def measSweepLoad(self):
#         QtGui.QApplication.processEvents()
        if self.isAllOn():
            self.clearTable(self.measTbl)
            self.Rload = ()
#             if doMeasLoad:
#                 self.resetRegs()
    #             self.measAllRload()
    #             self.vinOnOff()
#             self.setGear(1 if float(self.leVref.text()) >= float(self.leVgear.text()) else 0)
            for i in range(int(self.leRloadMin.text()), int(self.leRloadMax.text())+1, int(self.leRloadStep.text())):
                self.setLoad(i)
                QtGui.QApplication.processEvents()
#                 [Vink, Voutk, Vref, Iin, Iout, Rload, eta, rho, Pin, Pout] = self.measAll()
                self.measAll()
#                 rowData = [f1(float(self.leFreq.text())), f2(Iin*1e3), f2(Iout*1e3), f1(Vink*1e3), f1(float(self.keithleyIn.getV())*1e3), f1(Voutk*1e3), 
#                            f1(Vref*1e3), f3(Rload), f2(Pin*1e3), f2(Pout*1e3), f2(eta*100), f2(rho)]                
#                 self.updateTableRow(self.measTbl, self., rowData)
            self.setLoad(int( (int(self.leRloadMax.text())+1)/2 ), meas=True)
            self.setVin(2200)
            self.setLoad(0, meas=True)
#             self.measAll()
#             self.adjustVin()
    def measSweepLoadVrefVout(self, skipOverwrite):
        QtGui.QApplication.processEvents()
        xlsfiles = list()
        if self.isAllOn():
            if not skipOverwrite:
                if not self.confirmOverwrite(str(self.leSweepLoadVref.text())):
                    return
#             self.resetRegs()
#            self.measAllRload()
#            self.vinOnOff()
            adjustVoutkOld = self.leTargetVoutk.text()
#             gearOld = self.leGearFixed.text()
            for j in range(int(self.leVrefMin.text()), int(self.leVrefMax.text())+1, int(self.leVrefStep.text())):
#                print j, range(int(self.leVrefMin.text()), int(self.leVrefMax.text())+1, int(self.leVrefStep.text()))
                self.setVref(j)
                if self.checkMeasAllAdjustVout.isChecked():
                    self.leTargetVoutk.setText(str(j))
#                    print j, int(self.leVgear.text())
                self.setGear(1 if j >= int(self.leVgear.text()) else 0)
                self.measSweepLoad()
                self.saveTable(self.measTbl, 'V{0}.xls'.format(j), 'V={0}'.format(j))
                xlsfiles.append('V{0}.xls'.format(j))
            self.leTargetVoutk.setText(adjustVoutkOld)
#             self.setGear(gearOld)
            self.resetRegs()
            self.combine_xls('{0}.xls'.format(self.leSweepLoadVref.text()), xlsfiles)
            self.removeFile(xlsfiles)
            self.status('{0} was saved and all intermediate files {1} were deleted'.format(self.leSweepLoadVref.text(), xlsfiles))
            self.allOff()
    def measEverything(self):
#        print str(self.leSweepLoadVref.text())
        if self.isAllOn():
            chipName = self.leSweepLoadVref.text()
            vinOld = self.leTargetVink.text()
            freqOld = self.leFreq.text()
            VintargetList = str.split(str(self.leMeasEverythingVin.text()), ',')
            FreqtargetList = str.split(str(self.leMeasEverythingFreq.text()), ',')
#            print FreqtargetList, VintargetList
            if self.confirmOverwrite('{0}_Vin{1}_Freq{2}_fixedVout.xls'.format(self.leSweepLoadVref.text(), VintargetList[0], FreqtargetList[0])):            
                for k in range(0, len(FreqtargetList)):
    #                print k
                    self.setFreq(float(FreqtargetList[k]))
                    for i in range(0, len(VintargetList)):
                        print FreqtargetList[k], VintargetList[i]
                        self.leTargetVink.setText(VintargetList[i])
                        self.leSweepLoadVref.setText('{0}_Vin{1}_Freq{2}_fixedVout'.format(chipName, VintargetList[i], FreqtargetList[k]))
                        self.checkMeasAllAdjustVout.setChecked(True)
                        self.measSweepLoadVrefVout(skipOverwrite = True)
                        self.leSweepLoadVref.setText('{0}_Vin{1}_Freq{2}_fixedVref'.format(chipName, VintargetList[i], FreqtargetList[k]))
                        self.checkMeasAllAdjustVout.setChecked(False)
                        self.measSweepLoadVrefVout(skipOverwrite = True)
                self.setFreq(freqOld)
                self.leSweepLoadVref.setText(chipName)
                self.leTargetVink.setText(vinOld)
                self.allOff()
                self.status('Meas Everything has successfully completed!')
    def measRloadoverTemp(self):
#         self.clearTable(self.measTbl)
#         self.updateTableColumn(self.measTbl, 1, [self.leTemp.text()])
        if self.vlogicIsOn():
            self.measAllRload()
            self.Rload.insert(0,self.leTemp.text())
            self.updateTableColumn(self.measTbl, self.columnNumber, self.Rload)
            self.columnNumber = self.columnNumber + 1
        else: print 'Vlogic is not turned on'
        
        

#    def clearSweep(self):
#        self.clearTable(self.measTbl)
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
    def updateTableColumn(self, table, column, columnData):
        for i in range(0, len(columnData)):
            item = QTableWidgetItem(str(columnData[i]))
            item.setFlags(QtCore.Qt.ItemIsEnabled) # makes cells read-only
            table.setItem(i, column, item)                                       
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
        self.rowNumber=0
        self.columnNumber=0
    def saveTable(self, table, filename, sheetname):
        if self.tableIsEmpty(table) == True:
            self.status('Table is empty -> not processed')
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
                self.status('{0} was saved'.format(filename))  
    def combine_xls(self, filename, xlsfiles):
        wbk = xlwt.Workbook()
        for m in range(len(xlsfiles)):
            file_read = xlrd.open_workbook(xlsfiles[m])
            sh_read = file_read.sheet_by_index(0)
            sh_write = wbk.add_sheet(str.split(xlsfiles[m],'.')[0])
            for j in range(len(sh_read.col_values(0))):
                for i in range(len(sh_read.row_values(0))):
                    sh_write.write(j,i,sh_read.cell(j,i).value)
        wbk.save(filename)              
                                 
#------------------------------------------------------------------------------    
    def updateIinmaxLbl(self):
        self.lblIinmax.setText(f0(float(self.keithleyIn.getI())*1e3) + ' mA')
    def updateFreqLbl(self):
        self.lblFreq.setText(f2(self.freq.getFreq()/1e6) + ' MHz')
    def updateFreqAmplitudeLbl(self):
        self.lblFreqAmplitude.setText(f1(self.freq.getAmplitude()*1e3) + ' mV')
    def updateFreqOffsetLbl(self):
        self.lblFreqOffset.setText(f2(self.freqOffset.getV()*1e3) + ' mV')                
    def updateVinLbl(self):
        self.lblVin.setText(f2(float(self.keithleyIn.getV())*1e3) + ' mV') 
    def updateVrefLbl(self):
        self.lblVref.setText(f0(float(self.vref.getV())*1e3) + ' mV')
    def updateVinhalfrefLbl(self):
        self.lblVinhalfref.setText(f0(float(self.vinhalfref.getV())*1e3) + ' mV')
    def updateVlogicLbl(self):
        self.lblVlogic.setText(f2(float(self.vlogic.getV())*1e3) + ' mV')                 
    def updateEnableLbl(self):     
        self.lblEnable.setText('Enable: {0}'.format(self.leEnable.text()))             
    def updateLoadLbl(self):     
        self.lblLoad.setText('Load: {0}'.format(self.leLoad.text()))        
    def updateRetentionLbl(self):     
        self.lblRetention.setText('Retention: {0}'.format(self.leRetention.text()))            
    def updateConfigLbl(self):
        self.lblLoadProg.setText('LoadProg: {0}'.format(self.leLoadProg.text()))      
        self.lblGearProg.setText('GearProg: {0}'.format(self.leGearProg.text()))         
        self.lblGearFixed.setText('GearFixed: {0}'.format(self.leGearFixed.text()))      
        self.lblSelectn.setText('Selectn: {0}'.format(self.leSelectn.text()))
        self.lblOffsetEnable.setText('Offset Enable: {0}'.format(self.leOffsetEnable.text()))  
        self.lblOffset.setText('Offset: {0}'.format(self.leOffset.text()))                      
    def updateFreqOn(self):
        self.lblFreqOn.setText('ON' if self.freqIsOn() else 'OFF')
    def updateVinOn(self):
        self.lblVinOn.setText('ON' if self.vinIsOn() else 'OFF')
    def updateVrefOn(self):
        self.lblVrefOn.setText('ON' if self.vrefIsOn() else 'OFF')    
    def updateVinhalfrefOn(self):
        self.lblVinhalfrefOn.setText('ON' if self.vinhalfrefIsOn() else 'OFF')         
    def updateVlogicOn(self):
        self.lblVlogicOn.setText('ON' if self.vlogicIsOn() else 'OFF')            
    def updateAllLbl(self):
        self.updateIinmaxLbl()
        self.updateFreqLbl()
        self.updateVinLbl()
        self.updateVrefLbl()
        self.updateVinhalfrefLbl()
        self.updateVlogicLbl()
        self.updateFreqOn()
        self.updateVinOn()
        self.updateVrefOn()
        self.updateVinhalfrefOn()
        self.updateVlogicOn()
        QtGui.QApplication.processEvents()

#------------------------------------------------------------------------------        
    def buttonClicked(self):
        sender = self.sender()
        self.statusBar().showMessage(sender.text() + ' was pressed')         
    def status(self, text):
        self.statusBar().showMessage(text)               

#------------------------------------------------------------------------------        
    def closeEvent(self, event):
        print("Turning off and disconnecting devices ... \nClosing Window ... ")
        try:
            self.keithleyIn.close()
            self.keithleyOut.close()
            self.freq.close()
            self.freqOffset.close()
            self.vlogic.close()
            self.agilent.close()
            self.vref.close()  
        except Exception as e:
            print(str(e))   
    
    def withinLim(self, val, Max, Min):
        if  val > Max:
            self.status('{0} > max = {1} -> not processed'.format(val, Max))
            WithinLim = False 
        elif val < Min:
            self.status('{0} < min = {1} -> not processed'.format(val, Min))
            WithinLim = False 
        else:
            WithinLim = True
        return WithinLim  

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
                self.status('Old {0} was deleted'.format(filename))  
                return True
            else:
                self.status('{0} was not overwritten'.format(filename))  
                return False 
        else: return True

    def removeFile(self, files):
        if type(files) is list:
            for i in range(0,len(files)):
                os.remove(files[i])
        else: os.remove(files)
                    
    def openFile(self, filename):
        if os.path.isfile(filename):
            os.startfile(os.getcwd() +'\\' + filename)
        else: self.status('{0} does not exist'.format(filename))  
            
def f4(x):
    return '{:.4f}'.format(x)     
def f3(x):
    return '{:.3f}'.format(x)
def f2(x):
    return '{:.2f}'.format(x)
def f1(x):
    return '{:.1f}'.format(x)
def f0(x):
    return '{:.0f}'.format(x)

def main():
    app = QtGui.QApplication(sys.argv)
    SCCtrl = SCmeas()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
    
    
