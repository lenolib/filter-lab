# -*- coding:utf-8 -*-
"""
Created on 29 sep 2011

@author: lennart
"""
import filter_lab as flab
import sys,os    
    
if __name__ == "__main__":
    app,controls = flab.createApp()
    for modstr in dir(flab.filters_package):
        modu = getattr(flab.filters_package,modstr)
        if hasattr(modu,'getFilterList'):
            filters = modu.getFilterList()
            for fltr in filters:
                if isinstance(fltr,flab.filters_package.input_filter.Input_filter): 
                    fltr.setParamContent("Output type","original")
            controls.addFilters( filters )
#    controls.addFilters( flab.img_filters.curve_filter.getTestFilters() )
    controls.worker_thread.pause_resume()
    sys.exit(app.exec_())
    
    
    
    
    
    