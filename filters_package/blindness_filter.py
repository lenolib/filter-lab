# -*- coding: utf-8 -*-
from __future__ import division
from filter_base import Filter_base, Parameter, SUCCESS, FAIL 
import filter_base
import numpy
import time
import cv2

M = numpy.matrix([[17.8824, 43.5161, 4.11935],
                 [3.45565, 27.1554, 3.86714],
                 [0.0299566, 0.184309, 1.46709]])
P = numpy.matrix([[0, 2.022344, -2.52581],
                 [0, 1, 0],
                 [0, 0, 1]])
D = numpy.matrix([[1, 0, 0],
                 [0.494207, 0, 1.24827],
                 [0, 0, 1]])
MinvPM = numpy.asarray(M.I*P*M)
MinvDM = numpy.asarray(M.I*D*M)
 
class Blindness_filter(Filter_base):
    name = "Color blindness"
    def __init__(self):
        Filter_base.__init__(self)
        self.description = "Simulate different color blindnesses. "
        self.i_red = 'Red'
        self.i_green = 'Green'
        self.i_blue = 'Blue'
        self.o_red = 'Red'
        self.o_green = 'Green'
        self.o_blue = 'Blue'
        
        self.setupInputsOutputs([self.i_red,self.i_green,self.i_blue],
                                 [self.o_red,self.o_green,self.o_blue])
    
        self.addParam( Parameter(name="Type of blindness", param_type='list',
                                 default="Protanope",
                                 other_content=["None","Protanope", "Deuteranope"]))

    def process(self, input_images, connected_outs):
        if len(input_images) != 3:
            return FAIL
        blindness = self.getParamContent("Type of blindness")
        red_t,green_t,blue_t = self.transform(input_images[self.i_red],
                                         input_images[self.i_green],
                                         input_images[self.i_blue],
                                         blindness)
        return {self.o_red:red_t,
                self.o_green:green_t,
                self.o_blue:blue_t}    
        
    def transform(self, red, green, blue, blindness):
        """The procedure taken from 
        F. Viénot, H. Brettel, and J. Mollon. Digital video colourmaps for checking the
        legibility of displays by dichromats. Color Research and Application, 
        24:243-252, 1999"""
        if blindness == "None":
            return red,green,blue
        elif blindness == "Protanope":
            T = MinvPM            
            red = 0.992052*filter_base.pycv_power(red,2.2) + 0.003974
            green = 0.992052*filter_base.pycv_power(green,2.2) + 0.003974
            blue = 0.992052*filter_base.pycv_power(blue,2.2) + 0.003974
        elif blindness == "Deuteranope":
            T = MinvDM
            red = 0.957237*filter_base.pycv_power(red,2.2) + 0.0213814
            green = 0.957237*filter_base.pycv_power(green,2.2) + 0.0213814
            blue = 0.957237*filter_base.pycv_power(blue,2.2) + 0.0213814        
        else: 
            raise Exception("Unknown list parameter error")
        red_t = filter_base.pycv_power( T[0,0]*red + T[0,1]*green + T[0,2]*blue, 1/2.2 )
        green_t = filter_base.pycv_power( T[1,0]*red + T[1,1]*green + T[1,2]*blue, 1/2.2)
        blue_t = filter_base.pycv_power( T[2,0]*red + T[2,1]*green + T[2,2]*blue, 1/2.2)
        return red_t,green_t,blue_t
       
    def transform2(self, red, green, blue, blindness):
        """The procedure taken from 
        F. Viénot, H. Brettel, and J. Mollon. Digital video colourmaps for checking the
        legibility of displays by dichromats. Color Research and Application, 
        24:243-252, 1999"""
        if blindness == "None":
            return red,green,blue
        elif blindness == "Protanope":
            T = MinvPM            
            red = 0.992052*red**2.2 + 0.003974
            green = 0.992052*green**2.2 + 0.003974
            blue = 0.992052*blue**2.2 + 0.003974
        elif blindness == "Deuteranope":
            T = MinvDM
            red = 0.957237*red**2.2 + 0.0213814
            green = 0.957237*green**2.2 + 0.0213814
            blue = 0.957237*blue**2.2 + 0.0213814        
        else: 
            raise Exception("Unknown list parameter error")
        red_t = (T[0,0]*red + T[0,1]*green + T[0,2]*blue)**(1/2.2)
        green_t = (T[1,0]*red + T[1,1]*green + T[1,2]*blue)**(1/2.2)
        blue_t = (T[2,0]*red + T[2,1]*green + T[2,2]*blue)**(1/2.2)
        return red_t,green_t,blue_t
       
       
def getFilterList():
    """Return a list of connected filters in order to test the current filter."""
    import filters_package as imf
    loadf = imf.input_filter.Input_filter()
    current = Blindness_filter()    
    dispf = imf.display_filter.Display_filter()
    dispf.setName("Display - %s" %current.name)
    loadf.setName("Load - %s" %current.name)
    imf.filter_base.connect_filters(loadf,current,
                                   [loadf.output_names[1],loadf.output_names[2],loadf.output_names[3]],
                                   [current.input_names[0],current.input_names[1],current.input_names[2]])
    imf.filter_base.connect_filters(current, dispf, 
                                   [current.output_names[0],current.output_names[1],current.output_names[2]], 
                                   [dispf.input_names[1],dispf.input_names[2],dispf.input_names[3]])
    return [loadf,current,dispf]

if __name__ == "__main__":
    import os,sys
    flabfile = os.path.join(os.path.split(os.path.split(__file__)[0])[0],'filter_lab.py')
    os.system(sys.executable+" \""+flabfile+"\" \"%s\"" %__file__)