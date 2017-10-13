#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on Apr 12, 2017

@author: rid
'''

import sys
import hammerhead

from PyQt5 import QtWidgets
from GF1408_tools import GF1408_GUI,GF1408_BIDI
from GF1408_tools.GF1408_MConfig import GF1408config
from measurement.setup import MeasurementSetup

def main():

	a=1 # dummy command- to test git new branch
    
    app = QtWidgets.QApplication(sys.argv)
    
    hh = hammerhead.Hammerhead()
    BIDI = GF1408_BIDI.GF1408_BIDI( hh,GF1408_BIDI.GF1408_BIDI_REGISTERLIST )
    config = GF1408config()
    mSetup = MeasurementSetup( config )
    
    gui=GF1408_GUI.GF1408_GUI(BIDI, hh, mSetup)
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
