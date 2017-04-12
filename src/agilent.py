import visa
import time

class Agilent():
#    def __init__(self):

        
#        self.initme()
        
    def initme(self, devices, unique):
            self.DEFAULTMONCHAN   = 101
            self.agilent = devices.findUnique(unique)
            self.agilent.write("*RST")
            self.agilent.write("*CLS")
            
            self.defaultSetup()
            return self.agilent.ask("*IDN?")   
        
    def defaultSetup(self):
        self.agilent.write("CONF:VOLT:DC 10,1e-5,(@101,102,103)") # Configuring channels for DC voltage, range 1V, resolution 1e-5V
#        self.agilent.write("ROUT:SCAN (@101,102)") # Scan channel 101 and 102
        self.setMonChan(self.DEFAULTMONCHAN)
        self.agilent.write("ROUT:MON:STAT ON")
   
    def setMonChan(self, monChan):
        self.agilent.write("ROUT:MON:CHAN (@%s)" % monChan)
        
    def getMonChan(self):
        return self.agilent.ask("ROUT:MON:CHAN?")[5:8]
    
    def readMonChan(self):
        V = float(self.agilent.ask("ROUT:MON:DATA?"))
        return V

    def measVink(self): 
        self.setMonChan(101)
        return self.readMonChan()
        
    def measVoutk(self):
        self.setMonChan(102)
        return self.readMonChan()
    
    def measVref(self):
        self.setMonChan(103)
        return self.readMonChan()
    
    def measAll(self):
        V = str.split(self.meas(),',') # split the string.         
        return float(V[0]), float(V[1]) # Voutk, Vink         
    
#    def meas(self):
#        self.agilent.write("INIT") # Initiate the scan
#        V = self.agilent.ask("FETC?") # Fetch the measured values. 
##        print V
#        if len(V)<31: # Have had experiences where the read out array was too short. This clause forces a re-red if that happens.  
#            time.sleep(0.5)
#            V = self.agilent.ask("FETC?") # Fetch the measured values.
#            time.sleep(0.25)
#            print [V, len(V)]
#            print 'voltages were re-read'
#        
#        return V
#    def measVink(self): 
#        V = str.split(self.meas(),',') # split the string.         
#        return float(V[1]) # Vink
#        
#    def measVoutk(self):
#        V = str.split(self.meas(),',') # split the string.         
#        return float(V[0]) # Voutk
      
        
    def close(self):
        try:
            self.agilent.close()
        except Exception as e:
            print(str(e))        
            
            
        