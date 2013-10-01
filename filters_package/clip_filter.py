# -*- coding: utf-8 -*-
from filter_base import Filter_base, Parameter, SUCCESS, FAIL
import numpy
import time

class Clip_filter(Filter_base):
    name = "Clip"
    def __init__(self):
        Filter_base.__init__(self)        
        self.description = "Clip the pixel values of an image to a specified range."
        self.setupInputsOutputs(["Input"], ["Output"])
        self.addParam( Parameter(name="Maximum threshhold", param_type="variable", 
                                 default=1, minimum=-4,maximum=4, rank=0) )
        self.addParam( Parameter(name="Minimum threshhold", param_type="variable", 
                                 default=0, minimum=-4,maximum=4, rank=1) )

        
    def process(self, input_images, connected_outs):
        if len(input_images) == 0:
            return FAIL
        min = self.getParamContent("Minimum threshhold")
        max = self.getParamContent("Maximum threshhold")
        if max<=min:
            max = min + 0.001
        clipped_im = input_images["Input"].clip(min=min,max=max)
        return {"Output":clipped_im}


def getFilterList():
    """Return a list of connected filters in order to test the current filter."""
    import filters_package as imf
    loadf = imf.input_filter.Input_filter()
    current = Clip_filter()    
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