import visa
#import devices

class Agilent8648D():
    def __init__(self):
        self.DEFAULTFREQ   = 2000 # MHz
        self.DEFAULTAMPLITUDE  = 500 # mV
                
    def initme(self, devices, unique, defaultFreq, defaultAmplitude):
        self.DEFAULTFREQ   = defaultFreq # MHz
        self.DEFAULTAMPLITUDE  = defaultAmplitude # mV
        
        self.device = devices.findUnique(unique)
        self.device.write("*RST")
        self.device.write("*CLS")
        self.defaultSetup()
        return self.device.ask("*IDN?")
      
        
    def defaultSetup(self):
        self.outputOff()
        self.setFreq(self.DEFAULTFREQ)
        self.setAmplitude(self.DEFAULTAMPLITUDE)
  
    def setFreq(self, freq):
        self.device.write("FREQ:CW {0} MHz".format(freq))      
        
    def setAmplitude(self, amplitude):
        self.device.write("POW:AMPL {0} mV".format(amplitude))
        
    def getAmplitude(self):
        return ((10**(float(self.device.ask("POW:AMPL?"))/10))/20)**0.5
        
    def getFreq(self):
        return float(self.device.ask("FREQ:CW?")) 
    
    def setOutput(self, onOff):
        if onOff == 'ON':
            self.outputOn()
        else:
            self.outputOff()            

    def outputOn(self):
        self.device.write("OUTP:STAT ON")
    
    def outputOff(self):
        self.device.write("OUTP:STAT OFF")
 
    def getOutput(self):
        return self.device.ask("OUTP:STAT?")
    
    def close(self):
        try:
            self.outputOff()
            self.device.close()
        except Exception as e:
            print(str(e))      
                 