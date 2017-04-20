#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Simple GUI to control Single SAR ADC
Lukas Kull, 2012
"""

import sys
import hammerhead
from PyQt4 import QtGui


class SAR1Control(QtGui.QMainWindow):
    
    def __init__(self):
        super(SAR1Control, self).__init__()
        
        self.initUI()
        
    def initUI(self):      

        self.btnC = QtGui.QPushButton("Connect", self)
        self.btnC.move(30, 50)
        self.btnC.clicked.connect(self.connectHammerhead)            

        self.btnI = QtGui.QPushButton("Init", self)
        self.btnI.move(150, 50)
        self.btnI.clicked.connect(self.initHammerhead)

        self.lblC = QtGui.QLabel('not connected', self)
        self.lblC.move(270, 50)

        self.leR2 = QtGui.QLineEdit("0", self)
        self.leR2.move(30, 90)
        self.btnR2 = QtGui.QPushButton("Set Reg 0", self)
        self.btnR2.move(150, 90)
        self.btnR2.setObjectName("R0")
        self.btnR2.clicked.connect(self.writeReg)            
        self.lblR2 = QtGui.QLabel('-', self)
        self.lblR2.move(270, 90)
        
        self.leR3 = QtGui.QLineEdit("0", self)
        self.leR3.move(30, 130)
        self.btnR3 = QtGui.QPushButton("Set Reg 1", self)
        self.btnR3.move(150, 130)
        self.btnR3.setObjectName("R1")
        self.btnR3.clicked.connect(self.writeReg)            
        self.lblR3 = QtGui.QLabel('-', self)
        self.lblR3.move(270, 130)
        
        # self.leR4 = QtGui.QLineEdit("0", self)
#        self.leR4.move(30,170)
        self.btnR4 = QtGui.QPushButton("Init Converter", self)
        self.btnR4.move(150, 170)
        self.btnR4.setObjectName("InitConverter")
        self.btnR4.clicked.connect(self.writeReg)            
        # self.lblR4 = QtGui.QLabel('-', self)
#        self.lblR4.move(270, 170)
        
        self.leR5 = QtGui.QLineEdit("0", self)
        self.leR5.move(30, 210)
        self.leR5.setObjectName("SetLoadInt")
        self.leR5.returnPressed.connect(self.writeReg)
        self.btnR5 = QtGui.QPushButton("Set Load Int", self)
        self.btnR5.move(150, 210)
        self.btnR5.setObjectName("SetLoadInt")
        self.btnR5.clicked.connect(self.writeReg)            
        self.lblR5 = QtGui.QLabel('-', self)
        self.lblR5.move(270, 210)
        
        self.btnRa0 = QtGui.QPushButton("Set Reg 2-5 to 0", self)
        self.btnRa0.move(30, 250)
        self.btnRa0.setObjectName("Ra0")
        self.btnRa0.clicked.connect(self.writeReg)            
        
        self.btnRdef = QtGui.QPushButton("Set Reg 2-5 to 0,264,4,129", self)
        self.btnRdef.move(30, 290)
        self.btnRdef.resize(150, self.btnRdef.height())
        self.btnRdef.setObjectName("Rdef")
        self.btnRdef.clicked.connect(self.writeReg)            

        self.btnRtest1 = QtGui.QPushButton("Set Reg 2 to 1", self)
        self.btnRtest1.move(30, 330)
        self.btnRtest1.setObjectName("Rtest1")
        self.btnRtest1.clicked.connect(self.writeReg)            

        self.btnRtest2 = QtGui.QPushButton("Set Reg 2 to 3", self)
        self.btnRtest2.move(150, 330)
        self.btnRtest2.setObjectName("Rtest2")
        self.btnRtest2.clicked.connect(self.writeReg)            

        self.statusBar()
        
        self.setGeometry(300, 300, 390, 430)
        self.setWindowTitle('SAR 1 Control Window')
        self.show()

        self.h = hammerhead.Hammerhead()
        
    def closeEvent(self, event):
        print("Closing Window. Close Socket.")
        try:
            self.h.disconnect()
        except Exception as e:
            print(str(e))

    def buttonClicked(self):
      
        sender = self.sender()
        self.statusBar().showMessage(sender.text() + ' was pressed')

    def connectHammerhead(self):
        try:
            self.h.connect()
        except Exception as e:
            self.statusBar().showMessage(str(e))
        else:
            self.lblC.setText("connected")
    def initHammerhead(self):
        try:
            self.h.init()
        except Exception as e:
            self.statusBar().showMessage(str(e))
        else:
            self.statusBar().showMessage('Initialized.')
    def writeReg(self):
        try:
            if self.sender().objectName() == "R0":
                # print self.leR2.text()
                self.h.writera(0, self.leR2.text())
            if self.sender().objectName() == "R1":
                self.h.writera(1, self.leR3.text())
            if self.sender().objectName() == "InitConverter":
                self.initConverter()
                
            if self.sender().objectName() == "SetLoadInt":
                self.setLoadInt()                
            if self.sender().objectName() == "Ra0":
                self.h.writera(2, 0)
                self.h.writera(3, 0)
                self.h.writera(4, 0)
                self.h.writera(5, 0)
            if self.sender().objectName() == "Rdef":
                self.h.writera(2, 0)
                self.h.writera(3, 264)
                self.h.writera(4, 4)
                self.h.writera(5, 129)
            if self.sender().objectName() == "Rtest1":
                self.h.writera(2, 1)
            if self.sender().objectName() == "Rtest2":
                self.h.writera(2, 3)
        except Exception as e:
            self.statusBar().showMessage(str(e))
        else:
            if self.sender().objectName() == "R2":
                self.lblR2.setText(self.leR2.text())
            if self.sender().objectName() == "R3":
                self.lblR3.setText(self.leR3.text())
            if self.sender().objectName() == "R4":
                self.lblR4.setText(self.leR4.text())
            if self.sender().objectName() == "R5":
                self.lblR5.setText(self.leR5.text())
            if self.sender().objectName() == "Ra0":
                self.lblR2.setText("0")
                self.lblR3.setText("0")
                self.lblR4.setText("0")
                self.lblR5.setText("0")
            if self.sender().objectName() == "Rdef":
                self.lblR2.setText("0")
                self.lblR3.setText("264")
                self.lblR4.setText("4")
                self.lblR5.setText("129")
            if self.sender().objectName() == "Rtest1":
                self.lblR2.setText("1")
            if self.sender().objectName() == "Rtest2":
                self.lblR2.setText("3")
            
    def initConverter(self):
        try:
#            self.h.writera(1, 0b001111100000) # gear=0, short_offsetcomp=0, c_offset=11111
#            self.h.writera(0, 0b000000000000) # stop_clk=0, select_init=0, load_int=0
#            self.h.writera(0, 0b100000000000) # stop_clk=1, select_init=0, load_int=0
#            self.h.writera(0, 0b110000000000) # stop_clk=1, select_init=1, load_int=0
#            self.h.writera(0, 0b010000000000) # stop_clk=0, select_init=1, load_int=0
#            self.h.writera(0, 0b110000000000) # stop_clk=1, select_init=1, load_int=0        
#            self.h.writera(0, 0b100000000000) # stop_clk=1, select_init=0, load_int=0
#            self.h.writera(0, 0b000000000000) # stop_clk=0, select_init=0, load_int=0
            self.h.writera(1, 0b000001111100)  # gear=0, short_offsetcomp=0, c_offset=11111
            self.h.writera(0, 0b000000000000)  # stop_clk=0, select_init=0, load_int=0
            self.h.writera(0, 0b000000000001)  # stop_clk=1, select_init=0, load_int=0
            self.h.writera(0, 0b000000000011)  # stop_clk=1, select_init=1, load_int=0
            self.h.writera(0, 0b000000000010)  # stop_clk=0, select_init=1, load_int=0
            self.h.writera(0, 0b000000000011)  # stop_clk=1, select_init=1, load_int=0        
            self.h.writera(0, 0b000000000001)  # stop_clk=1, select_init=0, load_int=0
            self.h.writera(0, 0b000000000000)  # stop_clk=0, select_init=0, load_int=0
        except Exception as e: 
            self.statusBar().showMessage(str(e))
        else:
            self.statusBar().showMessage('Converter is initialized.')
        
    def setLoadInt(self):
        if int(self.leR5.text()) < 0:
            print '%s < 0 is not allowed' % int(self.leR5.text()) 
        elif int(self.leR5.text()) > 31:
            print '%s > 31 is not allowed' % int(self.leR5.text())
        else:                
            print '{0:011b}'.format(int(self.leR5.text()) << 2), ', ', int('{0:011b}'.format(int(self.leR5.text()) << 2), 2)
           
            self.h.writera(0, int('{0:011b}'.format(int(self.leR5.text()) << 2), 2))

def main():
    
    app = QtGui.QApplication(sys.argv)
    sarCtrl = SAR1Control()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
