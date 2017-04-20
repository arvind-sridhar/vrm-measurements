'''
Created on Apr 13, 2017

@author: rid
'''

from BIDI_REGISTERS import BIDI_REGISTERS
from test.test_binop import isint
from GF1408_tools import GF1408_CONST

class GF1408_BIDI_REGISTERLIST():
    
    DPWM_EN = [True,0,1]
    DPWM_RST = [True,1,1]
    DPWM_DUTY = [True,2,4,"static_mapDUTYcycle2int"]
    DPWM_DT_N = [True,6,3,"static_mapDT2int"]
    DPWM_DT_P = [True,9,3,"static_mapDT2int"]

    SEL_0 = [True, 12+0,2,"static_mapSEL2int"]
    SEL_1 = [True, 12+2,2,"static_mapSEL2int"]
    SEL_2 = [True, 12+4,2,"static_mapSEL2int"]
    SEL_3 = [True, 12+6,2,"static_mapSEL2int"]
    
    EN_PH_0 = [True,12+8,1]
    EN_PH_1 = [True,12+9,1]
    EN_PH_2 = [True,12+10,1]
    EN_PH_3 = [True,12+11,1]
    
    LOAD_EN = [True, 2*12+0,32,"static_mapLOADEN2int"]
    LOAD_CTRL_EN = [True, 4*12+8,1]
    LOAD_CTRL_PROG = [True, 4*12+9,1]
    LOAD_CTRL_SEL_CLK = [True, 4*12+10,2]
    
    @classmethod
    def static_mapSEL2int(BIDI_PARAM,degree_String):
        newStr = ""
        for char in degree_String:
            if char in ("0123456789"):
                newStr = newStr+char
        return int(newStr)/90

    @classmethod
    def static_mapLOADEN2int(BIDI_PARAM,loaden_int):
        
        ResblockCount = 4
        LoadCount = int(loaden_int)
        loadNums = [0]*ResblockCount
        
        for count in range(ResblockCount,0,-1):
            if(count>0):
                distributedLoad = LoadCount/count
            else:
                distributedLoad = count
            for i in range(0,count):
                loadNums[i]+=distributedLoad
            LoadCount = LoadCount-count*distributedLoad
        
        CODE = 0
        BitWidth = GF1408_BIDI_REGISTERLIST.LOAD_EN[2]/ResblockCount
        for i in range(0,4):
            CODE+=(2**loadNums[i]-1)*2**(i*BitWidth)
        
        return CODE

    @classmethod
    def static_mapDT2int(BIDI_PARAM,DT_int):
        CODE = int(DT_int)/GF1408_CONST.CONST.DT_STEP_N-1
        return CODE
    
    @classmethod
    def static_mapDUTYcycle2int(BIDI_PARAM,DUTY_float):
        CODE = int(DUTY_float/(100.0*2**(-GF1408_CONST.CONST.DUTY_BITS)))
        print CODE
        return CODE
    
class GF1408_BIDI( BIDI_REGISTERS ):

    BIDI_SIZE = 24

    def __init__( self, _hammerhead ):
        '''
        Constructor
        '''
        super( GF1408_BIDI, self ).__init__( self.BIDI_SIZE, _hammerhead, GF1408_BIDI_REGISTERLIST )
        


