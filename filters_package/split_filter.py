# -*- coding: utf-8 -*-
from filter_base import Filter_base, Parameter, SUCCESS, FAIL
import numpy
import time

def makeCross(side=30):
    cross = numpy.ones((side,side),dtype='float32')*255
    for i in xrange(side):          
        cross[i,i] = 0
        cross[side-i-1,i] = 0
    return cross
cross = makeCross()

class Split_filter(Filter_base):
    name = "Split image"
    def __init__(self):
        Filter_base.__init__(self)      
        self.description = "Split the input image into four new images."  
        self.setupInputsOutputs(["Input"], 
                                 ["Upper left","Upper right","Lower left","Lower right"])
        self.addParam( Parameter(name="Split horizontally at:", param_type="variable", 
                                 default=0, minimum=0,maximum=2048) )
        self.addParam( Parameter(name="Split vertically at:", param_type="variable", 
                                 default=0, minimum=0,maximum=2048) )

    def process(self, input_images, connected_outs):
        processed_images = {}

        if len(input_images) == 0:
            return FAIL
        image = input_images["Input"]
        im_w = image.shape[0]
        im_h = image.shape[1]
                
        y = int(self.getParamContent("Split vertically at:"))
        x = int(self.getParamContent("Split horizontally at:"))
        if x < 0:       x = 0
        if x >= im_w:   x = im_w
        if y < 0:       y = 0
        if y >= im_h:   y = im_h
        upleft,upright,lowleft,lowright = (1,1,1,1)
        if x == 0:
            upleft = None
            lowleft = None
        if x == im_w:
            upright = None
            lowright = None
        if y == 0:
            upleft = None
            upright = None
        if y == im_h:
            lowleft = None
            lowright = None
        if upleft is not None:   upleft = image[:x,:y]
        if upright is not None:  upright = image[:x,y:]
        if lowleft is not None:  lowleft = image[x:,:y]
        if lowright is not None: lowright = image[x:,y:]
        
        parts = [upleft,upright,lowleft,lowright]
        for i,im_part in enumerate(parts):
            if parts[i] is not None and 0 not in parts[i].shape:
                processed_images[self.output_names[i]] = parts[i]
            else:
                processed_images[self.output_names[i]] = cross
        return processed_images
    
def getFilterList():
    """Return a list of connected filters in order to test the current filter."""
    import filters_package as imf
    loadf = imf.input_filter.Input_filter()
    current = Split_filter()    
    dispf = imf.display_filter.Display_filter()
    dispf.setName("Display - %s" %current.name)
    loadf.setName("Load - %s" %current.name)
    imf.filter_base.connect_filters(loadf,current,[loadf.output_names[0]],[current.input_names[0]])
    imf.filter_base.connect_filters(current, dispf, [current.output_names[0]], [dispf.input_names[0]])
    return [loadf,current,dispf]

if __name__ == "__main__":
    import os,sys
    flabfile = os.path.join(os.path.split(os.path.split(__file__)[0])[0],'filter_lab.py')
    os.system(sys.executable+" \""+flabfile+"\" \"%s\"" %__file__)