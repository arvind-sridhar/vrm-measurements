import visa
from time import sleep

class Keithley():
    def __init__(self):    
#        self.DEFAULTILIM    = 200e-3
        self.DEFAULTIRANGE = 1000e-3
        
        
#        self.initme()
        
    def initme(self, devices, unique, mode, Vdefault, Vmax):
#        try:
#            visaInstrList = visa.get_instruments_list()
#        except Exception as e:
#            print(str(e))
#        else:
            self.DEFAULTV = Vdefault
            self.DEFAULTVMAX = Vmax
            self.keithley = devices.findUnique(unique);
            self.keithley.write("*RST")
#            self.keithley.write("*CLS")
            
            self.defaultSetup(mode)
            return self.keithley.ask("*IDN?")   
        
    def defaultSetup(self, mode):
        self.keithley.write("*RST")
        self.mode = mode
#        print self.mode
        self.outputOff()
        self.keithley.write("SYSTem:BEEPer:STATe 0")
        if self.mode == 'Isense':  # Keithley Manual p 108
            self.keithley.write("SOUR:FUNC VOLT")  # Set to voltage source
            self.keithley.write("SOUR:VOLT:MODE FIXED")
            self.keithley.write("SENS:FUNC 'CURR'")
            self.setIlim(1)  # MUST set Ilim before Irange. Will be reset to default below. 
            self.keithley.write("SENS:CURR:RANG %s" % self.DEFAULTIRANGE)  # Set to current compliance
#             self.keithley.write("SENS:CURR:RANG:AUTO ON") # Set to current compliance
#            self.setIlim(self.DEFAULTILIM) 
#            self.keithley.write("SENS:CURR:RANG:AUTO ON") # Set range to auto
            self.setV(self.DEFAULTV)
            self.keithley.write("FORM:ELEM CURR")
        if self.mode == 'Rsense':
            self.keithley.write("SENS:FUNC 'RES'")  # Select resistance measurement function
            self.keithley.write("SENS:RES:MODE MAN")  # Select manual ohms mode
#             self.keithley.write("SENS:RES:RANGE 2") # Select measurement range (might not be needed in manual ohms mode)
            self.keithley.write("SOUR:FUNC CURR")  # Select current as the source
            self.keithley.write("SOUR:CURR:RANG 0.1")  # Select current range
            self.keithley.write("SOUR:CURR 0.01")  # Select source current
            self.keithley.write("SYST:RSEN ON")  # turn on remote sense (4-wire)
            self.keithley.write("SENS:RES:OCOM ON")  # Turn on offset compensation (compensates internal temperature dependent offsets). 
            self.keithley.write("SENS:VOLT:PROT 1")  # Select voltage compliance to 1 V
            self.keithley.write("FORM:ELEM RES")  # only returns resistance readings    

        if self.mode == 'Vsense':  # Keithley Manual p 105
            self.keithley.write("SOUR:FUNC CURR")
            self.keithley.write("SOUR:CURR:MODE FIXED")
            self.keithley.write("SENS:FUNC 'VOLT'")
            self.keithley.write("SOUR:CURR:RANG MIN")
            self.keithley.write("SOUR:CURR:LEV 0")
            self.keithley.write("SENS:VOLT:PROT 1.2")
            self.keithley.write("SENS:VOLT:RANG 1")
            self.keithley.write("FORM:ELEM VOLT")
            self.outputOn()
        return mode
      
    def setV(self, V):
        Vold = self.getV()
        if float(V) <= self.DEFAULTVMAX:          
            self.keithley.write("SOUR:VOLT:LEV %s" % V)  # Set voltage level
        else:
            self.keithley.write("SOUR:VOLT:LEV %s" % Vold)  # Set voltage level
            print ('V > Vmax. \nV remains %.3f V' % float(Vold))    
        
    def setIlim(self, Ilim):
        self.keithley.write("SENS:CURR:PROT %s" % Ilim)  # Set to current compliance
        
    def setIrange(self, Irange):
        self.keithley.write("SENS:CURR:RANG %s" % Irange)
        
    def getIlim(self):
        return self.keithley.ask("SENS:CURR:PROT:LEV?")  # manual p 391
    
    def getV(self):
        return self.keithley.ask("SOUR:VOLT:LEV:IMM:AMPL?")  # manual p 395
    
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
        if self.mode == 'Isense':
            self.keithley.write("INIT")  # Initialize
            return float(self.keithley.ask("FETC?"))
        else:
            print 'Cannot measure I when configured to {0}'.format(self.mode)
            
    def measV(self):
        if self.mode == 'Vsense':
            self.keithley.write("INIT")  # Initialize
            return float(self.keithley.ask("FETC?"))
        else:
            print 'Cannot measure V when configured to {0}'.format(self.mode)            
        
    
    def measR(self):
        if self.mode == 'Rsense':
#            self.outputOn()
            self.keithley.write("INIT")  # Initialize
    #        self.keithley.write("*TRG") # Trigger once
            R = self.keithley.ask("FETC?")
#            self.outputOff()
            return R    
        else:
            print 'Cannot measure R when configured to {0}'.format(self.mode)
            
    def close(self):
        try:
            self.outputOff()
            self.keithley.close()
        except Exception as e:
            print(str(e))                      
        
        
    
        
