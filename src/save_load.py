# -*- coding:utf-8 -*-

import cPickle
import pickle
import os
from filters_package.filter_base import EMPTY
import re
import imp

#Cleans a string to make it a valid python identifier (variable name)
clean = lambda varStr: re.sub('\W|^(?=\d)','_', varStr)


def loadFilters(filename):
    filename = unicode(filename).replace('\\','/')
    try:
        mod = imp.load_source("filtersfile", filename)
    except Exception as e:
        print "Could not load file. The exception was: ", e
        return [],[]
    getfilters = getattr(mod,'getFilterList')
    return_data = getfilters()
    if isinstance(return_data,tuple): positions,filter_list = return_data
    else: positions, filter_list = [], return_data
    return filter_list,positions

def saveFilters(filter_list, filename, positions=[]):
    """Construct python code which can produce new instances of filters in 
    'filter_list' with the original parameter values and save them to file.
    
    """
    main_dir = "os.path.split(os.path.split(__file__)[0])[0]"
    code = ["# -*- coding:utf-8 -*-"]
    code.append("#This python code creates a list of connected filter instances.")
    code.append('\n')
    code.append("import os,sys")
    code.append("sys.path.append(%s)" %main_dir)
    code.append("import filters_package")
    code.append("from filters_package.filter_base import connect_filters")
    code.append('\n')
    code.append("def getFilterList():")
    filt2name = {}
    name2filt = {}
    names_ordered = []
    for ind,fltr in enumerate(filter_list):
        class_chain = str(fltr.__class__)[8:-2]
        var_name = class_chain.split('.')[-1]+'_'+clean(unicode(fltr.name))        
        names_ordered.append(var_name)
        if var_name in name2filt: var_name+='I'
        code.append("%s = %s()" %(var_name,class_chain))
        code.append("%s.setName(\"\"\"%s\"\"\")" %(var_name,fltr.name))
        code.append("%s.setDescription(\"\"\"%s\"\"\")" %(var_name,fltr.description))
        if fltr.disabled: code.append("%s.disabled = True" %var_name) 
        for pname,param in fltr.params.iteritems():
            if param.type in ('list','file','codebox','text'):
                code.append(var_name + ".setParamContent(\"\"\"%s\"\"\",\"\"\"%s\"\"\")" %(pname,str(fltr.getParamContent(pname))) )
            if param.type == 'variable':
                code.append(var_name + ".setParamContent(\"\"\"%s\"\"\",%s)" %(pname,str(fltr.getParamContent(pname))) )
                code.append(var_name + ".getParam(\"\"\"%s\"\"\").min = %s" %(pname,str(param.min)) )
                code.append(var_name + ".getParam(\"\"\"%s\"\"\").max = %s" %(pname,str(param.max)) )
        filt2name[fltr] = var_name
        name2filt[var_name] = fltr
    code.append('\n')
    for fltr in filter_list:
        for input_name, parent_tuple in fltr.filter_inputs.iteritems():
            if parent_tuple != EMPTY:
                parent,output_name = parent_tuple 
                code.append("connect_filters(%s,%s,[\"\"\"%s\"\"\"],[\"\"\"%s\"\"\"])" %(filt2name[parent],
                                                                         filt2name[fltr],
                                                                         output_name,
                                                                         input_name) )
    code.append("positions = " + str(positions))
    code.append("filter_list = " + str([str(item) for item in names_ordered]).replace("'",""))
    code.append("return positions, filter_list\n")
    for ind,item in enumerate(code): #Finding index of function definition  
        if item == 'def getFilterList():': break
    code = code[:ind+1] + ['    '+item for item in code[ind+1:]]    
    
    code.append("""if __name__ == "__main__":""")
    code.append("""    import os,sys""")
    code.append("""    flabfile = os.path.join(%s,'filter_lab.py')""" %main_dir)
    code.append("""    os.system(\"\"\"%s "%s" "%s" \"\"\" %(sys.executable, flabfile, __file__))""")


    filename = unicode(filename).replace('\\','/')
    if not filename.endswith('.py'):
        filename += '.py'
    try:
        py_file = open(filename, 'wb')
        py_file.writelines([item+'\n' for item in code])
    except Exception as e: 
        raise Exception(e)
    finally: 
        py_file.close()
    
    return


def pickleFilters(filter_data, filename):
    filename = unicode(filename).replace('\\','/')
    if not filename.endswith('.pickle'):
        filename += '.pickle'
    try:
        pickle_file = open(filename, 'wb')
    #    cPickle.dump(filter_data, pickle_file)
        pickle.dump(filter_data, pickle_file, protocol=2)
    except Exception as e: 
        raise Exception(e)
    finally:
        pickle_file.close()
    return

def unpickleFilters(filename):
    filename = unicode(filename).replace('\\','/')
    if os.path.isfile(filename):
    #    filterlist = cPickle.load(pickle_file)
        try:
            pickle_file = open(filename, 'rb')
            filter_data = pickle.load(pickle_file)
        except Exception as e:
            print "Could not load file. The exception was: ", e
            pickle_file.close()
            return [],[]
        finally:
            pickle_file.close()
            
        return filter_data
    else:
        print "Could not find file to unpickle,", filename
        return [],[]
    
    
    