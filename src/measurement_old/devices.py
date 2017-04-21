# from numpy import *


from INSTRUMENTS import *
import visa
        
class Devices():
    def __init__(self):        
        self.initme()    

    def initme(self):    
#        self.INSTNAMES = ['inst0', 'inst1', 'inst2', 'inst3', 'inst4', 'inst5', 'inst6', 'inst7', 'inst8', 'inst9']            
        self.instrList()
        
    def findUnique(self, unique):
        for i in range(0, len(self.visaInstrList)):
            inst = visa.ResourceManager().instrument(self.visaInstrList[i] + '::INSTR')
            if isinstance(unique, int):
                if str(unique) in self.instrList()[i]:
                    return inst
            if isinstance(unique, str):
                if unique in inst.ask("*IDN?"):
                    return inst
#            globals()[self.INSTNAMES[i]]=visa.instrument(self.visaInstrList[i]+'::INSTR')
#            if unique in globals()[self.INSTNAMES[i]].ask("*IDN?"):
#                return globals()[self.INSTNAMES[i]]
        
    def instrList(self):
        try:
#            x = visa.get_instruments_list()
            # for i in range(len(self.visaInstrList),0):
            #   if not 'GPIB' in self.visaInstrList[i]:
            #      self.visaInstrList.pop(i)
            #     print self.visaInstrList
            self.visaInstrList = [s for s in visa.ResourceManager().list_resources() if 'GPIB' in s]  # Removes all non-GPIB entries from the instrument list 
#            print self.visaInstrList
            return self.visaInstrList
#        y = [s for s in x if len(s) == 2]
        except Exception as e:
            print(str(e))
        
    def printInstrList(self):
        for i in range(0, len(self.visaInstrList)):
            inst = visa.ResourceManager().instrument(self.visaInstrList[i] + '::INSTR')
            print(inst.ask("*IDN?"))
#            globals()[self.INSTNAMES[i]]=visa.instrument(self.visaInstrList[i]+'::INSTR')
#            print globals()[self.INSTNAMES[i]].ask("*IDN?")
        

if __name__ == '__main__':    
    devs = Devices()
#     devs.printInstrList()
    VinSupply = agilentDC.AgilentDC()
    
    print('VinSupply = ' + VinSupply.initme(devs, 'E3633A', 2, 5))
    VinSupply.outputOn()
    print(VinSupply.getI())
    VinSupply.outputOn()
    VinSupply.setImax(4)
    VinSupply.setVmax(3)
    
