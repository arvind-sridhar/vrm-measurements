import visa
from time import sleep

class KeithleyRes():
    def __init__(self):    
        self.DEFAULTILIM    = 100e-3
        self.DEFAULTIRANGE  = 100e-3
#        self.initme()
        
    def initme(self, devices, unique):
#            self.DEFAULTV = Vdefault
#            self.DEFAULTVMAX = Vmax
            self.keithley = devices.findUnique(unique);
            self.keithley.write("*RST")
#            self.keithley.write("*CLS")
            
            self.defaultSetup()
            return self.keithley.ask("*IDN?")   
        
    def defaultSetup(self):
        self.outputOff()
        self.keithley.write("SENS:FUNC 'RES'") # Select resistance measurement function
        self.keithley.write("SENS:RES:MODE MAN") # Select manual ohms mode
#        self.keithley.write("SENS:RES:RANGE 200") # Select measurement range (might not be needed in manual ohms mode)
        self.keithley.write("SOUR:FUNC CURR") # Select current as the source
        self.keithley.write("SOUR:CURR:RANG 0.01") # Select 10 mA current range
        self.keithley.write("SOUR:CURR 0.005") # Select 5 mA source current
        self.keithley.write("SYST:RSEN ON") # turn on remote sense (4-wire)
        self.keithley.write("SENS:RES:OCOM ON") # Turn on offset compensation (compensates internal temperature dependent offsets). Changes ~5mOhm
        self.keithley.write("SENS:VOLT:PROT 1") # Select voltage compliance to 1 V
        self.keithley.write("FORM:ELEM RES") # only returns resistance readings
        
    def setV(self, V):
        Vold = self.getV()
        if float(V)<=self.DEFAULTVMAX:          
            self.keithley.write("SOUR:VOLT:LEV %s" % V) # Set voltage level
        else:
            self.keithley.write("SOUR:VOLT:LEV %s" % Vold) # Set voltage level
            print ('V > Vmax. \nV remains %.3f V' % float(Vold))    
        
    def setIlim(self, Ilim):
        self.keithley.write("SENS:CURR:PROT %s" % Ilim) # Set to current compliance
        
    def setIrange(self,Irange):
        self.keithley.write("SENS:CURR:RANG %s" % Irange)
        
    def getIlim(self):
        return self.keithley.ask("SENS:CURR:PROT:LEV?") # manual p 391
    
    def getV(self):
        return self.keithley.ask("SOUR:VOLT:LEV:IMM:AMPL?") # manual p 395
    
    def setOutput(self, state):
        if state == 'ON':
            self.outputOn()
        else:
            self.outputOff()
    
    def outputOn(self):
        self.keithley.write("OUTP ON")

    def outputOff(self):
        self.keithley.write("OUTP OFF")
        
    def getOutput(self):
        return self.keithley.ask("OUTP:STAT?")        
    
    def measI(self):
        self.keithley.write("INIT") # Initialize
        self.keithley.write("*TRG") # Trigger once
        I = str.split(self.keithley.ask("FETC?"),',') # split the string.
        return float(I[1]) # Get the measured output current
    
    def measR(self):
        self.outputOn()
        self.keithley.write("INIT") # Initialize
#        self.keithley.write("*TRG") # Trigger once
        R = self.keithley.ask("FETC?")
        self.outputOff()
        return R
    
    def close(self):
        try:
            self.outputOff()
            self.keithley.close()
        except Exception as e:
            print(str(e))                      
        
        
    
        