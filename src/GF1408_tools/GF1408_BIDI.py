'''
Created on Apr 13, 2017

@author: rid
'''

from GF1408_tools import GF1408_CONST
from GF1408_tools.BIDI_REGISTERS import BIDI_REGISTERS


class GF1408_BIDI_REGISTERLIST():
    '''
    Class holding the BIDI Registers of the 1410 Tapeout
    
    For linear registers the following arrangement was used:
    {List} = [Is_linear:bool, Startbit:int, Bitcount:int, Standardvalue:int, mapfuncname:str]
    '''

    DPWM_EN = [True, 0, 1, 1]
    DPWM_RST = [True, 1, 1, 0]
    DPWM_DUTY = [True, 2, 4, 2 ** 3, "static_mapDUTYcycle2int"]
    DPWM_DT_N = [True, 6, 3, 0, "static_mapDT2int"]
    DPWM_DT_P = [True, 9, 3, 0, "static_mapDT2int"]

    SEL_0 = [True, 12 + 0, 2, 0, "static_mapSEL2int"]
    SEL_1 = [True, 12 + 2, 2, 1, "static_mapSEL2int"]
    SEL_2 = [True, 12 + 4, 2, 2, "static_mapSEL2int"]
    SEL_3 = [True, 12 + 6, 2, 3, "static_mapSEL2int"]

    EN_PH_0 = [True, 12 + 8, 1, 1]
    EN_PH_1 = [True, 12 + 9, 1, 1]
    EN_PH_2 = [True, 12 + 10, 1, 1]
    EN_PH_3 = [True, 12 + 11, 1, 1]

    LOAD_EN = [True, 2 * 12 + 0, 32,0, "static_mapLOADEN2int"]
    LOAD_CTRL_EN = [True, 4 * 12 + 8, 1,1]
    LOAD_CTRL_PROG = [True, 4 * 12 + 9, 1,1]
    LOAD_CTRL_SEL_CLK = [True, 4 * 12 + 10, 2,1, "static_mapLOADCLK2int"]

    @classmethod
    def static_mapSEL2int(BIDI_PARAM, degree_String:str) -> int:
        return GF1408_CONST.CONST.DEG_STR.index(degree_String)

    @classmethod
    def static_mapLOADEN2int(BIDI_PARAM, loaden_int:int):

        ResblockCount = 4
        LoadCount = int(loaden_int)
        loadNums = [0] * ResblockCount

        for count in range(ResblockCount, 0, -1):
            if(count > 0):
                distributedLoad = int(LoadCount / count)
            else:
                distributedLoad = count
            for i in range(0, count):
                loadNums[i] += distributedLoad
            LoadCount = LoadCount - count * distributedLoad

        CODE = 0
        BitWidth = GF1408_BIDI_REGISTERLIST.LOAD_EN[2] / ResblockCount
        for i in range(0, 4):
            CODE += (2 ** loadNums[i] - 1) * 2 ** (i * BitWidth)

        return int(CODE)

    @classmethod
    def static_mapDT2int(BIDI_PARAM, DT_int:int) -> int:
        return int(int(DT_int) / GF1408_CONST.CONST.DT_STEP_N) - 1

    @classmethod
    def static_mapDUTYcycle2int(BIDI_PARAM, DUTY_float:float) -> int:
        return int(DUTY_float / (100.0 * 2 ** (-GF1408_CONST.CONST.DUTY_BITS)))

    @classmethod
    def static_mapLOADCLK2int(BIDI_PARAM, CKString:str) -> int:
        return GF1408_CONST.CONST.LOAD_CK_ARR.index(CKString)

class GF1408_BIDI(BIDI_REGISTERS):

    BIDI_SIZE = 24

    def __init__(self, _hammerhead):
        '''
        Constructor
        '''
        super(GF1408_BIDI, self).__init__(self.BIDI_SIZE, _hammerhead, GF1408_BIDI_REGISTERLIST)



