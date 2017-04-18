#!/usr/bin/env python
# -*- coding: utf-8 -*- 
'''
Created on Apr 18, 2017

@author: rid
'''

from threading import Thread
from PyQt4 import QtGui
from GF1408_CONST import *

class HammerheadGui_Class(object):
    '''
    classdocs
    '''


    def __init__(self, parent):
        '''
        Constructor
        '''
        Button_Connect = QtGui.QPushButton(GF1408_CONST.HAMMERHEAD_CONNECT, parent)
        Button_Connect.setAccessibleName(GF1408_CONST.HAMMERHEAD_CONNECT)
        Button_Connect.clicked.connect(self.onClickButton)
        Button_Connect.setFixedSize(75, 28)

        Button_Init = QtGui.QPushButton(GF1408_CONST.HAMMERHEAD_INIT, parent)
        Button_Init.clicked.connect(self.onClickButton)
        Button_Init.setFixedSize(75, 28)
        Button_Init.setEnabled(False);
        
        
        # Make Instance accessible
        self.Button_Connect = Button_Connect;
        self.Button_Init = Button_Init;
        
        box = QtGui.QVBoxLayout();
        box.addWidget(Button_Connect);
        box.addWidget(Button_Init);
        # box.addStretch(1);
        
        gb_Hammerhead = QtGui.QGroupBox('Hammerhead')
        gb_Hammerhead.setLayout(box)
        gb_Hammerhead.setMaximumWidth(100)
        gb_Hammerhead.setFixedHeight(100)
        
        self.GroupBox = gb_Hammerhead
        self.parent = parent
    
    def onClickButton(self):
        
        parent = self.parent
        parent.buttonClicked()  # print out pressed button
        
        '''
        try: 
            self.allOff()
        except Exception as e:
            self.status('Fail 1')
        '''
        
        if parent.sender().accessibleName() == GF1408_CONST.HAMMERHEAD_CONNECT:
            self.connectHammerhead() 
        
        try:
            if parent.sender().text() == GF1408_CONST.HAMMERHEAD_INIT:
                self.initHammerhead()                   
            if parent.sender().text() == GF1408_CONST.EXIT:
                self.close() 

        except Exception as e:
            print(str(e))  
        
    def connectHammerhead(self):
        
        self.Button_Connect.setEnabled(False);
        parent = self.parent
        
        def finishedConnect():
        
            self.Button_Connect.setEnabled(True);
            self.Button_Init.setEnabled(parent.h.isConnected)
            
            if(parent.h.isConnected):
                parent.status('Connected')
                newtext = GF1408_CONST.HAMMERHEAD_DISCONNECT
            else:
                parent.status('Disconnected')
                newtext = GF1408_CONST.HAMMERHEAD_CONNECT
                
            self.Button_Connect.setText(newtext)  
        
        parent.PYQT_SIGNAL.connect(finishedConnect)
        Thread(target=self.async_connectHH).start() 
    
    def async_connectHH(self):

        parent = self.parent            
        try:
            if parent.h.isConnected:
                parent.h.disconnect()
            else:
                parent.h.connect()
        except Exception as e:
            print(str(e))
        parent.PYQT_SIGNAL.emit()

    
