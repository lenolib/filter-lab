# -*- coding: utf-8 -*-
from __future__ import division    
from filter_base import Filter_base, Parameter, SUCCESS, FAIL
import time
import os,sys
from math import sin, cos, pi, sqrt, acos, hypot
import math
import pyopencv as cv
from matplotlib import pyplot
import numpy as np
import Image 
from Tkinter import *
import tkFileDialog
from scipy.misc import fromimage,toimage

N = 24
ax = None

class NoLinesError(Exception):
    def __init__(self): Exception.__init__(self)

class AutoCropFrame_filter(Filter_base):
    name = "Auto crop frame"
    def __init__(self):
        Filter_base.__init__(self)        
        self.description = "Automatically crop and rotate a frame from a 3:2 aspect ratio picture"
        self.i_image = "Input image"
        self.i_lines = "Lines"
        self.o_output = "Output"
        self.setupInputsOutputs([self.i_image, self.i_lines], [self.o_output])

        
        
    def process(self, input_data, connected_outs):
        if len(input_data) < 2:
            return FAIL
        try:
            rel_crop, angle, w,h = self.getCropRot(input_data[self.input_names[0]],
                                              input_data[self.input_names[1]])
            print "In '%s': " %self.name,rel_crop,angle,w,h
        except NoLinesError:
            print "In '%s': No lines" %self.name
            return FAIL

        im = toimage(input_data[self.input_names[0]])
        
        org_w, org_h = im.size
        cropping = tuple([int(i*org_w) for i in rel_crop])
        cg = cropping
        print "In '%s': " %self.name, cg,angle*180/pi, 1.5-cg[2]/cg[3]
        
        im=im.rotate(angle*180/pi, Image.BICUBIC )
        
#        pyplot.plot( (cg[0],cg[0]+cg[2]), (cg[1],cg[1]) )    
#        pyplot.plot( (cg[0],cg[0]), (cg[1], cg[1]+cg[3]) )
#        pyplot.plot( (cg[0]+cg[2],cg[0]+cg[2]), (cg[1],cg[1]+cg[3]) )    
#        pyplot.plot( (cg[0],cg[0]+cg[2]), (cg[1]+cg[3], cg[1]+cg[3]) )
        return {self.output_names[0]: np.asarray(im)[cg[1]:cg[1]+cg[3],cg[0]:cg[0]+cg[2]]}


    def separateANDfilter(self,lines, shape):
        margin = 0.04
        n = 8
        h = shape[0]
        w = shape[1]
        lefts,rights,ups,downs = [],[],[],[]
        for rho,theta in lines:
            if theta > 3*pi/4: theta-=pi
            if abs(rho)<w/n and abs(theta)<margin: lefts.append((rho,theta))
            elif abs(rho)>w-w/n and abs(theta)<margin: rights.append((rho,theta))
            elif abs(rho)<h/n and abs(theta-pi/2)<margin: ups.append((rho,theta))
            elif abs(rho)>h-h/n and abs(theta-pi/2)<margin: downs.append((rho,theta))            
        return [lefts,rights,ups,downs]
    
    #def findSimilar(tlist,dlist, shape):
    #    if not tlist or not dlist:
    #        return tlist + dlist
    #    if len(tlist) > N and len(dlist) < N:
    #        return dlist
    #    if len(tlist) < N and len(dlist) > N:
    #        return tlist        
    #    res = []    
    #    for i in tlist:
    #        for k in dlist:
    #            t_diff = abs(i[1]-k[1])
    #            r_diff = abs(i[0]-k[0])
    #            if t_diff < 0.004 and r_diff<shape[1]/500:                
    #                res.append( i )
    #                print 'found good match'
    #    if not res:
    #        return tlist + dlist
    #    else:
    #        return res
    
    def calcSubset(self,matches):
        res = []
        n = 0
        pallow = 0.02
        
    #    fewest = matches[ sorted([(len(matches[i]),i) for i in range(4)])[0][1] ]
    #    avgt = np.average([g[1] for g in fewest])
    #    print fewest,avgt,'fewest,avgt'
    #    temp = []
    #    for z in range(4):
    #        sidelines = sorted(matches[z],key=lambda tup: tup[1])
    #        if len(sidelines)>N:
    #            ind = min([(abs(e[1]-avgt),ind) for ind,e in enumerate(sidelines)])[1]  
    #            if ind+N/2 > len(sidelines) or ind-N/2 < 0:
    #                if ind-N/2 < 0:
    #                    sidelines = sidelines[0:int(ind+N/2)]
    #                elif ind+N/2 > len(sidelines):
    #                    sidelines = sidelines[int(ind-N/2):-1]
    #            else:
    #                sidelines = sidelines[int(ind-N/2):int(ind+N/2)]                
    #        temp.append(sidelines)
    #    temp = []
    #    for t in matches:
    #        if len(t)>N: 
    #            temp.append([t[i] for i in range(len(t),len(t)//N)])
    #            print 'cut', len(t)-N
    #        else: temp.append(t)
    #        
                
        lefts,rights,ups,downs = matches
        c=np.prod([len(m) for m in matches])
        for left in lefts:
            for up in ups:
    #            if abs(left[1]-up[1]) > pi/2+pallow: pass
                for right in rights:    
    #                if abs(right[1]-up[1]) > pi/2+pallow: pass
                    for down in downs:
    #                    if abs(down[1]-right[1]) > pi/2+pallow: pass
    #                    if abs(down[1]-left[1]) > pi/2+pallow: pass
                        n+=1
#                        print n, c
                        self.abortQuery()
                        vxs = np.array( (crossing(left,up), crossing(up,right), 
                                         crossing(right,down), crossing(down,left) ) )
                        diagA = vxs[0]-vxs[2]
                        diagB = vxs[1]-vxs[3]
                        lengthA = sqrt(diagA.dot(diagA))
                        lengthB = sqrt(diagB.dot(diagB))                   
                        diag_diff = abs( lengthA-lengthB )
                        arangle = acos( diagA.dot(diagB)/lengthA/lengthB )
                        res.append( (abs(arangle-1.9655874464946581), diag_diff, (lengthA+lengthB)/2,
                                     {'left':left,'right':right,'up':up,'down':down, 
                                     'corners':tuple([tuple(item) for item in tuple(vxs)])} ) )
        return res                                    
                        
    def getCropRot(self, res_im, lines):
        sidelines = self.separateANDfilter(lines,res_im.shape)                
        print "In '%s': " %self.name, sidelines
        h,w = res_im.shape[0:2]
    #    weeded = [findSimilar(tsides[i],dsides[i],res_im.shape) for i in range(4)]
        print sidelines
        subset = self.calcSubset(sidelines)    
        if not subset: raise NoLinesError()        
        subset.sort(key=lambda e: e[1])
        newset = [s for s in subset if s[1]/res_im.shape[0]<4/848 and s[0]<1*pi/180]
        
        global ax    
        ax = [s[:3] for s in newset]    
    
        if not newset:
    
            print "Diag difference and AR possibly above limit for image"
            newset = subset
        else:     
            newset.sort(key=lambda e: e[2])    
    #    print [s[0] for s in newset]
        best = newset[0][-1]['corners']
        x = best[0][0]-w/2
        y = h/2-best[0][1]
        angle = newset[0][-1]['left'][1]
        xr,yr = rotateVector(x,y,angle)
        xr += w/2
        yr = h/2 - yr
        rel_crop = (xr/w, yr/w, 
                    math.hypot(best[0][0]-best[1][0], best[0][1]-best[1][1])/w,
                    math.hypot(best[0][0]-best[3][0], best[0][1]-best[3][1])/w)    
        return ( rel_crop, angle, w,h )
    
def rotateVector(x,y,phi):
    return ( cos(phi)*x-sin(phi)*y , sin(phi)*x+cos(phi)*y )

def crossing((r1,t1),(r2,t2), polar=True):
    assert t1 != t2
    y = ( r1*cos(t2)-r2*cos(t1) ) / ( cos(t2)*sin(t1)-sin(t2)*cos(t1) ) 
    x = ( r1*sin(t2)-r2*sin(t1) ) / ( sin(t2)*cos(t1)-cos(t2)*sin(t1) ) 
    return (x,y)

