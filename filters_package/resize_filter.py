# -*- coding: utf-8 -*-    

from filter_base import Filter_base, Parameter, SUCCESS, FAIL
import filter_base

class Resize_filter(Filter_base):
    name = 'Resize'
    def __init__(self):
        Filter_base.__init__(self)
        self.description = "Resize the input image's dimensions by various methods. \
IMPORTANT IMPLEMENTATION NOTE: If the input pixels have float type and 'Bicubic' is chosen, \
the output image will be clipped to the minimum and maximum pixel values of the input image \
to ensure similar result to the other methods."
        self.setupInputsOutputs(['Input 1','Input 2','Input 3'], 
                                 ['Output 1','Output 2','Output 3'])
        self.addParam( Parameter(name='Resize by', param_type='list', default='percent and aspect ratio', 
                                 other_content=['percent and aspect ratio', 
                                                'width and height',
                                                'width and automatic height',
                                                'height and automatic width'],
                                 rank=0) ) 
        self.addParam( Parameter(name='Percent of original size', param_type='variable', 
                                 default=100, minimum=0, maximum=200, rank=1) )
        self.addParam( Parameter(name='Aspect ratio (width:height)', param_type='variable', 
                                 default=1, minimum=0.2, maximum=2, rank=2) )
        self.addParam( Parameter(name='New height', param_type='variable', 
                                 default=640, minimum=64, maximum=2048, rank=3) )
        self.addParam( Parameter(name='New width', param_type='variable', 
                                 default=640, minimum=64, maximum=2048, rank=4) )                
        self.addParam( Parameter(name='Resize method', param_type='list', default='Bilinear', 
                                 other_content=['Bilinear', 'Nearest-neighbor','Bicubic'],
                                 rank=0.5) )       
        
    def process(self, input_images, connected_outs):  
        new_height = int(self.getParamContent('New height'))
        new_width = int(self.getParamContent('New width'))
        percent = self.getParamContent('Percent of original size')
        aspect = self.getParamContent('Aspect ratio (width:height)')
        if percent == 0: percent = 0.02
        if aspect == 0: aspect = 0.02        
        resize_method = self.getParamContent('Resize method')
        processed_images= {}
        for i in (0,1,2):
            if (self.input_names[i] in input_images and 
                self.output_names[i] in connected_outs):
                choice = self.getParamContent('Resize by')
                image = input_images[self.input_names[i]]
                if choice == 'percent and aspect ratio':
                    if percent == 100 and aspect == 1: 
                        res = image
                    else:
                        res = filter_base.resize(image,
                                                percent = percent,
                                                aspect_ratio = aspect,
                                                method = resize_method)
                elif choice == 'width and height':
                    res = filter_base.resize(image,
                                            new_W = new_width,
                                            new_H = new_height,
                                            method = resize_method)
                elif choice == 'width and automatic height':
                    res = filter_base.resize(image,
                                            new_W = new_width,                                        
                                            method = resize_method)
                elif choice == 'height and automatic width':
                    res = filter_base.resize(image,
                                            new_H = new_height,                                        
                                            method = resize_method)
                
                if resize_method == 'Bicubic' and image.dtype == 'f':                    
                    res = res.clip(min=image.min(),max=image.max())
                processed_images[self.output_names[i]] = res                    
        return processed_images 
        

def getFilterList():
    """Return a list of connected filters in order to test the current filter."""
    import filters_package as imf
    loadf = imf.input_filter.Input_filter()
    current = Resize_filter()    
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