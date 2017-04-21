'''
Created on Apr 21, 2017

@author: rid

copied from lku
'''

from measurement.instruments.N6705A import N6705A

class N6705B(N6705A):
    def __init__(self, instr, channel, voltageProtectionLevel, alreadyReset):
        N6705A.__init__(self, instr, channel, voltageProtectionLevel, alreadyReset)
    def setMaxCurrent(self, curr):
        self.instr.write("CURR:LIM " + str(curr) + ",(@" + str(self.channel) + ")")
    def getMaxCurrent(self):
        return float(self.instr.ask("CURR:LIM? (@" + str(self.channel) + ")")) 