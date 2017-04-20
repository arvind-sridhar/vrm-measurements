import visa
import time

class AgilentDC():
#    def __init__(self):

        
#        self.initme()
        
    def initme(self, devices, unique, V, I):
        self.DEFAULTV = V
        self.DEFAULTI = I
        
        self.agilentDC = devices.findUnique(unique)
        self.agilentDC.write("*RST")
        self.agilentDC.write("*CLS")
        
        self.defaultSetup()
        return self.agilentDC.ask("*IDN?")   

    def defaultSetup(self):
        self.outputOff()
        self.setV(self.DEFAULTV)
        self.setI(self.DEFAULTI)    
    
    def setV(self, V):
        self.agilentDC.write("SOUR:VOLT %s" % V)
    def getV(self):
        return float(self.agilentDC.ask("SOUR:VOLT?"))

    def setI(self, I):
        self.agilentDC.write("SOUR:CURR %s" % I)       
    def getI(self):
        return float(self.agilentDC.ask("SOUR:CURR?"))
    def measI(self):
        return float(self.agilentDC.ask("MEAS:CURR?"))            
    
    def setIlim(self, Imax):
        self.agilentDC.write("SOUR:CURR:PROT %s" % Imax) 
    def getIlim(self):
        return float(self.agilentDC.ask("SOUR:CURR:PROT?"))         
    def setVlim(self, Vmax):
        self.agilentDC.write("SOUR:VOLT:PROT %s" % Vmax)     
    def getVlim(self):
        return float(self.agilentDC.ask("SOUR:VOLT:PROT?"))   
        
    def setOutput(self, state):
        if state == 'ON':
            self.outputOn()
        else:
            self.outputOff()
    
    def outputOn(self):
        self.agilentDC.write("OUTP ON")
        
    def outputOff(self):
        self.agilentDC.write("OUTP OFF")      
    def getOutput(self):
        return self.agilentDC.ask("OUTP?")          
    
    def close(self):
        try:
            self.outputOff()
            self.agilentDC.close()
        except Exception as e:
            print(str(e))          
