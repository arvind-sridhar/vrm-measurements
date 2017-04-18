'''
Created on Apr 13, 2017

@author: rid
'''

from GF1408_tools.BIDI_REGISTERS import BIDI_REGISTERS
from GF1408_tools.BIDI_REGISTERS import BIDI_PARAMETER
import hammerhead # the serial interface board


class GF1408_BIDI(BIDI_REGISTERS):
    
    BIDI_SIZE = 24

    def __init__(self,hammerhead):
        '''
        Constructor
        '''
        super(GF1408_BIDI, self).__init__(self.BIDI_SIZE,hammerhead)
        self.initRegisters(self);
        
        
        
    def initRegisters(self):
        
        self.PHASE_SEL_0 = BIDI_PARAMETER.linear('SEL_0', 12, 2, self)
        self.PHASE_SEL_1 = BIDI_PARAMETER.linear('SEL_1', 14, 2, self)
        self.PHASE_SEL_2 = BIDI_PARAMETER.linear('SEL_2', 16, 2, self)
        self.PHASE_SEL_3 = BIDI_PARAMETER.linear('SEL_3', 18, 2, self)