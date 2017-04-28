'''
Created on Apr 13, 2017

@author: rid
'''

import threading
import numpy
from xlrd.formula import num2strg

from GF1408_tools.BIDI_PARAMETER import BIDI_PARAMETER


class BIDI_REGISTERS(object):
    '''
    classdocs
    '''
    WORD_LENGTH = 12
    HAMMERHEAD = None

    def __init__(self, _registerCount:int, _hammerhead:"hammerhead.Hammerhead", _RegisterListClass):
        '''
        Constructor
        '''
        self.registerCount = _registerCount;
        self.bitCount = _registerCount * self.WORD_LENGTH
        
        self.registers_Used = numpy.zeros(shape=(_registerCount, self.WORD_LENGTH), dtype=numpy.int)
        self.registers_Bits = numpy.zeros(shape=(_registerCount, self.WORD_LENGTH), dtype=numpy.int)
        self.register_Names = [None] * self.bitCount
        
        self.HAMMERHEAD = _hammerhead;
        self.RegisterListClass = _RegisterListClass
        
        self.lock = threading.RLock()
    
        self.initRegisters()
        
    def allBits(self) -> numpy.ndarray:
        return self.registers_Bits.reshape(self.bitCount)
    
    def allRegistersUsage(self) -> numpy.ndarray:
        
        return self.registers_Used.reshape(self.bitCount)
        
    def setRegisterParamter(self, _bitrangeArray:numpy.ndarray, _registerName:str) -> None:
        
        # 1. Check if defined range is available 
        if (self.allRegistersUsage()[_bitrangeArray] != 0).any():
            
            overlapIDs_local = (self.allRegistersUsage()[_bitrangeArray] != 0)
            overlapIDs_global = _bitrangeArray[overlapIDs_local]
            oneOverlap = overlapIDs_global[0]
            
            raise IndexError("Registers are already used for {}".format(self.register_Names[oneOverlap]))
        
        for name in self.register_Names:
            if(name == _registerName):
                raise NameError("Name is already in use: {}".format(_registerName))
        
        # 2. Register Range
        self.allRegistersUsage()[_bitrangeArray] = 1
        for i in _bitrangeArray:
            self.register_Names[i] = _registerName
        #print(self.register_Names)

    def updateRegister(self, bidi_parameter:BIDI_PARAMETER, value_array:numpy.ndarray) -> bool:
        
        # 0. Ensure bitrange is valid
        
        assert bidi_parameter.bitrange_array.shape == value_array.shape
        
        # 1. Overwrite mentioned registers
        self.allBits()[bidi_parameter.bitrange_array] = value_array
        
        # 2. Prepare addresses and bit list
        AlteredAdresses = bidi_parameter.bitrange_array / self.WORD_LENGTH 
        UpdatedRegisters = numpy.unique(AlteredAdresses.astype(numpy.int))
        
        # 3. Iterate over updated registers and write to Bidi
        success = True
        for address in numpy.nditer(UpdatedRegisters):
            
            success = success and self.writeRegister(address)
            
        return success

    def initRegisters(self) -> None:
        
        RegisterClass = self.RegisterListClass
        Registers = self.RegisterListClass.__dict__.items()
        
        for name, liste in  Registers:
            
            if not ("__") in name and not ("static") in name and not liste==None:
                
                BIDIParameter = BIDI_PARAMETER.fromListe(name, liste, self, RegisterClass)
                setattr(self, name, BIDIParameter)
    
    def updateAllRegisters(self)->bool:
        
        success = True
        for address in range(0,self.registerCount):
            success = success and self.writeRegister(address)
        return success
        
    def writeRegister(self,address:int)->bool:
        with self.lock:
            assert address in range(0,self.registerCount)
            content = self.registers_Bits[address]
            bitstring = numpy.array2string(content, separator='')[1:-1]
            print("Write to " + num2strg(address) + " : " + bitstring)
            return self.HAMMERHEAD.write( address,int(bitstring,2) )    
    