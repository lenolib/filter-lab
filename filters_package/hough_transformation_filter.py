# -*- coding: utf-8 -*-
from filter_base import Filter_base, Parameter, SUCCESS, FAIL, getRandColor
import numpy
import pyopencv as pycv
import random
import math

class Hough_transformation_filter(Filter_base):
    name = 'Hough line detector'
    def __init__(self):
        Filter_base.__init__(self)
        self.setupInputsOutputs(['Input'], 
                                 ['RGB Overlay','Lines data'])
        self.description = "Use the Hough transform to detect lines from an edge detected image."
        self.addParam( Parameter(name="Type of Hough transform", param_type='list',
                                 default="Standard", other_content=["Standard","Probabilistic"], rank=-1) )
        self.addParam( Parameter(name="Distance resolution", param_type='variable',
                                 default=1, minimum=1, maximum=50, rank=1) )
        self.addParam( Parameter(name="Angle resolution (degrees)", param_type='variable',
                                 default=150, minimum=1, maximum=600, rank=2) )
        self.addParam( Parameter(name="Accumulator threshold", param_type='variable',
                                 default=150, minimum=0, maximum=600, rank=3) )
        self.addParam( Parameter(name="Minimum length", param_type='variable',
                                 default=50, minimum=0, maximum=600, rank=4) )
        self.addParam( Parameter(name="Maximum gap", param_type='variable',
                                 default=0, minimum=0, maximum=100, rank=5) )
        self.addParam( Parameter(name="draw # lines", param_type='variable',
                                 default=100, minimum=0, maximum=1000, rank=5) )
        

    def process(self, input_images, connected_outs):
        if len(input_images) == 0:
            return FAIL     
        src = input_images['Input']   
        dist_res = int( self.getParamContent('Distance resolution') )
        angle_res = int( self.getParamContent('Angle resolution (degrees)') )
        acc_thresh = int( self.getParamContent('Accumulator threshold') )
        min_length = int( self.getParamContent('Minimum length') )
        max_gap = int( self.getParamContent('Maximum gap') )
        choice = self.getParamContent("Type of Hough transform")
        if src.ndim > 2:
            print "In '%s': The hough transform takes a binary image (or 8-bit) as input." %self.name
            return FAIL
        color_dst = numpy.empty( (src.shape[0], src.shape[1], 3),dtype='uint8' )
        pycv.cvtColor( pycv.asMat(src), pycv.asMat(color_dst), pycv.CV_GRAY2BGR )

        if choice == "Standard":
            lines = pycv.HoughLines( pycv.asMat(src), dist_res, pycv.CV_PI/angle_res, acc_thresh )
            margin = 0.04
            n=8
            pi = math.pi
            h,w = src.shape[0:2]
            for i in range(min(len(lines), int(self.getParamContent("draw # lines")))):
                l = lines[i]
                rho = l[0]
                theta = l[1]
                if theta > 3*pi/4: theta-=pi
                if abs(rho)<w/n and abs(theta)<margin: pass
                elif abs(rho)>w-w/n and abs(theta)<margin: pass
                elif abs(rho)<h/n and abs(theta-pi/2)<margin: pass
                elif abs(rho)>h-h/n and abs(theta-pi/2)<margin: pass
                else:
                    continue         
                a = math.cos(theta)
                b = math.sin(theta)
                x0 = a*rho 
                y0 = b*rho
                pt1 = pycv.Point( int(round(x0 + 2000*(-b))), int(round(y0 + 2000*(a))) )
                pt2 = pycv.Point( int(round(x0 - 2000*(-b))), int(round(y0 - 2000*(a))) ) 
                pycv.line( pycv.asMat(color_dst), pt1, pt2, pycv.CV_RGB(random.randint(0,255),
                                                            random.randint(0,255),
                                                            random.randint(0,255)), 2, 8 )
    
        else:
            lines = pycv.HoughLinesP( pycv.asMat(src), dist_res, 
                                    pycv.CV_PI/angle_res, acc_thresh, min_length, max_gap )
            for l in lines:
                pycv.line( pycv.asMat(color_dst), pycv.Point(int(l[0]), int(l[1])), 
                           pycv.Point(int(l[2]), int(l[3])), 
                           pycv.CV_RGB(*getRandColor()), 2, 8 )    
        self.lines = [(item[0],item[1]) for item in lines]        
        return {self.output_names[0] : color_dst, self.output_names[1]:self.lines}
    