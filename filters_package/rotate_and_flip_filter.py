# -*- coding: utf-8 -*-
from filter_base import Filter_base, Parameter, SUCCESS, FAIL
import numpy
import time

class Rotate_and_flip_filter(Filter_base):
    name = "Rotate and flip"
    def __init__(self):
        Filter_base.__init__(self)       
        self.description = "Rotate the input image by 90-degrees increments or flip it." 
        self.setupInputsOutputs(["Input"], ["Output"])
        self.addParam( Parameter(name="Rotate:", param_type="list", 
                                 default="Rotate upside-down", 
                                 other_content=["No", "Rotate left","Rotate right","Rotate upside-down"]) )
        self.addParam( Parameter(name="Flip:", param_type="list", 
                                 default="No", 
                                 other_content=["No","Vertically","Horizontally"]) )
        
    def process(self, input_images, connected_outs):
        if len(input_images) == 0:
            return FAIL
        rotate = self.getParamContent("Rotate:")
        flip = self.getParamContent("Flip:")
        image = input_images[self.input_names[0]]
        if rotate == "No":
            pass
        elif rotate == "Rotate left":
            image = numpy.rot90(image,1)
        elif rotate == "Rotate right":
            image = numpy.rot90(image,3)
        elif rotate == "Rotate upside-down":
            image = numpy.rot90(image,2)
        if flip == "No":
            pass
        elif flip == "Vertically":
            image = numpy.flipud(image)
        elif flip == "Horizontally":
            image = numpy.fliplr(image)
        return {self.output_names[0] : image}


def getFilterList():
    """Return a list of connected filters in order to test the current filter."""
    import filters_package as imf
    loadf = imf.input_filter.Input_filter()
    current = Rotate_and_flip_filter()    
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