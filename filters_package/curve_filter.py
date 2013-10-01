# -*- coding: utf-8 -*-
import filter_base
from filter_base import Filter_base, Parameter, SUCCESS, FAIL
import numpy
import numpy as np
import math
import matplotlib as mpl

class Curve_filter(Filter_base):
    name = "Curve"
    def __init__(self):
        Filter_base.__init__(self)        
        self.description = "\
Apply an intensity transformation curve to the input image, \
by mapping old curve values to new ones via a \
look-up table created by linear interpolation.\
"
        self.setupInputsOutputs(["Input"], ["Output"])
        self.addParam( Parameter(name="Curve plot", param_type="display", rank=0))
        self.addParam( Parameter(name="Function/points input", param_type="codebox", rank=1, 
                                 default=("""\
k = (t-s)/(d-c)
m = -k*c+s
intervals = [
    [(vmin,c),  s ],
    [(c,d),     k*x+m ],
    [(d,vmax),  t ] ]\n""") ) )
        self.addParam( Parameter(name="c variable", param_type="variable", 
                                 default=0.25, minimum=0,maximum=1, rank=1) )
        self.addParam( Parameter(name="d variable", param_type="variable", 
                                 default=0.75, minimum=0,maximum=1, rank=2) )
        self.addParam( Parameter(name="s variable", param_type="variable", 
                                 default=0.1, minimum=0,maximum=1, rank=3) )
        self.addParam( Parameter(name="t variable", param_type="variable", 
                                 default=0.9, minimum=0,maximum=1, rank=4) )
        self.addParam( Parameter(name="Interpolation resolution", param_type="variable", 
                                 default=256, minimum=4,maximum=1024, rank=6,
                                 description="Number of data points from which to interpolate.") )
        self.addParam( Parameter(name="Min pixel value", param_type="variable", 
                                 default=0, minimum=0,maximum=1, rank=7,
                                 description="Start applying curve at this pixel value (vmin).") )
        self.addParam( Parameter(name="Max pixel value", param_type="variable", 
                                 default=1, minimum=0,maximum=1, rank=8,
                                 description="Stop applying curve at this pixel value (vmax).") )

        self.curve_fig = None
        self.curve_graph = None
        self.curve = None
        self.expression = None
        self.last_max = None
        self.last_min = None
        self.last_res = None
        self.last_indexes = None
        self.last_cvar = None
        self.last_tvar = None
        self.last_svar = None
        self.last_dvar = None
        try: self.processParams() #Create a curve graph from the moment of creation.
        except Exception: 
            pass
        
    def processParams(self):
        res = int(self.getParamContent("Interpolation resolution"))       
        cvar = self.getParamContent("c variable")
        dvar = self.getParamContent("d variable") 
        svar = self.getParamContent("s variable")  
        tvar = self.getParamContent("t variable")               
        vmin = self.getParamContent("Min pixel value")
        vmax = self.getParamContent("Max pixel value") 
        if vmax <= vmin or vmin >= vmax:
            print "In '%s': Wrong size relationship between vmin-vmax, setting vmax = vmin+0.1." %self.name
            vmax = vmin + 0.1       
            self.setParamContent("Max pixel value", vmax, emitSignal=True)
        new_exp = self.getParamContent("Function/points input")     
        if ([new_exp, res, vmin, vmax, 
             cvar, tvar, dvar, svar] == [self.expression, self.last_res, 
                                         self.last_min, self.last_max, 
                                         self.last_cvar, self.last_tvar, 
                                         self.last_dvar, self.last_svar]):
            return
        try:
            if res < 4:
                print "Resolution is too small, resetting to 4"        
                self.setParamContent("Interpolation resolution",4,emitSignal=True)
                res = 4
            x = numpy.linspace(vmin, vmax, res)
            c = cvar
            t = tvar
            s = svar
            d = dvar
            intervals = None
            exec(new_exp)
            if not isinstance(intervals,list): raise Exception("Intervals must be a list of lists with items of format [(start,end), expression]")
            curve_vals = numpy.zeros((res))
            unovec = numpy.ones((res))
            for (start,end), vals in intervals:
                startind = int(math.floor( (start-vmin)/(vmax-vmin)*res ))
                endind = int(math.ceil( (end-vmin)/(vmax-vmin)*res ))
                if isinstance(vals,numpy.ndarray) and len(vals)>1:
                    vals_slice = vals[startind:endind]*unovec[startind:endind]
                else:
                    vals_slice = float(vals)*unovec[startind:endind]
                curve_vals[startind:endind] = vals_slice
        except Exception,e:
            print "In '%s': Could create curve. Reason: " %self.name, e
            raise e
        self.expression = new_exp
        self.last_res = res
        self.last_max = vmax
        self.last_min = vmin
        self.last_cvar = cvar
        self.last_tvar = tvar
        self.last_svar = svar
        self.last_dvar = dvar
        self.last_indexes = x
        self.curve = curve_vals
        self.abortQuery()
        if self.curve_fig is None:
            self.curve_fig = mpl.pyplot.figure(figsize=(2, 2), dpi=100)
            self.curve_graph = self.curve_fig.add_subplot(111)
            self.hist_line = self.curve_graph.plot(self.last_indexes, self.curve, 'k')[0]
#            self.curve_graph.clear()
            self.curve_graph.tick_params(labelsize=8)
#            self.curve_graph.set_aspect(1,adjustable='datalim')
        self.hist_line.set_data(self.last_indexes, self.curve)
        mar = 0.05
        yminlim = 0-mar
        ymaxlim = 1+mar
        if not 0-mar < self.curve.min() < 1+mar: 
            yminlim = self.curve.min()-mar  
        if not 0-mar < self.curve.max() < 1+mar: 
            ymaxlim = self.curve.max()+mar
        self.curve_graph.set_ylim(yminlim, ymaxlim)
        self.curve_graph.set_xlim(0,1)
        self.curve_graph.grid(True)     

        curve_img = filter_base.plotfig2image(self.curve_fig)
        self.setParamContent("Curve plot", curve_img, emitSignal=True)                
           
    def process(self, input_images, connected_outs):
        self.processParams()
        if 'Input' not in input_images: 
            return {}
        curved_im = filter_base.applyCurve( input_images['Input'], self.curve)    
        return {'Output':curved_im}                
        
        
def getFilterList():
    """Return a list of connected filters in order to test the current filter."""
    import filters_package as fpk
    loadf = fpk.input_filter.Input_filter()
    current = Curve_filter()
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
    
    