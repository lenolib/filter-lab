# -*- coding: utf-8 -*-

from __future__ import division
from filter_base import Filter_base, Parameter
import filter_base
from math import pi,sqrt,ceil,cos,sin,atan,exp
#from scipy.signal import *
from scipy import fftpack
import numpy
import pyopencv as pycv
import matplotlib as mpl


class Gabor_filter(Filter_base):
    name = 'Gabor'
    def __init__(self):
        Filter_base.__init__(self)
        self.description = "\
Will convolve the input image with a specified Gabor kernel. \
Please note that the kernel size at the moment is fixed at 21 pixels. \
Feel free to edit the code to add an autoadjusted kernel size for \
improved performance. \
"
        self.i_input = 'Input'
        self.o_gabor = 'Gabor filtered'
        self.setupInputsOutputs([self.i_input], [self.o_gabor])
        self.addParam( Parameter(name="Kernel",param_type="display",rank=0))
        self.addParam( Parameter(name='Frequency (cycles / 100 pixels)', param_type='variable',
                                 default=10, minimum=2, maximum=50, rank=1) )
        self.addParam( Parameter(name='Kernel angle (degrees)', param_type='variable',
                                 default=45.0, minimum=0.0, maximum=180, rank=2) )
        self.addParam( Parameter(name='Scale (pixels)', param_type='variable',
                                 default=3, minimum=1, maximum=20, rank=3) )
        self.addParam( Parameter(name='Aspect ratio', param_type='variable',
                                 default=0.8, minimum=0, maximum=2, rank=4) )
        self.addParam( Parameter(name='Phase (degrees)', param_type='variable',
                                 default=0, minimum=-180, maximum=180, rank=1.5) )
        self.addParam( Parameter(name="Output only positive pixels", param_type="list", default="No",
                                 other_content=["No","Yes"], rank=6))
        self.addParam( Parameter(name='Field of view (degrees)', param_type='variable',
                                 default=45, minimum=2, maximum=180, rank=5,
                                 description="[Does nothing. Not yet implemented.]") )
        self.last_kernel = None
        self.last_params = None
        self.kernel_fig = None
        self.kernel_plt = None
        self.kernelSize = None

    def getAdditionalInfo(self):
        return "Kernel size (pixels): " + str(self.kernelSize)

    def getParam_dict(self):
        dict_ = {"F":self.getParamContent('Frequency (cycles / 100 pixels)')/100,
                "deg_angle":self.getParamContent('Kernel angle (degrees)'),
                "deg_omega":self.getParamContent('Kernel angle (degrees)'),
                "ainv":self.getParamContent('Scale (pixels)')*self.getParamContent('Aspect ratio'),
                "binv":self.getParamContent('Scale (pixels)')/self.getParamContent('Aspect ratio'),
                "Phase":self.getParamContent('Phase (degrees)') }
        return dict_

    def processParams(self):
        param_dict = self.getParam_dict()
        if isEqualDicts(param_dict,self.last_params): return

        kernel = self.createKernel(**(param_dict))
        self.last_params=param_dict
        self.last_kernel = kernel
        self.abortQuery()
        kernel = filter_base.make_uint8(kernel)
        kernel_rz = filter_base.resize(kernel, percent=800)
#        if self.kernel_fig is None:
#            self.kernel_fig = mpl.pyplot.figure(figsize=(3, 2), dpi=100)
#            self.kernel_plt = self.kernel_fig.add_subplot(111)
#        self.kernel_fig.clear()
#        self.kernel_plt.imshow(kernel, cmap=mpl.cm.gray)

        self.setParamContent("Kernel", kernel_rz, emitSignal=True)

    def process(self, input_images, connected_outs):
        self.processParams()
        if len(input_images)>0:
            gabor_im = filter2d_cv(input_images['Input'], self.last_kernel)
            if self.getParamContent("Output only positive pixels") == "Yes":
                return {self.o_gabor : gabor_im.clip(min=0, max=gabor_im.max())}
            else:
                return {self.o_gabor : gabor_im}

    def createKernel(self, K=None, ainv=None, binv=None, kernelSize=None, deg_angle=0,
                      fxinv=None, fyinv=None, F=None, deg_omega=None, sigma=None,
                      Phase=None, mode='spatial' ):
        """Create a gabor kernel based on the supplied parameters. 'mode' can be
        either 'spatial', which is normal, or 'fourier', in which case the kernel
        will be returned fourier transformed.

	The calculations are based on the following pdf, "Tutorial on Gabor Filters" by
	Javier R. Movellan:
	http://mplab.ucsd.edu/wordpress/tutorials/gabor.pdf"""

        def rot(u,u0,v,v0,angle):
            urot = (u-u0)*cos(angle) + (v-v0)*sin(angle)
            vrot = -(v-v0)*cos(angle) + (u-u0)*sin(angle)
            return urot, vrot

        if fxinv is not None and fyinv is not None:
            F = sqrt(1/fxinv/fxinv + 1/fyinv/fyinv)
            omega = atan(fxinv/fyinv) #intentional wrong order because of original inverted values
        elif F is not None and deg_omega is not None:
            fxinv = 1/F/cos(deg_omega * pi/180.0 + 0.01)
            fyinv = 1/F/sin(deg_omega * pi/180.0 + 0.01)
        else:
            raise Exception("incorrect parameters")
        if sigma is not None and ainv is None and binv is None:
            ainv = sigma
            binv = sigma
        elif sigma is not None and (ainv is not None or binv is not None):
            raise Exception("incorrect parameters. Call function with either a/b-inv values or sigma")

        angle = deg_angle * pi/180
        if K is None:
            K=5
        a,b,fx,fy = (1/ainv, 1/binv, 1/fxinv, 1/fyinv)
        fxrot = fx*cos(angle) + fy*sin(angle)
        fyrot = -fx*sin(angle) + fy*cos(angle)
        correction = exp( -pi*(fxrot*fxrot/a/a + fyrot*fyrot/b/b) )
        if kernelSize is None:
            #Should be extended to adapt (optimize) the size of the kernel to the other parameters.
            kernelSize = 20.0
            self.kernelSize = kernelSize
        y = numpy.kron( numpy.ones((kernelSize+1,1)), numpy.arange(-kernelSize/2,kernelSize/2+1,1) ).astype('f')
        x = y.transpose()
        xrot, yrot = rot(x,0,y,0,angle)
        urot, vrot = rot(x,fx,y,fy,angle)
        gaussian = K * numpy.exp( -pi*(a*a*xrot*xrot + b*b*yrot*yrot) )
        gabor_r = numpy.cos( 2*pi*(fx*x + fy*y) + Phase*pi/180 )
    #   gabor_i = sin( 2*pi*(fx*x + fy*y) + P )
        kernel = gaussian*(gabor_r-correction)
    #   kernel_fourier[i][j] = K/a/b*(exp( -pi*(urot*urot/a/a + vrot*vrot/b/b) ) + correction *
    #                                 exp( -pi*(xrot*xrot/a/a + yrot*yrot/b/b) ))
        if mode == 'spatial':
            return kernel
        if mode == 'fourier':
            kernel_fourier = numpy.asarray(fftpack.fft2(kernel), 'f')
            return kernel_fourier

def filter2d_cv(src, kernel, anchor = (-1,-1) ):
    if kernel.flags['C_CONTIGUOUS'] == False:
        kernel = numpy.ascontiguousarray(kernel, 'f')
    if src.flags['C_CONTIGUOUS'] == False:
        src = numpy.ascontiguousarray(src)
    dst = numpy.empty_like(src)
    pycv.filter2D( pycv.asMat(src),
                   pycv.asMat(dst),
                   -1,
                   pycv.asMat(kernel),
                   pycv.asPoint(numpy.asarray(anchor)),
                   borderType = pycv.BORDER_CONSTANT )
    return dst


def isEqualDicts(d1,d2):
    """Check if d1 is identical to d2, return True or False."""
    if not isinstance(d1,dict) or not isinstance(d2,dict): return False
    for key in d1.keys():
        if key not in d2: return False
        elif d2[key]!=d1[key]: return False
    return True


def getFilterList():
    """Return a list of connected filters in order to test the current filter."""
    import filters_package as imf
    loadf = imf.input_filter.Input_filter()
    current = Gabor_filter()
    dispf = imf.display_filter.Display_filter()
    dispf.setName("Display - %s" %current.name)
    loadf.setName("Load - %s" %current.name)
    imf.filter_base.connect_filters(loadf,current,[loadf.output_names[1]],[current.input_names[0]])
    imf.filter_base.connect_filters(current, dispf, [current.output_names[0]], [dispf.input_names[0]])
    return [loadf,current,dispf]


if __name__ == "__main__":
    import os,sys
    flabfile = os.path.join(os.path.split(os.path.split(__file__)[0])[0],'filter_lab.py')
    os.system(sys.executable+" \""+flabfile+"\" \"%s\"" %__file__)