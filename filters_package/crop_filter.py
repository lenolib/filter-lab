# -*- coding: utf-8 -*-
from filter_base import Filter_base, Parameter, SUCCESS, FAIL
import numpy
import time

class Crop_filter(Filter_base):
    name = "Crop"
    def __init__(self):
        Filter_base.__init__(self) 
        self.description = "Crop the image dimensions."       
        self.setupInputsOutputs(["Input"], ["Output"])
        self.addParam( Parameter(name="Center x-position", param_type="variable", 
                                 default=0, minimum=0,maximum=2048, rank=0) )
        self.addParam( Parameter(name="Center y-position", param_type="variable", 
                                 default=0, minimum=0,maximum=2048, rank=1) )
        self.addParam( Parameter(name="Width", param_type="variable", 
                                 default=320, minimum=0,maximum=2048, rank=2) )
        self.addParam( Parameter(name="Height", param_type="variable", 
                                 default=240, minimum=0,maximum=2048, rank=3) )
        
    def process(self, input_images, connected_outs):
        if len(input_images) == 0: return FAIL
        image = input_images["Input"]
        im_w = image.shape[1]
        im_h = image.shape[0]
                
        x_pos = int(self.getParamContent("Center x-position"))
        y_pos = int(self.getParamContent("Center y-position"))
        crop_w = int(self.getParamContent("Width"))
        crop_h = int(self.getParamContent("Height"))
        if crop_w == 0: crop_w = 1
        if crop_h == 0: crop_h = 1
        top = int( y_pos-crop_h/2 )
        bottom = int( y_pos+crop_h/2 )
        left = int( x_pos-crop_w/2 ) 
        right = int( x_pos+crop_w/2 )
        
        if top < 0:
            top = 0
        if bottom > im_h:
            bottom = im_h
        if bottom == 0:
            bottom = 1
        if left < 0:
            left = 0
        if right > im_w:
            right = im_w
        if right == 0:
            right = 1
        if top >= bottom:
            top = bottom -1
        if left >= right:
            left = right -1
        
        try:
            cropped_im = image[top:bottom,left:right]
        except IndexError:
            raise Exception("Could not crop image. Please adjust the parameters.")
        return {"Output":cropped_im}
    
    
def getFilterList():
    """Return a list of connected filters in order to test the current filter."""
    import filters_package as imf
    loadf = imf.input_filter.Input_filter()
    current = Crop_filter()    
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