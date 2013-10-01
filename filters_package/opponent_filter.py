# -*- coding: utf-8 -*-
from __future__ import division
from filter_base import Filter_base, Parameter, SUCCESS, FAIL
import cython_functions
import numpy
import time

class Opponent_filter(Filter_base):
    """This filter will calculate opponent color images from an RGB image."""
    name = 'Opponent colors'
    def __init__(self):
        Filter_base.__init__(self)
        self.description = "\
Convert the channels in the input RGB-image to \
opponent colors channels by simple pixel arithmetic.\
Note that all inputs have to be connected for the filter to work."
        self.setupInputsOutputs(['Red','Green','Blue'], 
                                 ['Red-Green','Blue-Yellow','Brightness'])
        
    def process(self, input_images, connected_outs):
        """Make sure there is an image at all inputs, and then create and return the result images."""
        #Could be made more efficient if needed by only calculating the necessary images.
        if len(input_images) != 3:
            return FAIL
        opponents = self.create_opponent_images(input_images[self.input_names[0]],
                                            input_images[self.input_names[1]],
                                            input_images[self.input_names[2]])  
        processed_images = {self.output_names[0]:opponents[0],
                            self.output_names[1]:opponents[1],
                            self.output_names[2]:opponents[2]}
        return processed_images
        
    def create_opponent_images(self, red, green, blue, mode='cython'):
        """Create and return opponent images by either the fast 'cython' method or with pure
        python code (numpy matrix algebra, which is slower) by using the mode='python', 
        and return the images as a list."""
        if mode == 'cython':
            if red.dtype != 'float32': 
                red = red.astype('f')
            if green.dtype != 'float32': 
                green = green.astype('f')
            if blue.dtype != 'float32': 
                blue = blue.astype('f')
            RGim = numpy.empty_like(red)
            BYim = numpy.empty_like(red)
            brightim = numpy.empty_like(red)
            cython_functions.cyth_create_opponent_images(red, green, blue, RGim, BYim, brightim)
            result = [RGim,BYim,brightim]               
        else:
            result = self.pyth_create_opponent_images(red,green,blue)     
        return result  
    
    def pyth_create_opponent_images(self, red, green, blue):
        """Create opponent images with numpy matrix algebra and return the result as a list."""
        RGim = 0.5 - red/2 + green/2
        BYim = 0.5 - (red+green)/4 + blue/2
        brightim = (red+green)/2
        return [RGim,BYim, brightim]
    
    
def getFilterList():
    """Return a list of connected filters in order to test the current filter."""
    import filters_package as imf
    loadf = imf.input_filter.Input_filter()
    current = Opponent_filter()    
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