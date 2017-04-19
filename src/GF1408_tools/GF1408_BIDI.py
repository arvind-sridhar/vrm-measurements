'''
Created on Apr 13, 2017

@author: rid
'''

from BIDI_REGISTERS import BIDI_REGISTERS
import numpy

class GF1408_BIDI_REGISTERLIST():

    EN_PH_0 = [True,8,1]
    EN_PH_1 = [True,9,1]
    EN_PH_2 = [True,10,1]
    EN_PH_3 = [True,11,1]
    
    SEL_0 = [True, 12,2]
    SEL_1 = [True, 14,2]
    SEL_2 = [True, 16,2]
    SEL_3 = [True, 18,2]
    
    LOAD_EN = [True, 24,32]


class GF1408_BIDI( BIDI_REGISTERS ):

    BIDI_SIZE = 24

    def __init__( self, _hammerhead ):
        '''
        Constructor
        '''
        super( GF1408_BIDI, self ).__init__( self.BIDI_SIZE, _hammerhead, GF1408_BIDI_REGISTERLIST )



