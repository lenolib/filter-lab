# -*- coding:utf-8 -*-

from filter_base import Filter_base, Parameter, SUCCESS, FAIL
import filter_base
import PyQt4


class Code_input_filter(Filter_base):
    name = "Code input"
    def __init__(self):
        Filter_base.__init__(self)        
        self.setupInputsOutputs(["inA", "inB", "inC"], ["outA","outB","outB"])
        self.description = "\
Specify any operations to apply to the input data. \
The command line input will be interpreted as a regular \
python command, so please be very careful not to do anything dangerous. \
If nothing is connected to an input, that input will be set as a scalar zero."
        self.addParam( Parameter(name="Code for imports", param_type="codebox", 
                                         default="import numpy as np\n\n\n", 
                                         rank=0, description="\
This code will only run once upon each edit, and make the declared names \
available in the processing code field below.") )
        self.addParam( Parameter(name="Processing code", param_type="codebox", rank=7, 
                                 default="outA = inA*x-inB*y-inC*z\n\n\n\n\n\n\n\n\n\n") )
        self.addParam( Parameter(name="Variable x", param_type="variable", 
                                 default=1, maximum=1, minimum=0, rank=1))
        self.addParam( Parameter(name="Variable y", param_type="variable", 
                                 default=1, maximum=1, minimum=0, rank=2))
        self.addParam( Parameter(name="Variable z", param_type="variable", 
                                 default=1, maximum=1, minimum=0, rank=3))        
        self.import_code = ""
        self.last_code = ""
        self.compcode = None
    
    
    def processParams(self):
        new_import_code = self.getParamContent("Code for imports")
        if new_import_code == self.import_code: return        
        compcode = compile(new_import_code,'<string>','exec')
        exec(compcode)
        self.import_code = new_import_code        
        del compcode,new_import_code
        for key,val in locals().iteritems():
            if key != 'self': 
                globals()[key] = val
        
    def process(self, input_images, connected_outs):        
        self.processParams()
        incode = self.getParamContent("Processing code")
        x = self.getParamContent("Variable x")
        y = self.getParamContent("Variable y")
        z = self.getParamContent("Variable z")
        if self.input_names[0] in input_images: inA = input_images['inA']
        else:                                   inA = 0            
        if self.input_names[1] in input_images: inB = input_images['inB']
        else:                                   inB = 0
        if self.input_names[2] in input_images: inC = input_images['inC']
        else:                                   inC = 0
        try:
            if incode != self.last_code:
                self.compcode = compile(incode,'<string>','exec')
                self.last_code = incode
            exec(self.compcode)
            results = {} 
            localscpy = locals()
            if 'outA' in localscpy: results['outA'] = outA
            if 'outB' in localscpy: results['outB'] = outB
            if 'ouktC' in localscpy: results['outC'] = outC
            return results
        except SyntaxError,e:
            print "In '%s': There was a non-critical SyntaxError: %s \n Command was: %s" %(self.name,e,incode)
        except NameError, e:
            print "In '%s': There was a non-critical NameError: %s \n Command was: %s" %(self.name,e,incode)
        except ValueError, e:
            print "In '%s': There was a non-critical ValueError: %s \n Command was: %s" %(self.name,e,incode)
        return FAIL

def getFilterList():
    """Return a list of connected filters in order to test the current filter."""
    import filters_package as imf
    loadf = imf.input_filter.Input_filter()
    current = Code_input_filter()    
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