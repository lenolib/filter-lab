# -*- coding: utf-8 -*-
from filter_base import Filter_base, Parameter, SUCCESS, FAIL
import numpy
import cv2

class Canny_filter(Filter_base):
    name = 'Edge detection (Canny)'
    def __init__(self):
        Filter_base.__init__(self)        
        self.setupInputsOutputs(['Input'], 
                                 ['Output'])
        self.description = "Use the Canny algorithm to detect edges. Input must be 8-bit."
        self.addParam( Parameter(name="First threshold", param_type='variable',
                                 default=50, minimum=0, maximum=600, rank=1) )
        self.addParam( Parameter(name="Second threshold", param_type='variable',
                                 default=150, minimum=0, maximum=600, rank=2) )
        self.addParam( Parameter(name="Aperture size", param_type='list',
                                 description="Aperture of the sobel operator.",
                                 default="3", other_content=["1","3","5","7"], rank=3) )

    def process(self, input_images, connected_outs):
        if len(input_images) == 0:
            return FAIL             
        src = input_images['Input']
        if src.dtype != 'uint8':
            print "In '%s': Only works on 8-bit images. Received data type was '%s'" %(self.name,src.dtype)
            return FAIL   
        aperture_size = int( self.getParamContent('Aperture size') )
        th1 = int( self.getParamContent('First threshold') )
        th2 = int( self.getParamContent('Second threshold') )
        
        if src.ndim > 2:
            print "In '%s': The canny edge detector only works on single channel images." %self.name
            return FAIL
        if src.flags['C_CONTIGUOUS'] == False:
            src = numpy.ascontiguousarray(src)
        edges = cv2.Canny(src, th1, th2, apertureSize=aperture_size)
        return {'Output' : edges}
    


def getFilterList():
    """Return a list of connected filters in order to test the current filter."""
    import filters_package as imf
    loadf = imf.input_filter.Input_filter()
    loadf.setParamContent("Output type", "original")
    current = Canny_filter()    
    dispf = imf.display_filter.Display_filter()
    dispf.setName("Display - %s" %current.name)
    loadf.setName("Load - %s" %current.name)
    imf.filter_base.connect_filters(loadf,current,[loadf.output_names[1]],[current.input_names[0]])
    imf.filter_base.connect_filters(current, dispf, [current.output_names[0]], [dispf.input_names[0]])
    return [loadf,current,dispf]    
    
if __name__ == "__main__":
    import os,sys
    flabfile = os.path.join(os.path.split(os.path.split(__file__)[0])[0],'filter_lab.py')
    os.system(sys.executable+" \""+flabfile+"\" \"%s\"" %__file__)
    