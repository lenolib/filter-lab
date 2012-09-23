# -*- coding: utf-8 -*-
from filter_base import Filter_base, Parameter, SUCCESS, FAIL
import filter_base
import numpy
import time

class Remap_range_filter(Filter_base):
    name = "Remap pixel range"
    def __init__(self):
        Filter_base.__init__(self)        
        self.setupInputsOutputs(["Input"], ["Output"])
        self.description = "Linearly remap the input image's pixel value range to a new range."
        self.addParam( Parameter(description="Put exactly equal to 'End of old range' \
to automatically set this value to the lowest pixel value in the current image \
(this span may change between images)",
                                 name="Start of old range", param_type="variable", 
                                 default=0, minimum=-4,maximum=4, rank=1) )
        self.addParam( Parameter(description="Put exactly equal to 'Start of old range' \
to automatically set this value to the highest pixel value in the current image \
(this span may change between images)",
                                 name="End of old range", param_type="variable", 
                                 default=0, minimum=-4,maximum=4, rank=2) )
        self.addParam( Parameter(name="Start of new range", param_type="variable", 
                                 default=0, minimum=-4,maximum=4, rank=3) )
        self.addParam( Parameter(name="End of new range", param_type="variable", 
                                 default=1, minimum=-4,maximum=4, rank=4) )
        
    def process(self, input_images, connected_outs):
        if len(input_images) == 0:
            return FAIL
        old_min = self.getParamContent("Start of old range")
        old_max = self.getParamContent("End of old range")
        min = self.getParamContent("Start of new range")
        max = self.getParamContent("End of new range")
        if max<=min:
            max = min + 0.001
            self.setParamContent('End of new range', max, emitSignal=True)
        
        remapped_im = filter_base.remap(input_images[self.input_names[0]], 
                                       min=min, max=max, curr_min=old_min, curr_max=old_max) #Takes care of the case old_min==old_max
        return {self.output_names[0]:remapped_im}
    
    
    
def getFilterList():
    """Return a list of connected filters in order to test the current filter."""
    import filters_package as imf
    loadf = imf.input_filter.Input_filter()
    current = Remap_range_filter()    
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