'''
Created on Apr 27, 2017

@author: rid

'''


from GF1408_tools.BIDI_REGISTERS import BIDI_REGISTERS
from measurement.setup import MeasurementSetup 


from GF1408_tools.GF1408_GUI import GF1408_GUI

class IBM32_GUI(GF1408_GUI):
    '''
    classdocs
    '''
    WINDOW_NAME = 'CarrICool IBM32 - Control Window'

    def __init__(self, _BIDI:BIDI_REGISTERS, _hammerhead, _setup:MeasurementSetup):
        '''
        Constructor
        '''
        super(IBM32_GUI, self).__init__( _BIDI, _hammerhead, _setup)
        
        
        