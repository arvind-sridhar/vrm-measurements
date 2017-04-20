from __future__ import division
from PyQt4.QtGui import *

# from PyQt4.QtCore import *
import numpy as np
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
# import matplotlib.pyplot as plt
from matplotlib.figure import Figure

def f3(x):
    return '{:.3f}'.format(x)
def f2(x):
    return '{:.2f}'.format(x)
def f1(x):
    return '{:.1f}'.format(x)
def f0(x):
    return '{:.0f}'.format(x)

class MplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        
        self.CHANNELS = 8
        self.plotLen = 1e6
        self.plotOffset = 0
        
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)
        self.data = [[1, 10]]
        self.t = [[0, 10]]
        self.dEnable = [True]

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        
    def setData(self, t, data):
        self.t = t
        self.data = data
        
        # if dEnable is not set or set to wrong length, set to all true
        if len(self.dEnable) != len(self.data):
            self.dEnable = list()
            for i in range(len(self.data)):
                self.dEnable.append(True)
        self.updateFigure()

#    def setEnable(self, index, state):
#        # Length of dEnable has to match number of rows in data
#        self.dEnable[index] = state
#        self.updateFigure()
#    
#    def setPlotLen(self, val):
#        if (val<0):
#            val = 0
#        self.plotLen = val
#        self.updateFigure()
#        
#    def setPlotOffset(self, val):
#        if (val<0):
#            val = 0
#        self.plotOffset = val
#        self.updateFigure()
        
    def setYAxis(self, Min, Max, Ticks, label, decimal):
        self.axes.hold(False)
        self.axes.grid(True)
        self.axes.set_ylabel(label)
        self.axes.set_ylim(Min, Max)
        self.axes.set_yticks([round(x, decimal) for x in np.linspace(Min, Max, Ticks + 1)])
        self.axes.hold(True)
        
    def setXAxis(self, Min, Max, Ticks, label, decimal):
        self.axes.hold(False)
        self.axes.grid(True)
        self.axes.set_xlabel(label)
        self.axes.set_xlim(Min, Max)
#        self.axes.set_xticks([round(x, 0) for x in list(linspace(Min, Max, Ticks))])
        self.axes.set_xticks([round(x, decimal) for x in np.linspace(Min, Max, Ticks)])        
        self.axes.hold(True)

        
    def clearFig(self):
        self.axes.hold(False)
        self.axes.plot([], [], 'w')
        self.draw() 
        self.axes.hold(True)

    def updateFigure(self):
        colors = ['r', 'b', 'g', 'c', 'm', 'y', '#0055ff', '#00ff55', 'k', 'r', 'b', 'g', 'c', 'm', 'y', '#0055ff', '#ff0055', 'k']


        # Clear Plots
#        self.axes.hold(False)
#        self.axes.plot([], [], 'w')
#        self.axes.hold(True)
#        print self.t
        self.axes.plot(self.t, self.data, colors[1])        
        
        self.draw()        
#        for i in range(len(self.data)):
#            if self.dEnable[i]:
#                axisLbl = "Ch "+str(i)
                
#                pLen = self.plotLen
#                pOffset = self.plotOffset
#                # If last channel (which is 8x longer than all others because it is combined
#                if i == len(self.data)-1:
#                    axisLbl = "Comb Ch"
#                else:
#                    pLen = int(pLen / self.CHANNELS)
#                    pOffset = int(pOffset / self.CHANNELS)
#                dLen = len(self.data[i])
#                if dLen-1 < pOffset:
#                    pOffset = dLen
#                if dLen < pOffset+pLen:
#                    pLen = dLen-pOffset
#                
#                self.axes.plot(self.t[i][pOffset:pOffset+pLen], self.data[i][pOffset:pOffset+pLen], colors[i], label=axisLbl)

#        self.axes.set_ylim(0, 2**self.CHANNELS-1)
#        self.axes.set_yticks([x for x in range(0, 256, 16)])
#        print self.t, self.data
#        self.axes.legend()
        
        # handles, labels = self.get_legend_handles_labels()

        # reverse the order
        # self.legend(handles[::-1], labels[::-1])
        

        
        

# def linspace(start, stop, n):
#    if n == 1:
#        yield stop
#        return
#    h = (stop - start) / (n - 1)
#    for i in range(n):
#        yield start + h * i        
