# -*- coding: utf-8 -*-
from filter_base import Filter_base, Parameter, SUCCESS, FAIL
import numpy
import time
i_REAL = "Real"
i_IMAG = "Imag"
o_REAL = "Real"
o_IMAG = "Imag"

class Fourier_filter(Filter_base):
    name = "Fourier transforms"
    def __init__(self):
        Filter_base.__init__(self)        
        self.description = "\
Take the fourier transform or it's inverse of the input image. \
The 'Real' output will always provide the real portion of the selected transform. \
If 'Output complex on 'Imag'' is set to 'Yes', the 'Imag' output will \
output complex numbers (complex datatype) instead of just the imaginary part of the transform. \
Complex matrices as input on either of the inputs will be autodetected, and if nothing \
is connected to the other input, the corresponding part (real or imaginary) of the matrix \
will be copied to the empty input."

        self.setupInputsOutputs([i_REAL,i_IMAG], 
                                 [o_REAL,o_IMAG])
        self.addParam( Parameter(name="Direction of transform", param_type="list",default="Transform", rank=0,
                                 other_content=["Transform","Inverse transform"]))
        self.addParam( Parameter(name="Shift origin", param_type="list",default="No",
                                 other_content=["Yes, shift output", "Yes, shift input", 
                                                "Yes, shift both", "No", ]))
        self.addParam( Parameter(name="Output complex on 'Imag'", param_type="list", default="No",
                                 other_content=["Yes", "No"]))
        self.addParam( Parameter(name="Use complex single input", param_type="list", default="Yes",
                                 other_content=["Yes", "No"]))
        
    def process(self, input_images, connected_outs):
        processed_images = {}
        direction = self.getParamContent("Direction of transform")
        shift = self.getParamContent("Shift origin")
        complex_out = self.getParamContent("Output complex on 'Imag'")
        split_in = self.getParamContent("Use complex single input")
        
        if len(input_images) == 0:
            return FAIL
        if i_REAL in input_images and i_IMAG in input_images:
            input_im = numpy.empty( input_images[i_REAL].real.shape, 'complex128')
            input_im.real = input_images[i_REAL].real
            if input_images[i_IMAG].dtype in ['complex64','complex128']:
                input_im.imag = input_images[i_IMAG].imag
            else:
                input_im.imag = input_images[i_IMAG]
        elif i_REAL in input_images: #Only real input connected
            if split_in == 'Yes':
                input_im = input_images[i_REAL]
            else:
                input_im = input_images[i_REAL].real
        elif i_IMAG in input_images: #Only imaginary input connected
            if split_in == 'Yes':
                if input_images[i_IMAG].dtype in ['complex64','complex128']:
                    input_im = input_images[i_IMAG]
                else:
                    input_im = numpy.zeros( input_images[i_IMAG].shape, 'complex128')
                    input_im.imag = input_images[i_IMAG]
            else:
                input_im = numpy.zeros( input_images[i_IMAG].shape, 'complex128')
                if input_images[i_IMAG].dtype in ['complex64','complex128']:
                    input_im.imag = input_images[i_IMAG].imag
                else:
                    input_im.imag = input_images[i_IMAG]
        else:
            raise Exception("Shouldn't get here.")
        
        image = input_im
        if direction == 'Transform':
            transformed = self.do_fft2(image, shift)
        elif direction == 'Inverse transform':
            transformed = self.do_ifft2(image, shift)
            
        processed_images[o_REAL] = transformed.real.astype('f')
        if complex_out == "Yes":
            processed_images[o_IMAG] = transformed
        else:
            processed_images[o_IMAG] = transformed.imag.astype('f')
        return processed_images
    
    def do_fft2(self, img, shift):
        if shift == "Yes, shift output":
            return numpy.fft.fftshift(numpy.fft.fft2(img))
        elif shift == "Yes, shift input":
            return numpy.fft.fft2(numpy.fft.fftshift(img))
        elif shift == "Yes, shift both":
            return numpy.fft.fftshift(numpy.fft.fft2(numpy.fft.fftshift(img)))
        else:
            return numpy.fft.fft2(img)            
    
    def do_ifft2(self, img, shift):
        if shift == "Yes, shift output":
            return numpy.fft.fftshift(numpy.fft.ifft2(img))
        elif shift == "Yes, shift input":
            return numpy.fft.ifft2(numpy.fft.fftshift(img))
        elif shift == "Yes, shift both":
            return numpy.fft.fftshift(numpy.fft.ifft2(numpy.fft.fftshift(img)))
        else:
            return numpy.fft.ifft2(img)  
        
        
def getFilterList():
    """Return a list of connected filters in order to test the current filter."""
    import filters_package as imf
    loadf = imf.input_filter.Input_filter()
    current = Fourier_filter()    
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