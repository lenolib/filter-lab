# -*- coding:utf-8 -*-

from filter_base import Filter_base, Parameter, SUCCESS, FAIL

class Time_lag_filter(Filter_base):
    name = "Time lag"
    def __init__(self):
        Filter_base.__init__(self)        
        self.setupInputsOutputs(["Input"], ["Output"])
        self.description = "\
Will act as a time lag and output the n'th frame before \
the current one. n=0: Current frame, n=1: Previous frame\
"
        self.addParam( Parameter(name="Input interval (frames)", param_type="text", rank=0, default="1") )
        self.past_frames = []

    def process(self, input_images, connected_outs):        
        if len(input_images) == 0:
            return FAIL
        interval = self.getParamContent("Input interval (frames)")        
        try:
            interval = int(interval)
        except ValueError,e:
            print "In '%s': ValueError: %s \n Input was: %s" %(self.name,e,interval)
            return FAIL        
        if interval < 0:
            raise Exception("In '%s': Time lag frame interval must not be negative" %self.name)
        if interval == 0:
            if len(self.past_frames) != 0:
                self.past_frames = []
            return {self.output_names[0]: input_images[self.input_names[0]]}
        elif len(self.past_frames) < interval:
            self.past_frames.append(input_images[self.input_names[0]])
            return FAIL
        elif len(self.past_frames) != 0:
            self.past_frames.append(input_images[self.input_names[0]])
            if len(self.past_frames) > interval+1:
                self.past_frames = self.past_frames[:interval+1]
            return {self.output_names[0]: self.past_frames.pop(0)}
        else:
            print "In '%s': Shouldn't get here in the code. Needs to be investigated." %self.name
            return {}
        
def getFilterList():
    """Return a list of connected filters in order to test the current filter."""
    import filters_package as imf
    loadf = imf.input_filter.Input_filter()
    current = Time_lag_filter()
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