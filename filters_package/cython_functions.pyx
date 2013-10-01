from __future__ import division
import numpy as np
cimport numpy as np
cdef extern from "math.h": 
    float ceilf(float x)
    float floorf(float x)

ctypedef np.uint8_t np_uint8 
ctypedef np.float32_t np_float


def cyth_create_opponent_images(np.ndarray[np_float, ndim=2] red, 
                                np.ndarray[np_float, ndim=2] green,
                                np.ndarray[np_float, ndim=2] blue,
                                np.ndarray[np_float, ndim=2] RGim, 
                                np.ndarray[np_float, ndim=2] BYim, 
                                np.ndarray[np_float, ndim=2] brightim ):
    cdef Py_ssize_t x, y
    cdef np_float rgb[3]
    cdef unsigned int floor = 0
    for x in xrange(red.shape[0]):
        for y in xrange(red.shape[1]):
            rgb[0], rgb[1], rgb[2] = red[x,y], green[x,y], blue[x,y]

            RGim[x,y] = ( 0.5 - rgb[1]/2 + rgb[0]/2 )
            BYim[x,y] = ( 0.5 - (rgb[0]+rgb[1])/4 + rgb[2]/2 )
            brightim[x,y] = ( (rgb[0]+rgb[1])/2 )



def cyth_remap(np.ndarray[np_float, ndim=2] src_im, 
               double min, 
               double max,
               double curr_min,
               double curr_max):
    cdef Py_ssize_t x, y
    cdef float minval = 0
    cdef float maxval = 0
    if curr_min == curr_max:
        maxval = src_im.max()
        minval = src_im.min()
    else:
        minval = curr_min
        maxval = curr_max 
    cdef float oldlength = maxval-minval
    if oldlength == 0:
        oldlength = 0.000001
    cdef float newlength = max-min    
    cdef float new_div_old = newlength / oldlength  
    cdef np.ndarray[np_float, ndim=2] rmp_im = np.empty_like(src_im)     
    for x in xrange(src_im.shape[0]):
        for y in xrange(src_im.shape[1]):
            rmp_im[x,y] = (src_im[x,y]-minval)*new_div_old + min 
    return rmp_im

def cyth_curve(np.ndarray[np_float, ndim=2] src_im,
               np.ndarray[np_float, ndim=1] curve):
    cdef Py_ssize_t x, y
    cdef float minval = src_im.min()
    cdef float maxval = src_im.max()
    cdef float span = maxval-minval
    if span == 0:
        raise Exception("In 'cyth_curve': Minvalue equals maxvalue")
    cdef int curve_len = len(curve)

    cdef float ind_float
    cdef unsigned int ind_int
    cdef unsigned int low
    cdef unsigned int high
    cdef float ind_diff
    cdef float curve_diff
    cdef np.ndarray[np_float, ndim=2] out_im = np.empty_like(src_im)
    for x in xrange(src_im.shape[0]):
        for y in xrange(src_im.shape[1]): 
            ind_float = (curve_len-1) * ((src_im[x,y] - minval) / span)  #Could perhaps optimize if minval=0 and span=1
            low = <unsigned int> floorf(ind_float)
            high = <unsigned int> ceilf(ind_float)
            ind_diff = ind_float-low
            curve_diff = curve[high]-curve[low]
            out_im[x,y] = curve[low]+curve_diff*ind_diff
    return out_im
    



cdef inline int int_max(int a, int b): return a if a >= b else b
cdef inline int int_min(int a, int b): return a if a <= b else b