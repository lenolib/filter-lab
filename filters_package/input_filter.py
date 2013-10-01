# -*- coding: utf-8 -*-
from filter_base import Filter_base, Parameter, SUCCESS, FAIL, SOURCE_FILTER
import filter_base
import numpy
import time
import os
#import pyopencv as pycv
import cv2
import cProfile

SUPPORTED_IMAGE_FORMATS = ('bmp', 'jpg', 'jpeg', 'png')

class Input_filter(Filter_base):
    """This image filter serves as a general input filter that can handle still pictures,
    video files and web camera streams.
    
    """
    name = 'Load image'
    guiColor = (255,155,55)    
    def __init__(self):
        Filter_base.__init__(self)
        self.description = "\
Load frames from image file, video file or camera. \
The 'original' output type is faster \
than floating point output since no scaling is necessary. \
However, some filters might require floating point input and vice versa.\
If source is monochrome, the output on all channels will be identical"
        self.o_rgb = "RGB"
        self.o_red = "Red"
        self.o_green = "Green"
        self.o_blue = "Blue"
        self.setupInputsOutputs([], [self.o_rgb, self.o_red, self.o_green, self.o_blue])
        directory, tmp = os.path.split( os.path.dirname(__file__).rstrip('/\\') )
        self.addParam( Parameter(name='Input type', param_type='list', default='Image file', 
                                 other_content=['Camera','Video file','Image file','Image sequence'], 
                                 rank=0) )
        self.addParam( Parameter(name='Image file',
                                 description="Select a single image file to be processed repeatedly, \
or select the first image in a sequence to be processed.",
                                 param_type='file', rank=1) )                
        self.setParamContent('Image file', os.path.join(directory,'house.jpg'))
        self.addParam( Parameter(name='Video file', param_type='file', rank=4) )
        self.addParam( Parameter(name='Output type', param_type='list', default='as float, range 0-1',
                                 other_content=['original', 'as float, range 0-1'],
                                 rank=5))
        self.addParam( Parameter(name='Loop video or sequence', param_type='list', 
                                 default='No', other_content=['No','Yes'], rank=7))
        self.addParam( Parameter(name='Camera to use', param_type='list', 
                                 default='0', other_content=[0,1,2,3,4], rank=8))
        self.loaded_image = None
        self.vid_cap = None
        self.cam_cap = None
        self.last_video_path = None
        self.last_image_path = None
        self.camera_to_use = None  
        self.image_sequence = None      
        self.last_sequence_dir = None
        self.next_sequence_ind = 0
        self.frame_counter = 0 
        self.output_names
        self.filtertype = SOURCE_FILTER       
        
    def __getstate__(self):
        """Prepare the filter for pickling (saving) by deleting the capture objects 
        that causes trouble when pickling."""
        pickle_dict = self.__dict__.copy()
        del pickle_dict['vid_cap']
        del pickle_dict['cam_cap']
        return pickle_dict
        
    def __setstate__(self, dict):
        """Restore the capture objects to the filter when unpickling (loading)."""
        super(Input_filter, self).__setstate__(dict)
        self.__dict__ = dict
        self.vid_cap = None
        self.cam_cap = None
        
#    def nextPicRunNotify(self):
#        """Run the input filter and get the next frame from the capture objects, if relevant.
#        This is a special method that gets called by the workerthread for all the input filters
#        in the scene."""
##        if self.getParamContent('Input type') == 'Image file' and self.updated == True:
##            return 'PASS'
#        res = self.run_filter()
#        self.notify_children()
#        return res

    def getAdditionalInfo(self):
        return "Frame number: " + str(self.frame_counter)

    def __del__(self):
        """Before deleting the filter, release the capture objects by resetting their references.
        This does not seem to work at the moment when shutting down the program."""
        self.deleteCaptures()
    
    def restart(self):
        self.deleteCaptures()
    
    def deleteCaptures(self):
        if self.cam_cap is not None: 
            self.cam_cap.release()  #temporary fix
            self.cam_cap = None
        if self.vid_cap is not None:
            self.vid_cap.release() 
            self.vid_cap = None  
        self.last_sequence_dir = None
            
    def process(self, input_images, connected_outs):        
        """Depending on the input type choice the user has made in the GUI, 
        get the appropriate single channel images and return them as a 
        dictionary, described in more detail in the 'Filter_base' documentation.
        """
        if len(connected_outs) == 0:
            return FAIL
        if self.o_rgb in connected_outs: #A bit hackish
            del connected_outs[self.o_rgb]
            connected_outs = self.output_names[1:4]
            rgb_connected = True
        else:
            rgb_connected = False
        processed_images = {}
        choice = self.getParamContent('Input type')
        output_choice = self.getParamContent('Output type')
        camera_to_use = self.getParamContent("Camera to use")
        if self.camera_to_use != camera_to_use and self.cam_cap is not None:
            self.cam_cap.release()
            self.cam_cap = None
            self.camera_to_use = camera_to_use
        if choice == 'Camera':
            processed_images = self.processCamera(connected_outs, output_choice)                
        elif choice == 'Video file':
            processed_images = self.processVideo(connected_outs, output_choice)            
        elif choice == 'Image file':
            processed_images = self.processImage(connected_outs, output_choice)   
        elif choice == 'Image sequence':
            processed_images = self.processSequence(connected_outs, output_choice)             
        
        if processed_images == FAIL: 
            return FAIL
        
        if rgb_connected == True:
            red = processed_images[self.o_red]
            green = processed_images[self.o_green]
            blue = processed_images[self.o_blue]
            processed_images[self.o_rgb] = numpy.dstack((red,green,blue))
#        print "'%s' frame counter: %d" %(self.name,self.frame_counter)
        self.frame_counter += 1
        return processed_images

    def processCamera(self, connected_outs, output_choice): 
        if self.cam_cap is None: 
            self.cam_cap = cv2.VideoCapture(self.camera_to_use)
            if not self.cam_cap.isOpened():
                print "In '%s': Could not connect to any camera (it could help to try again)." %self.name 
                return FAIL
            else:
                self.frame_counter = 0
        ret, frame = self.cam_cap.read()
        if not ret:
            return FAIL
        processed_images = {}    
        if frame.ndim == 3:
            for connection in connected_outs:
                if connection == self.o_red:
                    processed_images[connection] = self.convert_output_type(frame[:,:,2],output_choice)
                if connection == self.o_green:
                    processed_images[connection] = self.convert_output_type(frame[:,:,1],output_choice)
                if connection == self.o_blue:
                    processed_images[connection] = self.convert_output_type(frame[:,:,0],output_choice)
        elif frame.ndim == 2:
            frame = self.convert_output_type(frame,output_choice)
            for connection in connected_outs:
                processed_images[connection] = frame
        else:
            print "In '%s': Video frame has unrecognized dimensions." %self.name
            return FAIL            
        return processed_images
        
    def processVideo(self, connected_outs, output_choice):
        video_path = self.getParamContent('Video file')
        if video_path != self.last_video_path:
            if self.vid_cap is not None:
                self.vid_cap.release()
            self.vid_cap = None
            
        if self.vid_cap is None:
            if video_path is None:
                return FAIL
            self.vid_cap = cv2.VideoCapture(video_path)        
            if not self.vid_cap.isOpened():
                print "In '%s': Could not open video file." %self.name
                return FAIL
            else:
                self.frame_counter = 0
            self.last_video_path = video_path
            
        ret, frame = self.vid_cap.read()
        if not ret:
            if (self.getParamContent('Loop video or sequence') == 'Yes' and
                self.vid_cap.get(cv2.cv.CV_CAP_PROP_POS_AVI_RATIO == 1) ):                
                self.vid_cap.set(cv2.cv.CV_CAP_PROP_POS_AVI_RATIO,0)
                self.frame_counter = 0
                ret, frame = self.vid_cap
                
                if not ret:
        #           print "Could not get frame from video file. Possibly because of reaching the end of the video. Current frame number is ", self.frame_counter
                    return FAIL
            else:
                return FAIL
        processed_images = {}
        if frame.ndim == 3:
            for connection in connected_outs:
                if connection == self.o_red:
                    processed_images[connection] = self.convert_output_type(frame[:,:,2],output_choice)
                if connection == self.o_green:
                    processed_images[connection] = self.convert_output_type(frame[:,:,1],output_choice)
                if connection == self.o_blue:
                    processed_images[connection] = self.convert_output_type(frame[:,:,0],output_choice)
        elif frame.ndim == 2: 
            for connection in connected_outs:
                processed_images[connection] = frame
        else:
            print "In '%s': Video frame has unrecognized dimensions." %self.name
            return FAIL
        return processed_images
     
    def processImage(self, connected_outs, output_choice, image_path=None):
        frame = None
        if self.cam_cap is not None: self.cam_cap = None  #temporary fix
        if self.vid_cap is not None: self.vid_cap = None  #temporary fix
        if image_path is None or not os.path.isfile(image_path):
            image_path = self.getParamContent('Image file')
            if image_path is None or not os.path.isfile(image_path):
                return FAIL
        else:
            pass
        if image_path != self.last_image_path:                              
            frame = filter_base.load_image(image_path)  #Update with new image
        else:
            frame = self.loaded_image
        if frame is None:
            return FAIL
                
        processed_images = {}
        if frame.ndim == 3:
            for connection in connected_outs:
                for i in range(3):
                    if connection == self.output_names[i+1]:
                        processed_images[connection] = self.convert_output_type(frame[:,:,i],output_choice)
        elif frame.ndim == 2:
            frame = self.convert_output_type(frame,output_choice)
            for connection in connected_outs:
                processed_images[connection] = frame
        else:
            print "In '%s': Image frame has unrecognized dimensions." %self.name
            return FAIL                
        self.last_image_path = image_path
        self.loaded_image = frame        
        return processed_images     
    
    def processSequence(self, connected_outs, output_choice):  
        image_path = self.getParamContent('Image file')
        if image_path is None or not os.path.isfile(image_path):    
            return FAIL
        image_dir = os.path.split(image_path)[0]
        if image_dir != self.last_sequence_dir:
            image_dir = os.path.split(image_path)[0]
            dir_contents = [image_dir + '/' + item for item in os.listdir(image_dir)]
            images = filter( _hasImageFormat, dir_contents)
            images.sort()
            self.image_sequence = images
            self.last_sequence_dir = os.path.split(image_path)[0]
            self.next_sequence_ind = 0
        else:
            if self.next_sequence_ind >= len(self.image_sequence):
                if self.getParamContent('Loop video or sequence') == 'Yes':
                    self.frame_counter = 0
                    self.next_sequence_ind = 0
                else:
                    return FAIL
            else:
                pass
        if self.image_sequence:            
            processed_images = self.processImage(connected_outs, output_choice,
                                             image_path = self.image_sequence[self.next_sequence_ind])
            self.next_sequence_ind += 1
            return processed_images
        else:
            return FAIL
#        self.next_sequence_ind = images.index(image_path)
            

    def convert_output_type(self, frame, output_choice):
        """Convert 'frame' to 'output_choice' if necessary and return it."""
        if output_choice == 'as float, range 0-1': 
            if frame.min()<0 or frame.max()>1: return filter_base.make_normfloat32(frame)
            elif frame.dtype == numpy.dtype('f'): return frame
            else: 
                return filter_base.make_normfloat32(frame) #frame.astype('f')
#                return frame.astype('f')
        elif output_choice == 'original': return frame
        else: raise Exception("In '%s': An error (unhandled case) occurred when converting between input and output data types." %self.name)

#def convertType(arr, dtype, scale=1):    
#    arrmat = pycv.asMat(arr)   
#    if dtype == 'uint8': cvtype = pycv.CV_8U    
#    elif dtype == 'float32': cvtype = pycv.CV_32F    
#    dst = pycv.Mat(*arr.shape+(cvtype,))
#    pycv.Mat.convertTo(arrmat,dst,cvtype,scale)
#    return dst.ndarray                    
    

def _hasImageFormat(s):
    if os.path.isfile(s):        
        for format in SUPPORTED_IMAGE_FORMATS:
            if s.endswith("."+format):
                return True
    return False
        
