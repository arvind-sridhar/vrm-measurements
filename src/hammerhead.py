#!/usr/bin/python
from telnetlib import Telnet
import socket
import time
import re

class Hammerhead():
    
    
    # HOST = '192.168.1.200'
    # HOST = '9.4.208.191' #hh2 
    # HOST = '9.4.208.190' #hh1 -before
    HOST = '9.4.208.196'  # hh3
    BOOL_START_TELNET = True
    BOOL_PRINT_TELNET = True
    
    def __init__(self):
        super(Hammerhead, self).__init__()
        self.initH()

        self.tn = None;

    def initH(self):
        
        self.ADDR = self.__class__.HOST
        
        # TODO: Fix address
#       self.ADDR = 'hh3'
        self.CHANNEL = 0
        self.PORT = 55555
        self.DEBUGLEVEL = 2
        # minimum HHSPEED setting which is working: 2, very safe is 100
        self.MODE = 0  # 0x33 for old 13s behavior
        self.HHSPEED = 100
    
    
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.isConnected = False
    
    def connect(self) -> bool:
        try:
            
            # Telnet Part
            print('Starting Telnet...')
            tn = Telnet(self.ADDR)
            tn.write(b"cd miromico\r")
            tn.write(b"killall bidisrv.speedy_v2\r")
            
            if(self.BOOL_START_TELNET):
                print('Starting bidisrv...')
                tn.write(b"./run-bidisrv\r")
            
            self.tn = tn
            
            self.s.settimeout(2)
            
            print('connecting...')
            self.s.connect((self.ADDR, self.PORT))
            
        except Exception as e:
            
            raise Exception('Something\'s wrong with %s:%d. Exception type is %s' % (self.ADDR, self.PORT, e))
            self.isConnected = False
        else:
            self.isConnected = True
            self.printTelnet()
            print('done.')
            
        return self.isConnected
    
    def disconnect(self) -> bool:
        if(self.isConnected):
            print('disconnecting...')
            
            self.s.close()
            if self.tn!=None:
                
                self.tn.write(b'\x03')
                self.printTelnet()
                self.tn.close()
                self.tn = None
            
            self.initH()
            
            print('done.')
            
            
        return self.isConnected==False
    
    def write(self, addr:int, data:str) -> bool:
        '''
        Writes bytes to socket
        :param addr:int Address of BIDI Register
        :param data:str String with new register content
        '''
        assert self.isConnected
        byteData = self.bytes('w ' + str(addr) + ' ' + str(data) + '\n')
        numBytes = self.s.sendall(byteData)
        
        self.printTelnet()
        
        return True#numBytes == len(byteData)
        
    def read(self, addr:int) -> int:
        
        assert self.isConnected
        self.s.sendall(self.bytes('r ' + str(addr) + '\n'))  # , 'ascii'))
        return int(self.s.recv(1024))

    def readRange(self, addr) -> list:
        # addr2=addr[0:100]
        # addr = addr2
        # sendString = ""
        for i in addr:
            self.s.sendall(bytes('r ' + str(i) + '\n'))  # , 'ascii'))
            # sendString = sendString + 'r '+str(i)+'\n'
        # self.s.sendall(bytes(sendString, 'ascii'))
        leftOver = ''
        readArr = list()
        self.s.setblocking(False)
        # self.s.settimeout(0.001)
        while (len(readArr) < len(addr)):
            try:
                bArr = self.s.recv(len(addr) * 10)
            except:
                bArr = []
            # print(bArr)
            if len(bArr) > 0:
                recStr = (leftOver + bArr.decode()).split('\n')
                leftOver = recStr[-1]
                readArr.extend(recStr[0:-1])
            # else:
            #    readArr.append(leftOver)
        
        readArrInt = list()
        for i in readArr:
            try:
                readArrInt.append(int(i))
            except:
                print('Error:' + i)
        # print(len(readArrInt))
        return readArrInt
    
    def writerd(self, addr:int, data:int) -> bool:
        """Write reverse data"""
        return self.write(addr, self.reverseBits(data, 12))    
  
    def writera(self, addr:int, data:int) -> bool: 
        """Write reverse address"""
        return self.write(self.reverseBits(addr, 11), data)

    def readra(self, addr:int) -> int:
        return self.read(self.reverseBits(addr, 11))

    def readraRange(self, addr:int)-> list:
        addrR = list()
        for i in addr:
            addrR.append(self.reverseBits(i, 11))
        return self.readRange(addrR)
    
    def init(self) -> None:
        print('Initializing...')
        self.s.sendall(bytes('debug ' + str(self.DEBUGLEVEL) + '\n' , 'ascii'))
        self.s.sendall(bytes('c ' + str(self.CHANNEL) + '\n', 'ascii'))
        self.s.sendall(bytes('s ' + str(self.HHSPEED) + '\n', 'ascii'))
        self.s.sendall(bytes('m ' + str(self.MODE) + '\n', 'ascii'))
        self.s.sendall(bytes('i\n', 'ascii'))
        print('done.')

    def reverseBits(self, i:int, nbits:int) -> int:
        ibin = bin(i)[2:]
        ibin = '0' * (nbits - len(ibin)) + ibin
        # print ibin
        return int(ibin[::-1], 2)
    
    def printTelnet(self):
        
        if Hammerhead.BOOL_PRINT_TELNET:
            return
        
        time.sleep(0.005)
        string = str(self.tn.read_very_eager(),'ascii')
        if len(string)==0:
            return
        string=re.sub('\n', '', string)
        string=re.sub('\r', '\n', string)
        print("HH: "+ string)
    
    def bytes(self,intx:int)->bytes:
        return bytes(intx,"ascii")
