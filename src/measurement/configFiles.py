'''
Created on Apr 21, 2017

@author: rid
'''

class configParent():
    '''
    classdocs
    '''
    INST = None

    def __init__(self):
        '''
        Constructor
        '''

    @staticmethod
    def singleton():
        self = configParent
        
        if(self.INST==None):
            return self()
        return self.INST
