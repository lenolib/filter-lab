# -*- coding: utf-8 -*-
from filter_base import Filter_base, Parameter, SUCCESS, FAIL, OUTPUT_FILTER, arr2pixmap
import filter_base
import numpy
import time

class Display_filter(Filter_base):
    """This filter will save anything inputed to it in its 'result_images' dictionary."""
    name = 'Display'
    guiColor = (0,255,255)
    def __init__(self):
        Filter_base.__init__(self)
        self.i_bwrgb = 'BW or RGB'
        self.i_ch1 = 'Ch 1, Red'
        self.i_ch2 = 'Ch 2, Green'
        self.i_ch3 = 'Ch 3, Blue'
        self.setupInputsOutputs([self.i_bwrgb,self.i_ch1,self.i_ch2,self.i_ch3], [] )
        self.description = "\
Display a image in the viewer window. \
If the input images' pixels are not all in the [0,1] range, \
they will get compressed into this range by the 'remap'-function. \n\
If something is connected to the 'B&W or RGB' input, all other inputs \
will be ignored.\
"
        self.painted = False 
        self.visible = True  
        self.addParam( Parameter(name='Resize (%)', param_type='variable', 
                         default=100, minimum=0, maximum=200, rank=1) )
        self.addParam( Parameter(name='Resize method', param_type='list', default='Bilinear', 
                                 other_content=['Bilinear', 'Nearest-neighbor'],
                                 rank=0.5) ) #Bicubic not offered because of deviating behavior on floating point images.
        self.pixmap = None 
        self.filtertype = OUTPUT_FILTER        
        
    
    def setVisible(self, bool_var):
        self.mutex.lock()
        self.visible = bool_var
        self.mutex.unlock()
    
    def change_notice(self):    
        """Override the inherited function and set the state of the filter."""    
        self.setUpdated(False)
        self.painted = False
        
    def process(self, input_images, connected_outs):
        """Return a black&white image if something is connected to the B&W input, 
        otherwise return an RGB-image with unconnected channels zeroed (pure black).
        """
        names = self.input_names
        if len(input_images)==0:
            self.pixmap = None
            return {}
        
        processed_images = {}
        
        if names[0] in input_images: 
            bw_rgb = input_images[names[0]]
            if not (bw_rgb.ndim == 3 and bw_rgb.shape[2] == 3) and bw_rgb.ndim > 2:
                print "In '%s': Multichannel image must have 3 channels to display." %self.name
                return FAIL
            else:
                processed_images[names[0]] = bw_rgb
        else:     
            for i,channel in enumerate([self.i_ch1, self.i_ch2, self.i_ch3]):
                if channel in input_images:
                    ch_im = input_images[channel] 
                    if ch_im.ndim == 3 and ch_im.shape[2] == 3: 
                        try:
                            processed_images[channel] = ch_im[:,:,i]
                        except ValueError:
                            print "Can not display image in '%s' unless all channels have the same dimensions." %(self.name)
                            return FAIL
                    elif ch_im.ndim > 2:
                        print "In '%s': Multichannel image must have 3 channels to display." %self.name
                        return FAIL
                    else:
                        processed_images[channel] = input_images[channel]
                     
        res_images = self.resizeQuery(processed_images)
        disp_im = self.constructFinal(res_images)
        try: self.pixmap = arr2pixmap(disp_im)
        except Exception as e: print e
        return {}
    
    
    def constructFinal(self, res_images):
        if self.i_bwrgb in res_images:
            disp_im = res_images[self.i_bwrgb]
        elif len(res_images) != 0:
            zero_im = numpy.zeros_like( res_images.itervalues().next() )
            disp_im = numpy.empty( (zero_im.shape[0], zero_im.shape[1], 3) )
            if self.i_ch1 in res_images: disp_im[:,:,0] = res_images[self.i_ch1]
            else: disp_im[:,:,0] = zero_im
            if self.i_ch2 in res_images: disp_im[:,:,1] = res_images[self.i_ch2]
            else: disp_im[:,:,1] = zero_im
            if self.i_ch3 in res_images: disp_im[:,:,2] = res_images[self.i_ch3]
            else: disp_im[:,:,2] = zero_im
        else:        
            disp_im = None #In case of no input images, display a small black square.
        return disp_im
    
    def resizeQuery(self, processed_images):
        percent = self.getParamContent("Resize (%)")
        if percent == 100:
            return processed_images
        else:
            method = self.getParamContent('Resize method')
            for name in processed_images:
                processed_images[name] = filter_base.resize(processed_images[name], 
                                                           percent=percent, method=method)
        return processed_images 
    

#    def __getstate__(self):
#        """Prepare the filter for pickling (saving) by deleting the capture objects 
#        that causes trouble when pickling."""
#        pickle_dict = self.__dict__.copy()
#        del pickle_dict['pixmap']        
#        return pickle_dict
#        
#    def __setstate__(self, dict):
#        """Restore the capture objects to the filter when unpickling (loading)."""
#        super(Display_filter, self).__setstate__(dict)
#        self.__dict__ = dict
#        self.pixmap = None
#            


        
