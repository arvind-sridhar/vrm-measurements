'''
Created on Apr 24, 2017

@author: rid
'''

import numbers
import numpy

from typing import List, Union, Any



class BIDI_PARAMETER():
    
    VAL_ISLINEAR = 0
    VAL_BITRANGE = 1
    VAL_STDVAL = 3
    VAL_MAPFUN = 4
            
    
    @staticmethod
    def fromListe(name, liste:List[Union[bool,int,int,int,str]], bidiRegisters:"BIDI_REGISTERS", Registers:"GF1408_BIDI_REGISTERLIST")->"BIDI_PARAMETER":
        
        self = BIDI_PARAMETER
        
        if(liste[self.VAL_ISLINEAR]):
            startBit = liste[self.VAL_BITRANGE]
            Length = liste[self.VAL_BITRANGE + 1]
            bitrange = numpy.arange(startBit, startBit + Length)
        else:
            bitrange = liste[self.VAL_BITRANGE]
        
        
        if len(liste) > (self.VAL_MAPFUN):
            # print liste[self.VAL_MAPFUN]
            fun = getattr(Registers, liste[self.VAL_MAPFUN])
        else:
            fun = None    
        
        return  BIDI_PARAMETER(name, bitrange, bidiRegisters, fun)
    
    def __init__(self, name, bitrange_array:numpy.ndarray, bidiRegisters, mapFun=None):    
        
        assert len(bitrange_array.shape) == 1
        assert bitrange_array.size > 0
        
        self.BIDI = bidiRegisters
        self.name = name
        self.bitrange_array = bitrange_array
        
        self.mapFun = mapFun
        
        bidiRegisters.setRegisterParamter(bitrange_array, name)
        
    def set(self, newValue:Union[Any,int])->None:
        
        if self.mapFun != None:
            newValue = self.mapFun(newValue)
        
        Length = len(self.bitrange_array)
        
       
        assert(isinstance(newValue, numbers.Integral))
        
        # Convert to binary
        newValue_bin = ("{0:0" + str(Length) + "b}").format(newValue)
        
        assert(len(newValue_bin) <= Length)
        
        
        newValue_bin_array = numpy.zeros(shape=(Length), dtype=numpy.int)
        
        i = len(newValue_bin)-1
        for char in newValue_bin:
            newValue_bin_array[i] = int(char)
            i = i - 1
        
        print(newValue_bin_array)
        print(self.BIDI.updateRegister(self, newValue_bin_array))
    
