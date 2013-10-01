# -*- coding: utf-8 -*-
from __future__ import division
from filter_base import Filter_base, Parameter, SUCCESS, FAIL 
import filter_base
import numpy
import time

class Blend_filter(Filter_base):
    name = "Blend together"
    def __init__(self):
        Filter_base.__init__(self)
        self.description = "Blend several pictures together by simple weighting."
        self.i_input1 = 'Input 1'
        self.i_input2 = 'Input 2'
        self.i_input3 = 'Input 3'
        self.i_input4 = 'Input 4'
        self.o_output = 'Output'
        self.setupInputsOutputs([self.i_input1,self.i_input2,self.i_input3,self.i_input4],
                                 [self.o_output])
        for ind,input_name in enumerate(self.input_names):
            self.addParam( Parameter(name=input_name+' weight',param_type='variable',
                                     default=1,minimum=0,maximum=5, rank=ind))
#        self.addParam( Parameter(name='Output pixel data type'),type='list',
#                                 content='Same as input', other_content=['8-bit integer', '32-bit float'])
        
    def process(self, input_images, connected_outs):
        if len(input_images) == 0:
            return FAIL
        all_weights = [self.getParamContent(input_name+' weight') for input_name in self.input_names]
        imgs = []
        weights = []   
        all_inputs_8bit = True     
        for i,input_name in enumerate(self.input_names):
            if input_name in input_images.keys():
                imgs.append(input_images[input_name])
                if input_images[input_name].dtype != 'uint8': all_inputs_8bit = False
                weights.append(all_weights[i])
        
        summation_img = numpy.zeros_like(imgs[0], dtype='f')        
        for i,img in enumerate(imgs):
            summation_img = summation_img+img*weights[i]        
        if all_inputs_8bit:     
            out_im = filter_base.make_uint8(summation_img)
        else: 
            out_im = filter_base.make_normfloat32(summation_img)                              
        return {self.o_output:out_im}    
           

def getFilterList():
    """Return a list of connected filters in order to test the current filter."""
    import filters_package as imf
    loadf = imf.input_filter.Input_filter()
    current = Blend_filter()    
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
