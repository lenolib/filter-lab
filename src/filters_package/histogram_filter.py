# -*- coding: utf-8 -*-
from __future__ import division
from filter_base import (Filter_base, Parameter, 
                         SUCCESS, FAIL, arr2pixmap,
                         plotfig2image, OUTPUT_FILTER)
import numpy
import matplotlib
import matplotlib.pyplot as plt
import cv2
import time


class Histogram_filter(Filter_base):
    name = "Histogram"
    def __init__(self):
        Filter_base.__init__(self)
        self.filtertype = OUTPUT_FILTER
        self.description = "Produce a histogram of the input image"
        self.addParam( Parameter(name="Display width (pixels)", param_type='variable',
                                 default=400, maximum=600, minimum=50) )
        self.addParam( Parameter(name="Display height (pixels)", param_type='variable',
                                 default=200, maximum=600, minimum=50) )
        self.addParam( Parameter(name="Plot histogram", param_type='list',
                                 default="Yes", other_content=["Yes","No"], rank=0))
        self.addParam( Parameter(name="# of bins", param_type='variable',
                                 default=255, maximum=255, minimum=2) )
        self.addParam( Parameter(name="Log", param_type='list', default='No',
                                 other_content=['Yes','No']) )
        self.addParam( Parameter(name="Normalize", param_type='list', default='Yes',
                                 other_content=['Yes','No']) )
        self.setupInputsOutputs(['Input'],['Histogram','Bins'])
        self.hist_fig = None
        self.hist_axis = None
        self.hist_curve = None
        self.last_width = None
        self.last_height = None
        self.pixmap = None

    def process(self, input_images, connected_outs):
        if 'Input' not in input_images:
            return FAIL
        if self.getParamContent("Log") == "Yes": do_log = True
        else: do_log = False
        if self.getParamContent("Normalize") == "Yes": normalize = True
        else: normalize = False
        if self.hist_fig is None:
            self.hist_fig = plt.figure(figsize=(4, 2), dpi=100)
            self.hist_axis = self.hist_fig.add_subplot(111)
            self.hist_axis.tick_params(labelsize=8)
            self.hist_axis.grid(True)        
        width = self.getParamContent('Display width (pixels)')
        height = self.getParamContent('Display height (pixels)')
        if width!=self.last_width:
            self.hist_fig.set_figwidth(width/100)
            self.last_width=width
        if height!=self.last_height:
            self.hist_fig.set_figheight(height/100)
            self.last_height=height
        src = input_images['Input']
        no_of_bins = int(self.getParamContent("# of bins"))
        
        if src.flags['C_CONTIGUOUS'] == False:
            src = numpy.ascontiguousarray(src, 'f')
        if src.dtype != 'f' and src.dtype != 'uint8':
            src = src.astype('f')
        mini = float(numpy.amin(src))
        maxi = float(numpy.amax(src))
        hist_vals = cv2.calcHist([src],[0],None,[no_of_bins],[mini,maxi])
        x_vals = numpy.arange(mini,maxi,(maxi-mini)/no_of_bins)
        if do_log: hist_vals = numpy.log(hist_vals)
        if normalize: hist_vals = hist_vals/numpy.amax(hist_vals)
        if self.getParamContent("Plot histogram") == "Yes":
            x2plt,hist2plt = histOutline(hist_vals,x_vals)
            self.abortQuery()
#            self.hist_axis.clear()
            if self.hist_curve is None:
                self.hist_curve = self.hist_axis.plot(x2plt,hist2plt,'k')[0]
            else:
                self.hist_curve.set_data(x2plt,hist2plt)
            self.hist_axis.set_xlim(x2plt.min(),x2plt.max())
            self.hist_axis.set_ylim(hist2plt.min(), hist2plt.max())
#            self.setParamContent("Histogram plot",self.hist_fig, emitSignal=True)
            self.abortQuery()
            self.pixmap = arr2pixmap(plotfig2image(self.hist_fig))
        return {'Histogram':hist_vals, 'Bins':numpy.hstack((x_vals,[maxi]))}
    
def histOutline(histIn,binsIn):
    stepSize = binsIn[1] - binsIn[0]
    bins = numpy.zeros(len(binsIn)*2 + 2, dtype=numpy.float)
    data = numpy.zeros(len(binsIn)*2 + 2, dtype=numpy.float)
    for bb in range(len(binsIn)):
        bins[2*bb + 1] = binsIn[bb]
        bins[2*bb + 2] = binsIn[bb] + stepSize
        if bb < len(histIn):
            data[2*bb + 1] = histIn[bb]
            data[2*bb + 2] = histIn[bb]
    bins[0] = bins[1]
    bins[-1] = bins[-2]
    data[0] = 0
    data[-1] = 0
    return (bins, data)

    
def getFilterList():
    """Return a list of connected filters in order to test the current filter."""
    import filters_package as imf
    loadf = imf.input_filter.Input_filter()
    current = Histogram_filter()
    loadf.setName("Load - %s" %current.name)
    imf.filter_base.connect_filters(loadf,current,[loadf.output_names[1]],
                                                  [current.input_names[0]])
    return [loadf,current]

if __name__ == "__main__":
    import os,sys
    flabfile = os.path.join(os.path.split(os.path.split(__file__)[0])[0],'filter_lab.py')
    os.system(sys.executable+" \""+flabfile+"\" \"%s\"" %__file__)
    