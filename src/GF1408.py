#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on Apr 12, 2017

@author: rid
'''

import sys, hammerhead

from PyQt5 import QtWidgets
from GF1408_tools import GF1408_GUI,GF1408_BIDI
from GF1408_tools.GF1408_MConfig import GF1408config
from measurement.setup import MeasurementSetup


def main():
    app = QtWidgets.QApplication(sys.argv)
    
    hh = hammerhead.Hammerhead()
    BIDI = GF1408_BIDI.GF1408_BIDI( hh )
    
    #mSetup = MeasurementSetup( GF1408config.singleton() )
    #print(mSetup)
    
    GF1408_GUI.GF1408_GUI(BIDI,hh)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()