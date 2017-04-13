'''
Created on Apr 12, 2017

@author: rid
'''

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from GF1408_tools import GF1408_BIDI


class GF1408_CONST():
    HAMMERHEAD_CONNECT  = "Connect hammerhead"
    HAMMERHEAD_INIT     = "Init hammerhead"
    EXIT = "Exit"

class GF1408_GUI(QtGui.QMainWindow):
    
    WINDOW_SIZE=(500,500)
    WINDOW_NAME='CarrICool GF1408 - Control Window'
    
    def __init__(self):
        super(GF1408_GUI, self).__init__()
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
                
        HHBox = self.getHammerHeadBox()
            
        h0Box, h0Layout = self.addHWidget()
        v0Layout.addWidget(h0Box)          
        h0Layout.addWidget(HHBox)
        
        v0Box.setMaximumHeight(100)
        #v0Box.setMaximumWidth(100)
        return v0Box        
    
    def getHammerHeadBox(self):
        
        btnConnectHammerhead = QtGui.QPushButton("Connect", self)
        btnConnectHammerhead.clicked.connect(self.initClicked)
        btnConnectHammerhead.setFixedSize(75,28)
        btnConnectHammerhead.setCheckable(True)
        btnInitHammerhead = QtGui.QPushButton("Init", self)
        btnInitHammerhead.clicked.connect(self.initClicked)
        btnInitHammerhead.setFixedSize(75,28)
        
        box = QVBoxLayout();
        box.addWidget(btnConnectHammerhead);
        box.addWidget(btnInitHammerhead);
        box.addStretch(1);
        
        gb_Hammerhead=QtGui.QGroupBox('Hammerhead')
        gb_Hammerhead.setLayout(box)
        gb_Hammerhead.setMaximumWidth(100)
        
        return gb_Hammerhead
     
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
        
    def initClicked(self):
        self.buttonClicked()
        
        '''
        try: 
            self.allOff()
        except Exception as e:
            self.status('Fail 1')
        '''
        
        try:
            '''
            self.devices = devices.Devices()
            self.devices.printInstrList()
            self.addr0 = '-'
            self.addr1 = '-'
            self.addr2 = '-'
            self.hammerheadIsInitialized = False
            '''
            
            if self.sender().text() == GF1408_CONST.HAMMERHEAD_CONNECT:
                self.connectHammerhead()   
            if self.sender().text() == GF1408_CONST.HAMMERHEAD_INIT:
                self.initHammerhead()                   
            if self.sender().text() == GF1408_CONST.EXIT:
                self.close() 

        except Exception as e:
            print(str(e))  