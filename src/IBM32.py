#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on Apr 12, 2017

@author: rid
'''

import sys
import hammerhead


from PyQt5 import QtWidgets
from IBM32_tools import IBM32_GUI
from GF1408_tools import GF1408_BIDI
from GF1408_tools.GF1408_MConfig import GF1408config
from measurement.setup import MeasurementSetup



def main():
    
    
    app = QtWidgets.QApplication(sys.argv)
    
    hh = hammerhead.Hammerhead()
    BIDI = GF1408_BIDI.GF1408_BIDI( hh,GF1408_BIDI.IBM32_BIDI_REGISTERLIST )
    config = GF1408config()
    mSetup = MeasurementSetup( config )
    
    IBM32_GUI.IBM32_GUI(BIDI, hh, mSetup)
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
