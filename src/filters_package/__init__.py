# -*- coding: utf-8 -*-    

from filter_base import Filter_base 

import os
import inspect
filter_class_name_dict = {}
filter_given_name_dict = {}

#Could add code to check no filters have the same given names or class names if deemed necessary
for mod_name in os.listdir(os.path.dirname(__file__)):
    if mod_name == '__init__.py' or mod_name[-3:] != '.py' or mod_name[:-3] == 'filter_base':
        continue

    try:
        module = __import__(mod_name[:-3],globals(),locals(),[],-1)
    except ImportError as e:
        print "Could not import '%s', error was:" %mod_name, e
        continue
    globals()[mod_name[:-3]] = __import__(mod_name[:-3],globals(),locals(),[],-1)

    for obj_name,obj in inspect.getmembers(module):
        if inspect.isclass(obj):
            if issubclass(obj,Filter_base) and obj_name != 'Filter_base':
                print "imported:", obj_name
                __import__(mod_name[:-3],globals(),locals(),fromlist=[obj_name])
                filter_class_name_dict[obj_name] = obj
                filter_given_name_dict[obj.name] = obj
del mod_name,os,inspect,obj,obj_name,module
