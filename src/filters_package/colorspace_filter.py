# -*- coding: utf-8 -*-
from __future__ import division
from filter_base import Filter_base, Parameter, SUCCESS, FAIL 
import filter_base
import numpy
import time
import pyopencv as pycv

choices = {'RGB->HLS':pycv.CV_RGB2HLS,
           'RGB->HSV':pycv.CV_RGB2HSV,
           'RGB->XYZ':pycv.CV_RGB2XYZ,
           'RGB->YCrCv':pycv.CV_RGB2YCrCb,
           'RGB->Lab':pycv.CV_RGB2Lab,
           'RGB->Luv':pycv.CV_RGB2Luv,
           'HLS->RGB':pycv.CV_HLS2RGB,
           'HSV->RGB':pycv.CV_HSV2RGB,
           'YCrCv->RGB':pycv.CV_YCrCb2RGB,
           'Lab->RGB':pycv.CV_Lab2RGB,
           'Luv->RGB':pycv.CV_Luv2RGB}

class Colorspace_filter(Filter_base):
    name = "Colorspace transforms"
    def __init__(self):
        Filter_base.__init__(self)
        self.description = "Convert the input image to a new colorspace"
        self.setupInputsOutputs(['Input 1','Input 2','Input 3'],
                                 ['Output 1', 'Output 2', 'Output 3', "3ch output"])        
        self.addParam( Parameter(name='Transformation', param_type='list', default='RGB->HLS',
                                 other_content=choices.keys() ))
        
    def process(self, input_images, connected_outs):
        choice = self.getParamContent('Transformation')
        if len(input_images) != 3: return FAIL
        if choice in choices.keys():
            conversion_type = choices[choice]
        else: raise Exception("Unknown list parameter error")
        src = numpy.dstack((input_images['Input 1'], 
                            input_images['Input 2'],
                            input_images['Input 3']) )
        if src.flags['C_CONTIGUOUS'] == False:
            src = numpy.ascontiguousarray(src)
        dst = numpy.empty_like(src)
        pycv.cvtColor(pycv.asMat(src), 
                      pycv.asMat(dst), 
                      conversion_type)    
        return {'Output 1':dst[:,:,0], 
                'Output 2':dst[:,:,1], 
                'Output 3':dst[:,:,2],
                '3ch output':dst}    
        
        
def getFilterList():
    """Return a list of connected filters in order to test the current filter."""
    import filters_package as imf
    loadf = imf.input_filter.Input_filter()
    current = Colorspace_filter()    
    dispf = imf.display_filter.Display_filter()
    dispf.setName("Display - %s" %current.name)
    loadf.setName("Load - %s" %current.name)
    imf.filter_base.connect_filters(loadf,current,
                                   [loadf.output_names[1],loadf.output_names[2],loadf.output_names[3]],
                                   [current.input_names[0],current.input_names[1],current.input_names[2]])
    imf.filter_base.connect_filters(current, dispf, [current.output_names[0]], [dispf.input_names[0]])
    return [loadf,current,dispf]

if __name__ == "__main__":
    import os,sys
    flabfile = os.path.join(os.path.split(os.path.split(__file__)[0])[0],'filter_lab.py')
    os.system(sys.executable+" \""+flabfile+"\" \"%s\"" %__file__)