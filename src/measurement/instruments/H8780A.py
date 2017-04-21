'''
Created on Apr 21, 2017

@author: rid

copied from lku
'''
from measurement.instruments.instrParentClass import InstrParent 


class H8780A(InstrParent):
    # channel is not used in this class
    def __init__(self, instr, powerProtectionLevel, alreadyReset):
        self.instr = instr
        self.powerProtectionLevel = powerProtectionLevel

        # Since this device does not allow to read out all the values,
        # they are stored in local variables.
        self.currentFreq = 0
        self.currentAmpDBm = -110
        # Set maximum allowed voltage level
        
    def reset(self, alreadyReset=False):
        if not alreadyReset:
            self.instr.write("PR")
            self.instr.write("SP0")
        self.instr.write("LV -110 DBM")
        self.instr.write("RF1")
    # set Power in dBm
    def setPowerDBm(self, power):
        if power > self.powerProtectionLevel:
            print('Power too high! Set: ' + str(power) + ', Allowed: ' + str(self.powerProtectionLevel))
            return
        self.instr.write("LV " + str(power) + " DBM")
        self.currentAmpDBm = power
        self.instr.write("RF1")
    def getPowerDBm(self):
        return self.currentAmpDBm
    def setFrequency(self, freq):
        self.instr.write("FR " + str(freq) + " HZ")
        self.currentFreq = freq
    def getFrequency(self):
        return self.currentFreq
    def release(self):
        # Release remote control by GPIB and allow local control
        # If it is not working, try instr.unlock() or inst.local()
        return
#        self.instr.write("RL1")
    def getInstr(self):
        return self.instr
    def close(self):
        self.instr.close()
