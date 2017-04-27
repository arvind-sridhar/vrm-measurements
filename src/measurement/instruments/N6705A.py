'''
Created on Apr 21, 2017

@author: rid

copied from lku
'''


from measurement.instruments.instrParentClass import InstrParent 

#===============================================================================
#  One class equals one channel of the N6705
#===============================================================================

class N6705A(InstrParent):
    """4 channel power supply"""
    def __init__(self, instr, channel, voltageProtectionLevel, alreadyReset):
        self.instr = instr
        self.channel = channel
        self.voltageProtectionLevel = voltageProtectionLevel
        # Set maximum allowed voltage level
        self.instr.write("VOLT:PROT:LEV " + str(voltageProtectionLevel) + "V,(@" + str(channel) + ")")
        # Init to 0V
        self.instr.write("VOLT:RANG 5,(@" + str(channel) + ")")
    def reset(self, alreadyReset=False):
        if not alreadyReset:
            self.instr.write("*RST")
            self.instr.write("*CLS")
        self.instr.write("VOLT:SENS:SOUR INT,(@" + str(self.channel) + ")")
        self.instr.write("VOLT 0V,(@" + str(self.channel) + ")")
        self.instr.write("OUTP ON,(@" + str(self.channel) + ")")
    def setVoltage(self, volt):
        if volt > self.voltageProtectionLevel:
            print('Voltage too high! Set: ' + str(volt) + ', Allowed: ' + str(self.voltageProtectionLevel))
            return
        self.instr.write("VOLT " + str(volt) + "V,(@" + str(self.channel) + ")")
        self.instr.write("OUTP ON,(@" + str(self.channel) + ")")
    def getVoltage(self):
        return float(self.instr.ask("VOLT? (@" + str(self.channel) + ")"))
    def setVoltageProtection(self, volt):
        self.voltageProtectionLevel = volt
        self.instr.write("VOLT:PROT:LEV " + str(self.voltageProtectionLevel) + "V,(@" + str(self.channel) + ")")
    def getVoltageProtection(self):
        return float(self.instr.ask("VOLT:PROT:LEV? (@" + str(self.channel) + ")"))
    def setMaxCurrent(self, curr):
        self.instr.write("CURR:LEV " + str(curr) + "A,(@" + str(self.channel) + ")")
    def getMaxCurrent(self):
        
        print(1)
        return float(self.instr.ask("CURR:LEV? (@" + str(self.channel) + ")"))
    
    def measureVoltage(self):
        return float(self.instr.ask("MEAS:VOLT? (@" + str(self.channel) + ")"))
    def measureCurrent(self):
        # Returns Average Output Current
        return float(self.instr.ask("MEAS:CURR? (@" + str(self.channel) + ")"))
    def clearProtection(self):
        self.instr.write("POW:PROT:CLE (@" + str(self.channel) + ")")
    def isProtectionTriggered(self):
        # return self.instr.ask("POW:PROT:CLE? (@"+str(self.channel)+")")
        return False
    # Enable or disable 4 point measurement. EXT means enable
    def set4Point(self, is4Point):
        if is4Point:
            self.instr.write("VOLT:SENS:SOUR EXT,(@" + str(self.channel) + ")")
        else:
            self.instr.write("VOLT:SENS:SOUR INT,(@" + str(self.channel) + ")")
    def get4Point(self):
        return self.instr.ask("VOLT:SENS:SOUR? (@" + str(self.channel) + ")") == "EXT"
    def release(self):
        # Release remote control by GPIB and allow local control
        # If it is not working, try instr.unlock() or inst.local()
        self.instr.write("SYST:COMM:RLST LOC")
    def getInstr(self):
        return self.instr
    def close(self):
        self.instr.close()
        
    #TODO: AddFDatalog Functions