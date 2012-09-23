# -*- coding: utf-8 -*-
from __future__ import division
#from PyQt4.QtCore import *
from PyQt4 import QtCore
from PyQt4.QtGui import QImage, QPixmap, QColor
dummy_im = QImage(2,2,QImage.Format_Indexed8)
for i in range(256): dummy_im.setColor(i, QColor(i, i, i).rgb())
gray_table = dummy_im.colorTable()
import ctypes
import colorsys
import random
import time
import numpy
import cython_functions
import Image
import ImageOps
import textwrap
import StringIO
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sys 
import traceback
import pyopencv as pycv

SUCCESS = (1) #Defined as tuples to produce singletons (unique memory addresses for comparisons)
FAIL = (0)
EMPTY = 'empty'
OUTPUT = 'output'
INPUT = 'input'


"""
Filter type descriptions (see the comment for the WorkerThread.run method for 
further information: 
SOURCE_FILTER -- The filter produces original data and should be notified 
at the start of each processing loop to allow it to change it's internal 
behavior, such as preparing to process .   
STANDARD_FILTER -- 'standard_filter'  #The default type of filter, just a placeholder name
OUTPUT_FILTER -- 'output_filter'  #Is meant to be at the end of a filter chain, 
                  and is where the processing start 
"""
SOURCE_FILTER = 'source_filter'   
STANDARD_FILTER = 'standard_filter'  
OUTPUT_FILTER = 'output_filter'


class Parameter:
    """Class for holding a parameter value and meta-information about the parameter.
    
    Description of the class variables:
    name         -- the name of the parameter. It will be displayed in the GUI and used 
                    to retrieve the parameter. Can contain spaces.
    type         -- one of the types defined in the PARAMTYPES list of valid types.    
    description  -- description of the parameter. It will be displayed in the GUI.
    default      -- the default value of the parameter 
    content      -- the current value of the parameter
    min, max     -- can be set to supply a range for the interval of the value of a 
                    'variable' type parameter.
    other_content -- can be anything to also store in the parameter, or inthe 
    rank -- A value for ordering parameters in the GUI. Parameters with lower values
           are placed above those with higher values in GUI. Specification is not necessary.
    
    PARAMTYPES contains the allowed parameter types. This is necessary for the GUI
    to know how to display the content of the parameter, and how to edit it. 
    For a 'variable'-parameter the GUI will for example draw a slider and input boxes 
    for min and max values, and for a 'file'-parameter, will enable the user to select a file.
    
        'variable' -- The parameter will contain a scalar value that varies in the interval 
                      min-max. A value for 'content' have to be specified on creation 
                      of the parameter. Default limits for the GUI spinboxes are 
                      [-99999,99999], but could easily be changed.
        'file' -- The parameter will contain a string with a file path, 
                  ie "E:/new_folder/my_image.jpg"
                  In windows, be sure to convert backslashes (\) to slashes (/) 
                  if you enter a default value manually in the code, or use double backslashes.
        'list' -- The parameter will contain a list of predetermined choices which the GUI will
                  display as a drop-down list (combobox) which the user can select one of the 
                  entries from. If the items can not be transformed
                  into strings by the unicode() function, add them as tuples with a string description
                  as the first element in the tuple, for example ('Item description', the_item).
                  The function that will add them to the combobox will check if the item 
                  contains a tuple or not.
        'text' -- The parameter will contain a text input line which can be used to input 
                  anything to the filter.
        'codebox' -- The parameter will contain a scrollable multi-line python code 
                     input area. To set the height of the area, set the content so as 
                     to contain a number of newlines ("[some example code] \n\n\n\n").
        'display' -- The parameter will contain and display an image or a 
                     matplotlib figure (the latter slows downs the gui in 
                     the current implementation).

    """
    PARAMTYPES = ('variable','file','list','text','codebox','display')
    
    def __init__(self, name=None, param_type=None, description=None, default=None,
                 minimum=None, maximum=None, other_content=None, rank=None):        
        """Required arguments when creating a new instance are 'name' and 'param_type'."""
        if name is not None and param_type in self.PARAMTYPES:
            self.name = name
            self.type = param_type
        else:
            raise Exception("Error when creating parameter. Please specify a name and a valid parameter param_type")
        if param_type =='variable' and default is not None: 
            if minimum is None or maximum is None: print "Warning: minimum or maximum value for 'variable'-parameter '%s' is not set." %self.name             
            self.min = minimum
            self.max = maximum
        elif param_type =='variable' and default is None:
            raise Exception("Error when creating parameter. Please specify a value for variable or constant parameters.")
        if param_type == 'list' and (default is None or other_content is None):
            raise Exception("Error when creating parameter. Please specify a list as 'other_content' and the default list element as 'default'") 
        self.default = default                        
        self.content = self.default
        self.description = description
        self.other_content = other_content
        self.rank = rank
        
        
class Filter_base(QtCore.QObject):
    '''Class that all filters inherit most of their functionality from.  
    
    Description of the class variables:
        name -- The name of the filter that will be displayed in the GUI.
        guiColor -- The RGB-color of the filter displayed in the GUI. 
                    The default is (255,255,0), ie. yellow.
        input_names -- List of strings that name the inputs of the filter.
        output_names -- Equivalent of input_names for the filter's outputs. 
        updated -- Bool for knowing if the filter's content or function 
                   have been updated successfully since a change was made to its 
                   inputs or parameters.
        filter_inputs -- Dictionary with entries in the format 
                         input_names[x]:(parent_filter,"parent_filter_output_name")
                         i.e. a dictionary of tuples
                         It stores tuples since every input can only have one connection.
                         If no connection is made at an input, the dictionary content 
                         for that input name is the string 'empty'
        filter_outputs -- Dictionary with entries in the format 
                          output_names[x]:[(child_filter,"child_filter_input_name"), ...]
                          i.e. a dictionary of lists of tuples
                          If no connection is made at an output, the dictionary content
                          for that input name is an empty list, []
        result_data -- Dictionary of the filters result data in 
                       the format {output_names[x]:data} where 'data' will often be
                       a two-dimensional numpy array, usually with float32 or uint8 
                       values (dtype='f' or 'uint8')
        params -- Dictionary of the filters parameters in the 
                  format {"parameter name":parameter_instance}
        time_consumption -- Stores the time of the 'process' function each time it runs
        last_result -- [No description written yet. Possibly deprecated.]
        verbose -- Bool for optional print out of debugging information
        filtertype -- Determines what type the filter has, the default is STANDARD_FILTER.
                      See the comments for the constant definitions of 
                      SOURCE_FILTER, OUTPUT_FILTER and STANDARD_FILTER
    
    Functions intended to be called in subclasses:            
        In '__init__'-constructor:
            addParam
            setupInputsOutputs (required)
        Elsewhere:
            getParamContent
            setParamContent
            abortQuery    (recommended)
        
    
    Functions intended to be reimplemented in subclasses:
        process
        processParams        (optional)
        getAdditionalInfo    (optional)
    
    '''
    name = 'Not named filter'
    guiColor = (255,255,0)
    param_changed_in_filter_sig = QtCore.pyqtSignal(str,object)
    filter_name_change_sig = QtCore.pyqtSignal(object,object)
    filter_description_change_sig = QtCore.pyqtSignal(object,object)
    def __init__(self):        
        QtCore.QObject.__init__(self)
        self.input_names = []
        self.output_names = []
        self.updated = True
        self.filter_inputs = {}  
        self.filter_outputs = {}  
        self.result_data = {}  
        self.params = {}
        self.description = ""
        self.time_consumption = 0
        self.filtertype = STANDARD_FILTER
        self.last_result = SUCCESS
        self.verbose = False
        self.mutex = QtCore.QMutex()
        self.abort_processing = False
        self.disabled = False
        
    def __getstate__(self):
        self.result_data = {} #To reduce the file size of pickled saves.
        found_fig = False
        for attr in dir(self):
            if isinstance(getattr(self,attr), (plt.Figure,plt.Axes)):
                setattr(self,attr,None)
                found_fig = True
        if found_fig:
            for param_name in self.params:
                if self.params[param_name].type == 'display':
                    self.setParamContent(param_name, None)                
        return self.__dict__
    
    def __setstate__(self,dict_):
        QtCore.QObject.__init__(self)
        self.__dict__ = dict_

    def setName(self, name):
        self.name = name
        self.filter_name_change_sig.emit(self,self.name)
        
    def setDescription(self,description):
        self.description = unicode(description)
        self.filter_description_change_sig.emit(self,self.description)
        
    def getWrappedDescription(self):
        if self.description == "":
            return ""
        else:
            return '\n'.join(textwrap.wrap(self.description, 40))
        
    def getInfo(self):
        """Create a multi-line string with information about the filter's status and contents.
        To supply specific information for a filter, override the 'getAdditionalInfo' function.
        """ 
        lines = ""
        if self.description != "": lines += self.getWrappedDescription() + '\n----------------\n'
        additional = self.getAdditionalInfo()
        if additional != "": lines += additional + '\n'
        if self.result_data is not None and len(self.result_data)==0: "Content: None\n" 
        else: 
            lines += "Content:\n"
            if len(self.output_names) != 0:
                for output_name in self.output_names:
                    if output_name in self.result_data:
                        resdata = self.result_data[output_name]
                        if isinstance(resdata, numpy.ndarray): 
                            lines += (output_name + ": " + unicode(resdata.shape) + 
                                      ", dtype=" + unicode(resdata.dtype) +
                                      ", min: " + unicode(resdata.min()) +
                                      ", max: " + unicode(resdata.max()) + "\n")
                        else:
                            lines += output_name + ": " + unicode(resdata.__class__)
                            if isinstance(resdata,(str,list,tuple,dict)):
                                lines += ", Length: " + unicode(len(resdata))
                            lines += "\n"
            else:
                for data_name in self.result_data:
                    if data_name in self.result_data:
                        data = self.result_data[data_name]
                        if isinstance(resdata, numpy.ndarray):
                            lines += data_name + ": " + unicode(data.shape) + ", dtype=" + unicode(data.dtype) + "\n"
                        else: continue        
        return lines
    
    def getAdditionalInfo(self):
        """Overload in inherited classes to provide additional tool-tip information.
        Returns an empty string by default. """
        return ""
    
    def addParam(self, parameter):
        """Add a parameter to the filter."""
        if parameter.type in Parameter.PARAMTYPES:
            if parameter.name not in self.params.keys():
                self.params[parameter.name] = parameter
            else:
                print "Error: Could not add parameter when creating a new filter since a parameter with the same name was already added to the parameter dictionary. Name was:", parameter.name
                return
        else:
            print "InError: Could not add parameter since the parameter has an unrecognized type. Specified type was:", parameter.type
            return

    def getParamContent(self, name):
        """Return the filter's parameter with name 'name'."""
        try: return self.params[name].content
        except:
            print "Could not find a parameter with name: " + name
            raise
    
    def getParam(self, name):
        """Return the filter's parameter with name 'name'."""
        return self.params[name]
        
            
    def setParamContent(self, name, content, emitSignal=False):
        """Set the content of the parameter with the name 'name' to 'content'.
        Send signal go gui to update.
        """
        try:
            self.params[unicode(name)].content = content
            self.setUpdated(False)      
            if emitSignal == True: 
                self.param_changed_in_filter_sig.emit(name,content)
        except KeyError:
            traceback.print_exc()
            print "Error: Could not find a parameter with name: ", name, ", in filter: ", self.name
    
    def setupInputsOutputs(self, input_names, output_names):
        """Add the string elements of the lists'input_names' and 'output_names' to 
        the filter_input and filter_output dictionaries.
        
        Arguments are:
        input_names -- A list of strings with the names of the filters inputs, for example:
                       ["input 1", "input 2"]. If the filters does not have any inputs,
                       explicitly specify a empty list, []
        output_names -- The equivalent of input_names for the filters outputs.
        
        Setups the filters filter_inputs and filter_outputs dictionaries with 
        specific names for the outputs and inputs.
        
        """
        self.input_names = input_names
        self.output_names = output_names
        for name in self.input_names:  #Should perhaps empty the dictionaries first, in case a reduction in inputs or outputs occurs
            self.filter_inputs[name] = EMPTY
        for name in self.output_names:
            self.filter_outputs[name] = []   
    
    def getOutput(self, output_name):
        """Return the data on the output with name output_name, return FAIL otherwise.
        
        Runs the filter if necessary and then returns the data with key 'output_name'
        in result_data, or FAIL if it could not be found in result_data even 
        after running the filter once.
        
        """
        if self.disabled: return FAIL
        if self.updated == False or output_name not in self.result_data:
            if self.run_filter() is FAIL:
                self.last_result = FAIL
                return FAIL 
        if self.result_data is not None and output_name in self.result_data:
            return self.result_data[output_name]
        else:
            return FAIL      
    
    def abortProcessing(self):
        """Convenience function for 'setAbort(True)"""
        self.setAbort(True)
        
    def setAbort(self, abortBool):
        self.mutex.lock()
        self.abort_processing = abortBool
        self.mutex.unlock()
        
    def abortQuery(self):
        """Check if the processing has been requested to stop, if so raise AbortException
        
        Call this function inside potentially computation intensive loops
        in order to cancel the computation it has been requested of the filter 
        by the user. 
        Note that in order to be able to call it from a function, that function 
        must have a reference to the filter instance, i.a. be a member function
        of the filter class. 
        The call looks like 'self.abortQuery()' or 'filter_instance.abortQuery()'
        """
        if self.abort_processing:
            raise AbortException()

    def run_filter(self):
        """Request input data, process, save the result, return SUCCESS or FAIL.
        
        The filter checks which of its inputs and outputs are connected,
        requests data on each of its connected inputs, and then tries to
        process that data and save the result in its class variable result_data.
        Depending on if all went fine or not, the function returns the 
        constants SUCCESS or FAIL. 
        
        """        
        if self.disabled: return FAIL
        connected_ins, connected_outs = checkConnectedness(self)
        input_data = {}
        for input_name in connected_ins:
            output_parent = connected_ins[input_name][0]
            output_name = connected_ins[input_name][1]
            received_output = output_parent.getOutput(output_name)  #Getting parent output (running parent if necessary)
            if received_output is FAIL:
                return FAIL
            else:
                input_data[input_name] = received_output 
        t = time.clock()
        try:
            self.abortQuery()
            received_result = self.process(input_data, connected_outs)
        except AbortException:
            self.time_consumption = "Stopped"
            return FAIL
        except Exception:
            self.time_consumption = "Failed"
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print "Caught error in '%s': " %(self.name)
            traceback.print_exception(exc_type, exc_value, exc_traceback)
            return FAIL
        finally: self.setAbort(False)
        
        if not isinstance(received_result,dict):
            self.time_consumption = "Failed"
            return FAIL
        else:
            self.time_consumption = time.clock()-t 
            self.result_data = received_result
            self.setUpdated(True)            
            return SUCCESS   
    
    def process(self, input_data, connected_outs):
        """Process the 'input_data' and return the result data if successfull, FAIL otherwise.
        
        Arguments are:
        input_data -- a dictionary of the filter's connected inputs' data 
                        in the format {'input_name':data}
        connected_outs -- a dictionary of the filter's connected outputs 
                          in the format {'output_name':[(child_filter,'child_input_name'),...]}
                          The content the dictionary's items is often not relevant more than
                          to know which of the filter's outputs are connected and which aren't, 
                          allowing the filter's process to choose not to process data for 
                          outputs that are not connected anyway.
        
        This is the function that does the real data processing in the filter.
        The function returns a dictionary of data in a format that 
        is the same as that for result_data, {'filter_output_name':data} 
        where data will often be a two-dimensional numpy array with 
        float32 values (dtype='f'), but could be anything.
        
        This function is meant be reimplemented in each filter implementation.
        
        Exceptions raised in this function will be caught and handled by the
        run_filter() function.
        
        """
        print "ERROR: The 'process' function ought to be reimplemented in filter:", self.name
        return FAIL
    
    def processParams(self):
        """Perform processing of parameters upon a change to some of the parameters of the filter.
        
        This method will be run even though the worker thread is paused, to allow 
        parameters to interact with each other (such as one parameter changing 
        another parameters content (through 'self.setParamContent()'). 
        This method can very well be called from 
        inside the 'process' method often as a first step to avoid code duplication.
        It may return anything or nothing, or alternatively the result could be 
        saved as class instance variables (i.e. self.xxx=result_xxx) to make them
        accessible inside the 'process' function.
        
        """
        pass
    
    def setUpdated(self, value):
        self.mutex.lock()
        self.updated = value
        self.mutex.unlock()
    
    def change_notice(self):
        """Notify this filter that a change has occurred in one of its parents, 
        and notify its children.""" 
        self.setUpdated(False)
        self.notify_children()
    
    def notify_children(self):
        """Notify all the filters children that the filter have changed in some way."""
        notified_children = []
        for output_name, child_tuple_list in self.filter_outputs.iteritems():
            if child_tuple_list:
                for child_tuple in child_tuple_list:
                    if child_tuple[0] not in notified_children:
#                        print 'notifying', child_tuple[0].name
                        child_tuple[0].change_notice()             
    
    def getEmptyInputs(self):
        cins = checkConnectedness(self)[0]
        return [name for name in self.input_names if name not in cins]    
    
    def getEmptyOutputs(self):
        couts = checkConnectedness(self)[1]
        return [name for name in self.output_names if name not in couts]
    
    def getOccupiedInputs(self):
        cins = checkConnectedness(self)[0]
        return [name for name in self.input_names if name in cins]
        
    def getOccupiedOutputs(self):
        couts = checkConnectedness(self)[1]
        return [name for name in self.output_names if name in couts]
    
    def getConnections(self, otherF, return_connection_type=False):
        """Return the type and names of connections this filter has to filter 'other'."""
        
        cins, couts = checkConnectedness(self)
        outs = [outp for outp in couts.keys() 
                if otherF in [tup[0] for tup in couts[outp]]] 
        ins = [inp for inp in cins.keys() if otherF == cins[inp][0]]
        if ins and outs:
            print "Notice: Loop connection detected between '%s' and '%s'." %(self.name, otherF.name)
            return outs
        elif ins: 
            if return_connection_type: return ins,INPUT
            else: return ins
        elif outs: 
            if return_connection_type: return outs,OUTPUT
            else: return outs      
        else: return []        
        
    def getInputsConnectedTo(self,fltr):
        cins = checkConnectedness(self)[0]        
        return [inp for inp in self.input_names 
                if inp in cins and fltr == cins[inp][0]]
    
    def getOutputsConnectedTo(self,fltr, return_duplicates=False):
        couts = checkConnectedness(self)[1]
        if return_duplicates:
            inputs = fltr.getInputsConnectedTo(self)
            return [fltr.filter_inputs[inp][1] for inp in inputs]
        else:
            return [output for output in self.output_names 
                    if output in couts and fltr in [tup[0] for tup in couts[output]] ]


class AbortException(Exception):
    def __init__(self): Exception.__init__(self,"Process was aborted")            
            
            
def getRandColor():
    h = random.uniform(0, 1) # Select random green'ish hue from hue wheel
    s = random.uniform(0.7, 1)
    l = random.uniform(0.6, 0.7)
    r, g, b = [int(x*255) for x in colorsys.hls_to_rgb(h, l, s)]
    return (r,g,b)
                
def checkConnectedness(fltr):
    connected_ins = {}
    connected_outs = {}
    for input_name, parent_tuple in fltr.filter_inputs.iteritems():
        if parent_tuple != EMPTY: connected_ins[input_name] = parent_tuple            
    for output_name, child_tuple_list in fltr.filter_outputs.iteritems():
        if child_tuple_list != []: connected_outs[output_name] = child_tuple_list
    return connected_ins, connected_outs

def autoConnectPair(parent,child):
    """Connect a pair of filters based on deductions."""
#    cinsP,coutsP = checkConnectedness(parent)
#    cinsC,coutsC = checkConnectedness(child)    
    emptyC = child.getEmptyInputs()
#    emptyP = parent.getEmptyOutputs()
    if not emptyC: return FAIL
    else:
        outP, inC = None, None
        for outname in parent.output_names:
            if parent.filter_outputs[outname] == []:
                outP = outname
                break
        if outP is None and parent.output_names:
            outP = parent.output_names[0]
        for inname in child.input_names:
            if child.filter_inputs[inname] == EMPTY:
                inC = inname
                break
        if outP and inC:
            connect_filters(parent, child, [outP], [inC])
        else:
            return FAIL
    return SUCCESS           
#    if emptyC == 1:
#        [connect first P to first empty in C]
#    if emptyC == 2:
#        if emptyP

def insertFilter(insert,parent,child, auto_identify=False):
    """Insert one filter between two others seamlessly. 
    If uncertain of the arguments' identities, supply auto_identify argument.
    """
    if auto_identify:
        filtA, filtB, filtC = insert, parent, child                        
        intercons = [filtA.getConnections(filtB),
                    filtA.getConnections(filtC),
                    filtC.getConnections(filtB)]
        if sum(1 for item in intercons if len(item) == 0) != 2:
            print "Could not insert filter because of detected unexpected inter-connectivity."
            return FAIL
        if len(filtA.getConnections(filtB))==0 and len(filtA.getConnections(filtC))==0: 
            insert,pair = filtA,(filtB,filtC)
        elif len(filtB.getConnections(filtA))==0 and len(filtB.getConnections(filtC))==0: 
            insert,pair = filtB,(filtA,filtC)
        elif len(filtC.getConnections(filtA))==0 and len(filtC.getConnections(filtB))==0: 
            insert,pair = filtC,(filtA,filtB)
        dummy, filter_type = pair[0].getConnections(pair[1], return_connection_type=True)
        if filter_type == INPUT: child,parent = pair[0],pair[1]
        else: child,parent = pair[1],pair[0]

    coutsP = parent.getConnections(child)
    cinsC = child.getConnections(parent)
    ncon = len(coutsP)
    einsI = len(insert.getEmptyInputs())
    eoutsI = len(insert.getEmptyOutputs()) 
    if insert.getConnections(parent) or insert.getConnections(child):
        print "Could not insert '%s' because it's already connected to '%s' or '%s'." %(insert.name,parent.name,child.name)
        return FAIL       
    if einsI < ncon or eoutsI < ncon:
        print "Please make sure '%s' has enough free inputs and outputs." %insert.name
        return FAIL    
    res1 = disconnect_filters(parent,child,coutsP,cinsC)
    res2 = connect_filters(parent,insert,coutsP,insert.getEmptyInputs()[:ncon])
    res3 = connect_filters(insert,child,insert.getEmptyOutputs()[:ncon], cinsC)
    if res1 is FAIL or res2 is FAIL or res3 is FAIL: return FAIL
    else: return SUCCESS
    
def remove_filter(fltr):
    """Disconnect the filter from all other filters. Raise an exception if unsuccessfull."""
    for inp in fltr.filter_inputs:
        if fltr.filter_inputs[inp] != EMPTY:
            parent = fltr.filter_inputs[inp][0]
            output = fltr.filter_inputs[inp][1]
            if disconnect_filters(parent, fltr, [output], [inp]) is FAIL:
                raise Exception("Something went wrong when trying to remove the filter")
    for out_list in fltr.filter_outputs:
        for output in fltr.filter_outputs[out_list]:
            if disconnect_filters(fltr, output[0], [out_list], [output[1]]) is FAIL:
                raise Exception("Something went wrong when trying to remove the filter")
    del fltr #Will automatically garbage collect without specific deletion?

def disconnect_filters(parent, child, outputs='ALL', inputs='ALL'):
    """Disconnect filters and return SUCCESS if successful, FAIL otherwise.
    
    Arguments are:
    parent -- the filter instance providing the output
    child -- the filter instance providing the input
    outputs -- list of strings with the output names to be disconnected, 
               for example ["output 1", ...]
    inputs -- equivalent of outputs

    Disconnects the inputs of the child filter to the outputs of the parent filter. 
    The outputs and inputs lists must match in length, 
    since corresponding (list order, not names) indexes will be disconnected.
    
    """
    if parent == child: return FAIL
    if outputs=='ALL' and inputs=='ALL':
        outputs = parent.getOutputsConnectedTo(child, return_duplicates=True)
        inputs = child.getInputsConnectedTo(parent)
        if not outputs:
            return FAIL
    elif (outputs=='ALL') + (inputs=='ALL') == 1:
        raise Exception("Unsupported configuration of parameters in function call")
    
    if len(outputs)!=len(inputs):
        print 'could not disconnect to parent since the number of ouputs does not equal the number of inputs'
        return FAIL
    for ind in range(len(inputs)):
        if inputs[ind] not in child.filter_inputs or outputs[ind] not in parent.filter_outputs:
            print ("Could not find output or input name among the filters' outputs and inputs:", 
                   inputs[ind],' or ', outputs[ind])
            return FAIL        
        if child.filter_inputs[inputs[ind]] != EMPTY:  #Could be connected to the filter we're trying to disconnect, or to another one
            if (child, inputs[ind]) in parent.filter_outputs[outputs[ind]]:
                parent.filter_outputs[outputs[ind]].remove( (child, inputs[ind]) )
            else:
#                print "Filters are not connected, could not disconnect, but that's probably OK."
                return FAIL
            child.filter_inputs[inputs[ind]] = EMPTY   
        else:
            print "Input is not connected to anything, so cannot be disconnected."
            return FAIL
    child.change_notice()
    return SUCCESS

def connect_filters(parent, child, outputs, inputs):
    """Connect filters and return SUCCESS if successfull, FAIL otherwise.
    
    Arguments are:
    parent -- the filter instance providing the output
    child -- the filter instance providing the input
    outputs -- list of strings with the output names to be connected, for example ["output 1", ...]
    inputs -- equivalent of outputs
    
    Connects the inputs of the child filter to the outputs of the parent filter. 
    The outputs and inputs lists must match in length, 
    since corresponding (list order, not names) indexes will be connected.
    
    """
    if len(outputs)!=len(inputs):
        print 'could not connect to parent since the number of ouputs does not equal the number of inputs'
        return FAIL
    if parent == child:
        print "could not connect the filter to itself"
        return FAIL
    for ind in range(len(inputs)):
        if inputs[ind] not in child.filter_inputs or outputs[ind] not in parent.filter_outputs:
            print ("Could not find output or input name among the filters' outputs and inputs:", 
                   inputs[ind],' or ', outputs[ind])
            return FAIL
        if child.filter_inputs[inputs[ind]] == EMPTY:
            child.filter_inputs[inputs[ind]] = (parent, outputs[ind])
            parent.filter_outputs[outputs[ind]].append( (child, inputs[ind]) )
        else:
            print "One or more of the inputs are already in use. Could not connect to parent filter"
            return FAIL
    child.change_notice()
    return SUCCESS    

            
def load_image(filepath):
    """Load an image from disk and return it as a numpy array"""
    try:
        loaded_image = numpy.asarray( Image.open(filepath) )
    except:
        return None
    return loaded_image
    
def applyCurve(arr, curve_vec):
    """Apply 'curve_vec' to 'arr' via lookup table.
    
    Arguments are:
    arr -- The source array to apply curve to.
    curve_vec -- a vector with at least 2 elements
    
    """
    if len(curve_vec) <= 1:
        raise Exception("The curve to apply must have at least two values.")
    if arr.dtype != numpy.dtype('f'):
        arr = arr.astype('f')
    if curve_vec.dtype != numpy.dtype('f'):
        curve_vec = curve_vec.astype('f')
    if arr.ndim == 1: 
        new_arr = numpy.empty((1,len(arr)),dtype='f')
        new_arr[1,:] = arr
    curved = numpy.empty_like( arr )
    if arr.ndim == 2:
        curved = cython_functions.cyth_curve(arr, curve_vec)
    elif arr.ndim == 3:
        for i in range(arr.shape[2]):
            curved[:,:,i] = cython_functions.cyth_curve(arr[:,:,i], curve_vec)
    return curved

def make_uint8(arr_im):
    """Make a floating point matrix into one with 8-bit values (0-255).
    
    If the matrix only contains values between 0 and 1, the function will treat
    those numbers as the maximum and minimum pixel values of the image when it calls
    the 'remap' function.
    """
    if arr_im.min() >= 0 and arr_im.max() <= 1:
        return numpy.around(arr_im*255).astype('uint8')
    else:        
        rmp_im = remap(arr_im, min=0, max=1, curr_min=arr_im.min(), curr_max=arr_im.max())
        return numpy.around(rmp_im*255).astype('uint8')

def make_normfloat32(arr_im):
    """Makes a matrix into one with floating points between 0 and 1."""
    if arr_im.dtype == 'uint8':
            return numpy.asarray(arr_im/255, 'f')
        
    if arr_im.ndim >= 3:
        rmp_im = numpy.empty(arr_im.shape,'f')
        for i in range(arr_im.ndim):
            rmp_im[:,:,i] = remap(arr_im[:,:,i], min=0,max=1)
    else:
        rmp_im = remap(arr_im, min=0,max=1)
    return rmp_im
            
def remap(src_im, min=0., max=1., curr_min=0., curr_max=0., mode='cython'):
    """Remap src_im's pixel values to the range (min,max). Use curr_min and curr_max to
    specify the current range of the image. If not specified, they will be detected."""
    if src_im.dtype != 'float32':
        src_im = src_im.astype('f')
    if mode == 'cython':
        remapped_im = numpy.empty( src_im.shape, 'f' )  
        if src_im.ndim == 2:
            remapped_im = cython_functions.cyth_remap(src_im, float(min), float(max),
                                                      float(curr_min),float(curr_max))
        elif src_im.ndim == 3:
            for i in range(src_im.shape[2]):
                remapped_im[:,:,i] = cython_functions.cyth_remap(
                                            src_im[:,:,i], float(min), float(max), 
                                            float(curr_min),float(curr_max)
                                            ) 
        else: raise Exception("Weird image dimensions")    
    
    else:
        if curr_min == curr_max:
            curr_max = src_im.max()
            curr_min = src_im.min()
        scale = (max-min)/(curr_max-curr_min)
        if mode == 'cv':
            if src_im.flags['C_CONTIGUOUS'] == False:
                src_im = numpy.ascontiguousarray(src_im)
            arrmat = pycv.asMat(src_im)                   
            dst = pycv.Mat(*src_im.shape+(pycv.CV_32F,))
            pycv.Mat.convertTo(arrmat,dst,pycv.CV_32F,scale,min*(1-scale))
            return dst.ndarray
        else:
            remapped_im = src_im*scale+min*(1-scale)
            if remapped_im.max()>max or remapped_im.min()<min: 
                remapped_im = remapped_im.clip(min=min,max=max)
    return remapped_im

def plotfig2image(fig):
    """Convert a matplotlib pyplot figure to a numpy image."""
    imgdata = StringIO.StringIO()
    fig.savefig(imgdata, format='png')        
    imgdata.seek(0)  # rewind the data
    im = ImageOps.grayscale(Image.open(imgdata))
    return numpy.asarray( im )
    
#def curve2image(x_vals,y_vals, width=4, height=3):
#    """Plot y against x with matplotlib and return the result as a numpy image."""
#    fig = plt.figure(figsize=(width,height), dpi=100)
#    ax = fig.add_subplot(111)
#    try:
#        ax.plot(x_vals, y_vals)
#    except Exception,e:
#        print "Error when creating graph,", e
#        return numpy.zeros((30,30))
#    return plotfig2image(fig)

def arr2pixmap(disp_im):
    if disp_im.ndim != 3 and disp_im.ndim != 2:
        raise Exception("Wrong image dimensions in arr2pix()")
    if disp_im.dtype != 'uint8':
        disp_im = make_uint8(disp_im)
    if disp_im.flags['C_CONTIGUOUS'] == False:
        disp_im = numpy.ascontiguousarray(disp_im, 'uint8')
    if disp_im.ndim == 3:
        qimg = QImage(disp_im.data, disp_im.shape[1], disp_im.shape[0], 
                          disp_im.strides[0], QImage.Format_RGB888)        
    elif disp_im.ndim == 2:        
        qimg = QImage(disp_im.data, disp_im.shape[1], disp_im.shape[0], 
                      disp_im.strides[0], QImage.Format_Indexed8)
        qimg.setColorTable(gray_table)
    pixm = QPixmap.fromImage(qimg)
    return pixm

def pycv_power(arr, exponent):
    """Raise the elements of a floating point matrix to a power. 
    It is 3-4 times faster than numpy's built-in power function/operator."""
    if arr.dtype not in [numpy.float32, numpy.float64]:
        arr = arr.astype('f')
    res = numpy.empty_like(arr)
    if arr.flags['C_CONTIGUOUS'] == False:
        arr = numpy.ascontiguousarray(arr)        
    pycv.pow(pycv.asMat(arr), float(exponent), pycv.asMat(res))
    return res    

def resize(image, percent=None, new_H=None, new_W=None, aspect_ratio=1, method='Bilinear'):
    if method == 'Bilinear':
        method = pycv.INTER_LINEAR
    elif method == 'Nearest-neighbor':
        method = pycv.INTER_NEAREST
    elif method == 'Bicubic':
        method = pycv.INTER_CUBIC
    else:
        raise Exception("Invalid resize method.")    
    old_W = image.shape[1]
    old_H = image.shape[0]
    if percent is not None:
        new_W = int( old_W*percent/100/aspect_ratio )
        new_H = int( old_H*percent/100*aspect_ratio )
        if new_W == 0: new_W = 2
        if new_H == 0: new_H = 2
    elif new_H is not None and new_W is None:
        new_W = int( new_H/old_H*old_W )
    elif new_H is None and new_W is not None:
        new_H = int( new_W/old_W*old_H )
    elif new_H is not None and new_W is not None:
        pass    
    else:
        raise Exception("Wrong arguments to resize function.")
    limit = 10000
    if new_W > limit : 
        print "Image resize limit has been set to %d pixels. Limiting to %d." %(limit)
        new_W = limit
    if new_H > limit: 
        print "Image resize limit has been set to %d pixels. Limiting to %d." %(limit)
        new_H = limit
    if image.flags['C_CONTIGUOUS'] == False:
        image = numpy.ascontiguousarray(image)
    
    if image.dtype == 'uint8':
        np_type = 'uint8'
        cv_type = pycv.CV_8U
    elif image.dtype == 'float32':
        np_type = 'float32'
        cv_type = pycv.CV_32F
    else:
        raise Exception("Unsupported data type for resize.")
    
    if (old_W,old_H)==(new_W,new_H): return image
    if image.ndim == 3:
        res = numpy.empty((new_H,new_W,3),np_type)
    elif image.ndim == 2:
        res = numpy.empty((new_H,new_W),np_type)
    else:
        raise Exception("Can't handle image dimensions when resizing.")
    pycv.resize(pycv.asMat( image ), 
                pycv.asMat( res ), 
                pycv.Size2i(new_W,new_H), 
                cv_type,
                interpolation=method)
    return res

def keep_busy(busy_time):
    "Keep busy to achieve a busy sleep for debugging purposes"
    t = time.clock()
    while(time.clock()-t<wait_time): 
        rand = numpy.random.rand(100,100)
        sor = numpy.sort(rand)
                