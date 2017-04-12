'''
Created on Apr 12, 2017

@author: rid
'''

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *


class GF1408_GUI(QtGui.QMainWindow):
    
    def __init__(self):
        super(GF1408_GUI, self).__init__()
        self.initUI()
        
    def initUI(self):
        vMainBox, vMainLayout = self.addVWidget()
        self.setCentralWidget(vMainBox)    
        hMainBox, hMainLayout = self.addHWidget()
                   
        #vMainLayout.addWidget(self.initButtons())
        vMainLayout.addWidget(hMainBox)
        #hMainLayout.addWidget(self.setOnMeasButtons())
        #hMainLayout.addWidget(self.setSweepButtons())
        
        self.statusBar()
        self.setGeometry(25, 25, 50, 50)
        self.setWindowTitle('10W SCVR Control Window')
        self.show()
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
   