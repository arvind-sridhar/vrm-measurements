import visa
import time

class AgilentHP():
#    def __init__(self):

        
#        self.initme()
        
    def initme(self, devices, unique, V, I):
        self.DEFAULTV = V
        self.DEFAULTI = I
        
        self.agilentHP = devices.findUnique(unique)
        self.agilentHP.write("*RST")
        self.agilentHP.write("*CLS")
        
        self.defaultSetup()
        return self.agilentHP.ask("*IDN?")   

    def defaultSetup(self):
        self.outputOff()
        self.setV(self.DEFAULTV)
        self.setI(self.DEFAULTI)    
    
    def setV(self, V):
        self.agilentHP.write("SOUR:VOLT %s" % V)
    def getV(self):
        return float(self.agilentHP.ask("SOUR:VOLT?"))

    def setI(self, I):
#         self.agilentHP.write("SOUR:PROT %s" % I)   
        self.agilentHP.write("SOUR:CURR %s" % I)  
    def getI(self):
        return self.agilentHP.ask("MEAS:CURR?")            
        
    def setOutput(self, state):
        if state == 'ON':
            self.outputOn()
        else:
            self.outputOff()
    
    def outputOn(self):
        self.agilentHP.write("OUTP ON")
        
    def outputOff(self):
        self.agilentHP.write("OUTP OFF")      
    def getOutput(self):
        return self.agilentHP.ask("OUTP?")          
    
    def close(self):
        try:
            self.outputOff()
            self.agilentHP.close()
        except Exception as e:
            print(str(e))          