# -*- coding: utf-8 -*-
from filter_base import Filter_base, Parameter, SUCCESS, FAIL
import cython_functions
import numpy

class Adaptation_filter(Filter_base):
    name = "Adaptation"
    def __init__(self):
        Filter_base.__init__(self)    
        self.i_input = "Input"
        self.o_output = "Output"    
        self.setupInputsOutputs([self.i_input], [self.o_output])
        self.addParam( Parameter(name="Sensitivity reduction", param_type="variable",
                                  default=1,minimum=0,maximum=1, rank=1.0) )

    def process(self, input_images, connected_outs):
        if len(input_images) == 0:
            return FAIL
        Sens_Reduction = self.getParamContent("Sensitivity reduction")
        if Sens_Reduction<=0:
            Sens_Reduction = 0
#        print "Sens_Reduction:", Sens_Reduction
        out_im = Sens_Reduction * input_images["Input"]
        return {self.output_names[0]:out_im}

    


def getFilterList():
    """Return a list of connected filters in order to test the current filter. Boilerplate."""
    import filters_package as fpk
    loadf = fpk.input_filter.Input_filter()
    current = Adaptation_filter()
    dispf = fpk.display_filter.Display_filter()
    dispf.setName("Display - %s" %current.name)
    loadf.setName("Load - %s" %current.name)
    fpk.filter_base.connect_filters(loadf,current,[loadf.output_names[1]],[current.input_names[0]])
    fpk.filter_base.connect_filters(current, dispf, [current.output_names[0]], [dispf.input_names[0]])
    return [loadf,current,dispf]

if __name__ == "__main__":    
    import os,sys
    flabfile = os.path.join(os.path.split(os.path.split(__file__)[0])[0],'filter_lab.py')
    command = sys.executable+" \""+flabfile+"\" \"%s\"" %__file__
    os.system(command)

