'''
Created on Apr 19, 2017

@author: rid
'''

class GuiTools(object):
    '''
    classdocs
    '''


    def __init__(self, parent):
        '''
        Constructor
        '''
        super(GuiTools,self).__init__()
        self.parent = parent
        self.mainLayout = None
    
    @staticmethod
    def layout_widgets(layout):
        return (layout.itemAt(i).widget() for i in range(layout.count()))


    def setEnabled(self,en):
        if(self.mainLayout == None):
            return
        for obj in GuiTools.layout_widgets(self.mainLayout):
            if hasattr(obj, 'isEnabled'):
                obj.setEnabled(en)
                