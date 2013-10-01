# -*- coding:utf-8 -*-

from filter_base import Filter_base, Parameter, SUCCESS, FAIL
import numpy
import cv2

class Smooth_filter(Filter_base):
    name = 'Smooth'
    def __init__(self):
        Filter_base.__init__(self)
        self.setupInputsOutputs(['Input'], 
                                 ['Output'])
        self.description = "Smooth the image. \nTo disable all smoothing, set all sliders to zero."
        self.addParam( Parameter(name='Smoothing method', param_type='list', default='Gaussian', 
                                 other_content=['Gaussian','Box blur', 'Median - input must be 8-bit'], rank=0) )
        self.addParam( Parameter(name='Smoothing kernel width', param_type='variable',
                                 description="Will be rounded to an odd number or zero.",
                                 default=3, minimum=0, maximum=15, rank=1) )
        self.addParam( Parameter(name="Smoothing kernel height", param_type='variable',
                                 description="Is set to equal the kernel width if zero.",
                                 default=0, minimum=0, maximum=15, rank=2) )
        self.addParam( Parameter(name='Gaussian standard deviation', param_type='variable',
                                 description="Will be calculated automatically if zero.\
                                 If not zero while the kernel size is, \
                                 a suitable kernel size will be calculated.",
                                 default=0, minimum=0, maximum=15, rank=3) )

    def process(self, input_images, connected_outs):
        if len(input_images) == 0:
            return FAIL     
        src = input_images['Input']   
        choice = str( self.getParamContent('Smoothing method') )
        p1_width = int( round( self.getParamContent('Smoothing kernel width') ) )
        p3_std = self.getParamContent('Gaussian standard deviation')
        p2_height = int( round( self.getParamContent('Smoothing kernel height') ) )
        if p1_width < 0:
            p1_width = 0
        elif p1_width%2 != 1:
            p1_width += 1        
        if p2_height <= 0:
            p2_height = 0
        elif p2_height%2 != 1:
            p2_height += 1            
        if p3_std <= 0:
            p3_std = 0   
        if (p1_width,p2_height,p3_std) == (0,0,0): 
            p1_width = 1
                
        if choice == 'Gaussian':
            method = cv2.cv.CV_GAUSSIAN     
        elif choice == 'Box blur':
            method = cv2.cv.CV_BLUR
        elif choice == 'Median - input must be 8-bit':
            method = cv2.cv.CV_MEDIAN
            if p1_width == 0:
                p1_width = 1
        if (p1_width,p2_height,p3_std) == (0,0,0): 
            return {'Output' : src}

        if src.flags['C_CONTIGUOUS'] == False:
            src = numpy.ascontiguousarray(src)
        smoothed = numpy.empty_like(src)
        cv2.cv.Smooth(cv2.cv.fromarray(src), cv2.cv.fromarray(smoothed),
                      method, p1_width, p2_height, p3_std)
        return {'Output' : smoothed}
    
def getFilterList():
    """Return a list of connected filters in order to test the current filter."""
    import filters_package as imf
    loadf = imf.input_filter.Input_filter()
    current = Smooth_filter()    
    dispf = imf.display_filter.Display_filter()
    dispf.setName("Display - %s" %current.name)
    loadf.setName("Load - %s" %current.name)
    imf.filter_base.connect_filters(loadf,current,[loadf.output_names[0]],[current.input_names[0]])
    imf.filter_base.connect_filters(current, dispf, [current.output_names[0]], [dispf.input_names[0]])
    return [loadf,current,dispf]
    
    
if __name__ == "__main__":
    import os,sys
    flabfile = os.path.join(os.path.split(os.path.split(__file__)[0])[0],'filter_lab.py')
    os.system("""%s "%s" "%s" """ %(sys.executable, flabfile, __file__))