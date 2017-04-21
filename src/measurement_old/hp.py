import visa
# import devices

class Hp():
    def __init__(self):
        self.DEFAULTFREQ = 10e-9
        self.DEFAULTHIGH = 1
        self.DEFAULTLOW = 0
        
#        self.initme()
        
    def initme(self, devices, unique):
#        try:
#            visaInstrList = visa.get_instruments_list()
#        except Exception as e:
#            print(str(e))
#        else:
#            self.hp = visa.instrument(visaInstrList[0]+'::INSTR')
            self.hp = devices.findUnique(unique)
            self.hp.write("*RST")
            self.hp.write("*CLS")
            self.defaultSetup()
            return self.hp.ask("*IDN?")
      
        
    def defaultSetup(self):
        self.outputOff()
        self.hp.write("PULS1:TIM:DCYC:MODE ON")
        self.hp.write("PULS1:TIM:DCYC 50")
        self.hp.write("PULS2:TIM:DCYC:MODE ON")
        self.hp.write("PULS2:TIM:DCYC 50")    
        self.setFreq(self.DEFAULTFREQ)
        self.setHigh(self.DEFAULTHIGH)
        self.setLow(self.DEFAULTLOW)
      
    def setFreq(self, per):
        self.hp.write("PULS:TIM:PER %s" % per)      
        
    def setHigh(self, high):
        self.hp.write("PULS:LEV:HIGH %s" % high)
        
    def setLow(self, low):
        self.hp.write("PULS:LEV:LOW %s" % low)
        
    def getFreq(self):
        return self.hp.ask("PULS:TIM:PER?")  # manual p 29

    def setOutput(self, state):
        if state == 'ON':
            self.outputOn()
        else:
            self.outputOff()

    def outputOn(self):
        self.output1on()
        self.output2on()
    
    def outputOff(self):
        self.output1off()
        self.output2off()
    
    def output1on(self):
        self.hp.write("OUTP:PULS:STATe ON")
        
    def output2on(self):
        self.hp.write("OUTP:PULS:CSTate ON")        
        
    def output1off(self):
        self.hp.write("OUTP:PULS:STAT OFF")
        
    def output2off(self):
        self.hp.write("OUTP:PULS:CSTate OFF")  
        
    def getOutput(self):
        return self.hp.ask("OUTP:PULS:STAT?")  # manual p 29
        
    def close(self):
        try:
            self.outputOff()
            self.hp.close()    
        except Exception as e:
            print(str(e))      
            
        
