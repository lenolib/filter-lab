# -*- coding:utf-8 -*-
#This python code creates a list of connected filter instances.


import os,sys
sys.path.append(os.path.split(os.path.split(__file__)[0])[0])
import filters_package
from filters_package.filter_base import connect_filters


def getFilterList():
    Input_filter_Load___Color_blindness = filters_package.input_filter.Input_filter()
    Input_filter_Load___Color_blindness.setName("""Load - Color blindness""")
    Input_filter_Load___Color_blindness.setDescription("""Load frames from image file, video file or camera. The 'original' output type is faster than floating point output since no scaling is necessary. However, some filters might require floating point input and vice versa.If source is monochrome, the output on all channels will be identical""")
    Input_filter_Load___Color_blindness.setParamContent("""Output type""","""original""")
    Input_filter_Load___Color_blindness.setParamContent("""Input type""","""Image file""")
    Input_filter_Load___Color_blindness.setParamContent("""Camera to use""","""0""")
    Input_filter_Load___Color_blindness.setParamContent("""Image file""","""/home/lennart/filter-lab/house.jpg""")
    Input_filter_Load___Color_blindness.setParamContent("""Loop video or sequence""","""No""")
    Input_filter_Load___Color_blindness.setParamContent("""Video file""","""None""")
    Display_filter_Display___Blend_together = filters_package.display_filter.Display_filter()
    Display_filter_Display___Blend_together.setName("""Display - Blend together""")
    Display_filter_Display___Blend_together.setDescription("""Display a image in the viewer window. If the input images' pixels are not all in the [0,1] range, they will get compressed into this range by the 'remap'-function. 
If something is connected to the 'B&W or RGB' input, all other inputs will be ignored.""")
    Display_filter_Display___Blend_together.setParamContent("""Resize (%)""",100)
    Display_filter_Display___Blend_together.getParam("""Resize (%)""").min = 0
    Display_filter_Display___Blend_together.getParam("""Resize (%)""").max = 200
    Display_filter_Display___Blend_together.setParamContent("""Resize method""","""Bilinear""")
    Input_filter_Load___Code_input = filters_package.input_filter.Input_filter()
    Input_filter_Load___Code_input.setName("""Load - Code input""")
    Input_filter_Load___Code_input.setDescription("""Load frames from image file, video file or camera. The 'original' output type is faster than floating point output since no scaling is necessary. However, some filters might require floating point input and vice versa.If source is monochrome, the output on all channels will be identical""")
    Input_filter_Load___Code_input.setParamContent("""Output type""","""original""")
    Input_filter_Load___Code_input.setParamContent("""Input type""","""Image file""")
    Input_filter_Load___Code_input.setParamContent("""Camera to use""","""0""")
    Input_filter_Load___Code_input.setParamContent("""Image file""","""/home/lennart/filter-lab/house.jpg""")
    Input_filter_Load___Code_input.setParamContent("""Loop video or sequence""","""No""")
    Input_filter_Load___Code_input.setParamContent("""Video file""","""None""")
    Display_filter_Display___Remap_pixel_range = filters_package.display_filter.Display_filter()
    Display_filter_Display___Remap_pixel_range.setName("""Display - Remap pixel range""")
    Display_filter_Display___Remap_pixel_range.setDescription("""Display a image in the viewer window. If the input images' pixels are not all in the [0,1] range, they will get compressed into this range by the 'remap'-function. 
If something is connected to the 'B&W or RGB' input, all other inputs will be ignored.""")
    Display_filter_Display___Remap_pixel_range.setParamContent("""Resize (%)""",100)
    Display_filter_Display___Remap_pixel_range.getParam("""Resize (%)""").min = 0
    Display_filter_Display___Remap_pixel_range.getParam("""Resize (%)""").max = 200
    Display_filter_Display___Remap_pixel_range.setParamContent("""Resize method""","""Bilinear""")
    Input_filter_Load___Gabor = filters_package.input_filter.Input_filter()
    Input_filter_Load___Gabor.setName("""Load - Gabor""")
    Input_filter_Load___Gabor.setDescription("""Load frames from image file, video file or camera. The 'original' output type is faster than floating point output since no scaling is necessary. However, some filters might require floating point input and vice versa.If source is monochrome, the output on all channels will be identical""")
    Input_filter_Load___Gabor.setParamContent("""Output type""","""original""")
    Input_filter_Load___Gabor.setParamContent("""Input type""","""Image file""")
    Input_filter_Load___Gabor.setParamContent("""Camera to use""","""0""")
    Input_filter_Load___Gabor.setParamContent("""Image file""","""/home/lennart/filter-lab/house.jpg""")
    Input_filter_Load___Gabor.setParamContent("""Loop video or sequence""","""No""")
    Input_filter_Load___Gabor.setParamContent("""Video file""","""None""")
    Adaptation_filter_Adaptation = filters_package.adaptation_filter.Adaptation_filter()
    Adaptation_filter_Adaptation.setName("""Adaptation""")
    Adaptation_filter_Adaptation.setDescription("""""")
    Adaptation_filter_Adaptation.setParamContent("""Sensitivity reduction""",1)
    Adaptation_filter_Adaptation.getParam("""Sensitivity reduction""").min = 0
    Adaptation_filter_Adaptation.getParam("""Sensitivity reduction""").max = 1
    Canny_filter_Edge_detection__Canny_ = filters_package.canny_filter.Canny_filter()
    Canny_filter_Edge_detection__Canny_.setName("""Edge detection (Canny)""")
    Canny_filter_Edge_detection__Canny_.setDescription("""Use the Canny algorithm to detect edges. Input must be 8-bit.""")
    Canny_filter_Edge_detection__Canny_.setParamContent("""First threshold""",50)
    Canny_filter_Edge_detection__Canny_.getParam("""First threshold""").min = 0
    Canny_filter_Edge_detection__Canny_.getParam("""First threshold""").max = 600
    Canny_filter_Edge_detection__Canny_.setParamContent("""Second threshold""",150)
    Canny_filter_Edge_detection__Canny_.getParam("""Second threshold""").min = 0
    Canny_filter_Edge_detection__Canny_.getParam("""Second threshold""").max = 600
    Canny_filter_Edge_detection__Canny_.setParamContent("""Aperture size""","""3""")
    Display_filter_Display___Time_lag = filters_package.display_filter.Display_filter()
    Display_filter_Display___Time_lag.setName("""Display - Time lag""")
    Display_filter_Display___Time_lag.setDescription("""Display a image in the viewer window. If the input images' pixels are not all in the [0,1] range, they will get compressed into this range by the 'remap'-function. 
If something is connected to the 'B&W or RGB' input, all other inputs will be ignored.""")
    Display_filter_Display___Time_lag.setParamContent("""Resize (%)""",100)
    Display_filter_Display___Time_lag.getParam("""Resize (%)""").min = 0
    Display_filter_Display___Time_lag.getParam("""Resize (%)""").max = 200
    Display_filter_Display___Time_lag.setParamContent("""Resize method""","""Bilinear""")
    Input_filter_Load___Opponent_colors = filters_package.input_filter.Input_filter()
    Input_filter_Load___Opponent_colors.setName("""Load - Opponent colors""")
    Input_filter_Load___Opponent_colors.setDescription("""Load frames from image file, video file or camera. The 'original' output type is faster than floating point output since no scaling is necessary. However, some filters might require floating point input and vice versa.If source is monochrome, the output on all channels will be identical""")
    Input_filter_Load___Opponent_colors.setParamContent("""Output type""","""original""")
    Input_filter_Load___Opponent_colors.setParamContent("""Input type""","""Image file""")
    Input_filter_Load___Opponent_colors.setParamContent("""Camera to use""","""0""")
    Input_filter_Load___Opponent_colors.setParamContent("""Image file""","""/home/lennart/filter-lab/house.jpg""")
    Input_filter_Load___Opponent_colors.setParamContent("""Loop video or sequence""","""No""")
    Input_filter_Load___Opponent_colors.setParamContent("""Video file""","""None""")
    Curve_filter_Curve = filters_package.curve_filter.Curve_filter()
    Curve_filter_Curve.setName("""Curve""")
    Curve_filter_Curve.setDescription("""Apply an intensity transformation curve to the input image, by mapping old curve values to new ones via a look-up table created by linear interpolation.""")
    Curve_filter_Curve.setParamContent("""s variable""",0.1)
    Curve_filter_Curve.getParam("""s variable""").min = 0
    Curve_filter_Curve.getParam("""s variable""").max = 1
    Curve_filter_Curve.setParamContent("""Function/points input""","""k = (t-s)/(d-c)
m = -k*c+s
intervals = [
    [(vmin,c),  s ],
    [(c,d),     k*x+m ],
    [(d,vmax),  t ] ]
""")
    Curve_filter_Curve.setParamContent("""d variable""",0.75)
    Curve_filter_Curve.getParam("""d variable""").min = 0
    Curve_filter_Curve.getParam("""d variable""").max = 1
    Curve_filter_Curve.setParamContent("""Interpolation resolution""",256)
    Curve_filter_Curve.getParam("""Interpolation resolution""").min = 4
    Curve_filter_Curve.getParam("""Interpolation resolution""").max = 1024
    Curve_filter_Curve.setParamContent("""Min pixel value""",0)
    Curve_filter_Curve.getParam("""Min pixel value""").min = 0
    Curve_filter_Curve.getParam("""Min pixel value""").max = 1
    Curve_filter_Curve.setParamContent("""Max pixel value""",1)
    Curve_filter_Curve.getParam("""Max pixel value""").min = 0
    Curve_filter_Curve.getParam("""Max pixel value""").max = 1
    Curve_filter_Curve.setParamContent("""c variable""",0.25)
    Curve_filter_Curve.getParam("""c variable""").min = 0
    Curve_filter_Curve.getParam("""c variable""").max = 1
    Curve_filter_Curve.setParamContent("""t variable""",0.9)
    Curve_filter_Curve.getParam("""t variable""").min = 0
    Curve_filter_Curve.getParam("""t variable""").max = 1
    Input_filter_Load___Clip = filters_package.input_filter.Input_filter()
    Input_filter_Load___Clip.setName("""Load - Clip""")
    Input_filter_Load___Clip.setDescription("""Load frames from image file, video file or camera. The 'original' output type is faster than floating point output since no scaling is necessary. However, some filters might require floating point input and vice versa.If source is monochrome, the output on all channels will be identical""")
    Input_filter_Load___Clip.setParamContent("""Output type""","""original""")
    Input_filter_Load___Clip.setParamContent("""Input type""","""Image file""")
    Input_filter_Load___Clip.setParamContent("""Camera to use""","""0""")
    Input_filter_Load___Clip.setParamContent("""Image file""","""/home/lennart/filter-lab/house.jpg""")
    Input_filter_Load___Clip.setParamContent("""Loop video or sequence""","""No""")
    Input_filter_Load___Clip.setParamContent("""Video file""","""None""")
    Input_filter_Load___Adaptation = filters_package.input_filter.Input_filter()
    Input_filter_Load___Adaptation.setName("""Load - Adaptation""")
    Input_filter_Load___Adaptation.setDescription("""Load frames from image file, video file or camera. The 'original' output type is faster than floating point output since no scaling is necessary. However, some filters might require floating point input and vice versa.If source is monochrome, the output on all channels will be identical""")
    Input_filter_Load___Adaptation.setParamContent("""Output type""","""original""")
    Input_filter_Load___Adaptation.setParamContent("""Input type""","""Image file""")
    Input_filter_Load___Adaptation.setParamContent("""Camera to use""","""0""")
    Input_filter_Load___Adaptation.setParamContent("""Image file""","""/home/lennart/filter-lab/house.jpg""")
    Input_filter_Load___Adaptation.setParamContent("""Loop video or sequence""","""No""")
    Input_filter_Load___Adaptation.setParamContent("""Video file""","""None""")
    Input_filter_Load___Smooth = filters_package.input_filter.Input_filter()
    Input_filter_Load___Smooth.setName("""Load - Smooth""")
    Input_filter_Load___Smooth.setDescription("""Load frames from image file, video file or camera. The 'original' output type is faster than floating point output since no scaling is necessary. However, some filters might require floating point input and vice versa.If source is monochrome, the output on all channels will be identical""")
    Input_filter_Load___Smooth.setParamContent("""Output type""","""original""")
    Input_filter_Load___Smooth.setParamContent("""Input type""","""Image file""")
    Input_filter_Load___Smooth.setParamContent("""Camera to use""","""0""")
    Input_filter_Load___Smooth.setParamContent("""Image file""","""/home/lennart/filter-lab/house.jpg""")
    Input_filter_Load___Smooth.setParamContent("""Loop video or sequence""","""No""")
    Input_filter_Load___Smooth.setParamContent("""Video file""","""None""")
    Input_filter_Load___Fourier_transforms = filters_package.input_filter.Input_filter()
    Input_filter_Load___Fourier_transforms.setName("""Load - Fourier transforms""")
    Input_filter_Load___Fourier_transforms.setDescription("""Load frames from image file, video file or camera. The 'original' output type is faster than floating point output since no scaling is necessary. However, some filters might require floating point input and vice versa.If source is monochrome, the output on all channels will be identical""")
    Input_filter_Load___Fourier_transforms.setParamContent("""Output type""","""original""")
    Input_filter_Load___Fourier_transforms.setParamContent("""Input type""","""Image file""")
    Input_filter_Load___Fourier_transforms.setParamContent("""Camera to use""","""0""")
    Input_filter_Load___Fourier_transforms.setParamContent("""Image file""","""/home/lennart/filter-lab/house.jpg""")
    Input_filter_Load___Fourier_transforms.setParamContent("""Loop video or sequence""","""No""")
    Input_filter_Load___Fourier_transforms.setParamContent("""Video file""","""None""")
    Display_filter_Display___Edge_detection__Canny_ = filters_package.display_filter.Display_filter()
    Display_filter_Display___Edge_detection__Canny_.setName("""Display - Edge detection (Canny)""")
    Display_filter_Display___Edge_detection__Canny_.setDescription("""Display a image in the viewer window. If the input images' pixels are not all in the [0,1] range, they will get compressed into this range by the 'remap'-function. 
If something is connected to the 'B&W or RGB' input, all other inputs will be ignored.""")
    Display_filter_Display___Edge_detection__Canny_.setParamContent("""Resize (%)""",100)
    Display_filter_Display___Edge_detection__Canny_.getParam("""Resize (%)""").min = 0
    Display_filter_Display___Edge_detection__Canny_.getParam("""Resize (%)""").max = 200
    Display_filter_Display___Edge_detection__Canny_.setParamContent("""Resize method""","""Bilinear""")
    Input_filter_Load___Histogram = filters_package.input_filter.Input_filter()
    Input_filter_Load___Histogram.setName("""Load - Histogram""")
    Input_filter_Load___Histogram.setDescription("""Load frames from image file, video file or camera. The 'original' output type is faster than floating point output since no scaling is necessary. However, some filters might require floating point input and vice versa.If source is monochrome, the output on all channels will be identical""")
    Input_filter_Load___Histogram.setParamContent("""Output type""","""original""")
    Input_filter_Load___Histogram.setParamContent("""Input type""","""Image file""")
    Input_filter_Load___Histogram.setParamContent("""Camera to use""","""0""")
    Input_filter_Load___Histogram.setParamContent("""Image file""","""/home/lennart/filter-lab/house.jpg""")
    Input_filter_Load___Histogram.setParamContent("""Loop video or sequence""","""No""")
    Input_filter_Load___Histogram.setParamContent("""Video file""","""None""")
    Split_filter_Split_image = filters_package.split_filter.Split_filter()
    Split_filter_Split_image.setName("""Split image""")
    Split_filter_Split_image.setDescription("""Split the input image into four new images.""")
    Split_filter_Split_image.setParamContent("""Split vertically at:""",0)
    Split_filter_Split_image.getParam("""Split vertically at:""").min = 0
    Split_filter_Split_image.getParam("""Split vertically at:""").max = 2048
    Split_filter_Split_image.setParamContent("""Split horizontally at:""",0)
    Split_filter_Split_image.getParam("""Split horizontally at:""").min = 0
    Split_filter_Split_image.getParam("""Split horizontally at:""").max = 2048
    Input_filter_Load___Resize = filters_package.input_filter.Input_filter()
    Input_filter_Load___Resize.setName("""Load - Resize""")
    Input_filter_Load___Resize.setDescription("""Load frames from image file, video file or camera. The 'original' output type is faster than floating point output since no scaling is necessary. However, some filters might require floating point input and vice versa.If source is monochrome, the output on all channels will be identical""")
    Input_filter_Load___Resize.setParamContent("""Output type""","""original""")
    Input_filter_Load___Resize.setParamContent("""Input type""","""Image file""")
    Input_filter_Load___Resize.setParamContent("""Camera to use""","""0""")
    Input_filter_Load___Resize.setParamContent("""Image file""","""/home/lennart/filter-lab/house.jpg""")
    Input_filter_Load___Resize.setParamContent("""Loop video or sequence""","""No""")
    Input_filter_Load___Resize.setParamContent("""Video file""","""None""")
    Blend_filter_Blend_together = filters_package.blend_filter.Blend_filter()
    Blend_filter_Blend_together.setName("""Blend together""")
    Blend_filter_Blend_together.setDescription("""Blend several pictures together by simple weighting.""")
    Blend_filter_Blend_together.setParamContent("""Input 2 weight""",1)
    Blend_filter_Blend_together.getParam("""Input 2 weight""").min = 0
    Blend_filter_Blend_together.getParam("""Input 2 weight""").max = 5
    Blend_filter_Blend_together.setParamContent("""Input 1 weight""",1)
    Blend_filter_Blend_together.getParam("""Input 1 weight""").min = 0
    Blend_filter_Blend_together.getParam("""Input 1 weight""").max = 5
    Blend_filter_Blend_together.setParamContent("""Input 4 weight""",1)
    Blend_filter_Blend_together.getParam("""Input 4 weight""").min = 0
    Blend_filter_Blend_together.getParam("""Input 4 weight""").max = 5
    Blend_filter_Blend_together.setParamContent("""Input 3 weight""",1)
    Blend_filter_Blend_together.getParam("""Input 3 weight""").min = 0
    Blend_filter_Blend_together.getParam("""Input 3 weight""").max = 5
    Histogram_filter_Histogram = filters_package.histogram_filter.Histogram_filter()
    Histogram_filter_Histogram.setName("""Histogram""")
    Histogram_filter_Histogram.setDescription("""Produce a histogram of the input image""")
    Histogram_filter_Histogram.setParamContent("""Normalize""","""Yes""")
    Histogram_filter_Histogram.setParamContent("""Display width (pixels)""",400)
    Histogram_filter_Histogram.getParam("""Display width (pixels)""").min = 50
    Histogram_filter_Histogram.getParam("""Display width (pixels)""").max = 600
    Histogram_filter_Histogram.setParamContent("""Log""","""No""")
    Histogram_filter_Histogram.setParamContent("""# of bins""",255)
    Histogram_filter_Histogram.getParam("""# of bins""").min = 2
    Histogram_filter_Histogram.getParam("""# of bins""").max = 255
    Histogram_filter_Histogram.setParamContent("""Display height (pixels)""",200)
    Histogram_filter_Histogram.getParam("""Display height (pixels)""").min = 50
    Histogram_filter_Histogram.getParam("""Display height (pixels)""").max = 600
    Histogram_filter_Histogram.setParamContent("""Plot histogram""","""Yes""")
    Display_filter_Display___Opponent_colors = filters_package.display_filter.Display_filter()
    Display_filter_Display___Opponent_colors.setName("""Display - Opponent colors""")
    Display_filter_Display___Opponent_colors.setDescription("""Display a image in the viewer window. If the input images' pixels are not all in the [0,1] range, they will get compressed into this range by the 'remap'-function. 
If something is connected to the 'B&W or RGB' input, all other inputs will be ignored.""")
    Display_filter_Display___Opponent_colors.setParamContent("""Resize (%)""",100)
    Display_filter_Display___Opponent_colors.getParam("""Resize (%)""").min = 0
    Display_filter_Display___Opponent_colors.getParam("""Resize (%)""").max = 200
    Display_filter_Display___Opponent_colors.setParamContent("""Resize method""","""Bilinear""")
    Input_filter_Load___Colorspace_transforms = filters_package.input_filter.Input_filter()
    Input_filter_Load___Colorspace_transforms.setName("""Load - Colorspace transforms""")
    Input_filter_Load___Colorspace_transforms.setDescription("""Load frames from image file, video file or camera. The 'original' output type is faster than floating point output since no scaling is necessary. However, some filters might require floating point input and vice versa.If source is monochrome, the output on all channels will be identical""")
    Input_filter_Load___Colorspace_transforms.setParamContent("""Output type""","""original""")
    Input_filter_Load___Colorspace_transforms.setParamContent("""Input type""","""Image file""")
    Input_filter_Load___Colorspace_transforms.setParamContent("""Camera to use""","""0""")
    Input_filter_Load___Colorspace_transforms.setParamContent("""Image file""","""/home/lennart/filter-lab/house.jpg""")
    Input_filter_Load___Colorspace_transforms.setParamContent("""Loop video or sequence""","""No""")
    Input_filter_Load___Colorspace_transforms.setParamContent("""Video file""","""None""")
    Display_filter_Display___Colorspace_transforms = filters_package.display_filter.Display_filter()
    Display_filter_Display___Colorspace_transforms.setName("""Display - Colorspace transforms""")
    Display_filter_Display___Colorspace_transforms.setDescription("""Display a image in the viewer window. If the input images' pixels are not all in the [0,1] range, they will get compressed into this range by the 'remap'-function. 
If something is connected to the 'B&W or RGB' input, all other inputs will be ignored.""")
    Display_filter_Display___Colorspace_transforms.setParamContent("""Resize (%)""",100)
    Display_filter_Display___Colorspace_transforms.getParam("""Resize (%)""").min = 0
    Display_filter_Display___Colorspace_transforms.getParam("""Resize (%)""").max = 200
    Display_filter_Display___Colorspace_transforms.setParamContent("""Resize method""","""Bilinear""")
    Display_filter_Display___Gabor = filters_package.display_filter.Display_filter()
    Display_filter_Display___Gabor.setName("""Display - Gabor""")
    Display_filter_Display___Gabor.setDescription("""Display a image in the viewer window. If the input images' pixels are not all in the [0,1] range, they will get compressed into this range by the 'remap'-function. 
If something is connected to the 'B&W or RGB' input, all other inputs will be ignored.""")
    Display_filter_Display___Gabor.setParamContent("""Resize (%)""",100)
    Display_filter_Display___Gabor.getParam("""Resize (%)""").min = 0
    Display_filter_Display___Gabor.getParam("""Resize (%)""").max = 200
    Display_filter_Display___Gabor.setParamContent("""Resize method""","""Bilinear""")
    Input_filter_Load___Split_image = filters_package.input_filter.Input_filter()
    Input_filter_Load___Split_image.setName("""Load - Split image""")
    Input_filter_Load___Split_image.setDescription("""Load frames from image file, video file or camera. The 'original' output type is faster than floating point output since no scaling is necessary. However, some filters might require floating point input and vice versa.If source is monochrome, the output on all channels will be identical""")
    Input_filter_Load___Split_image.setParamContent("""Output type""","""original""")
    Input_filter_Load___Split_image.setParamContent("""Input type""","""Image file""")
    Input_filter_Load___Split_image.setParamContent("""Camera to use""","""0""")
    Input_filter_Load___Split_image.setParamContent("""Image file""","""/home/lennart/filter-lab/house.jpg""")
    Input_filter_Load___Split_image.setParamContent("""Loop video or sequence""","""No""")
    Input_filter_Load___Split_image.setParamContent("""Video file""","""None""")
    Display_filter_Display___Rotate_and_flip = filters_package.display_filter.Display_filter()
    Display_filter_Display___Rotate_and_flip.setName("""Display - Rotate and flip""")
    Display_filter_Display___Rotate_and_flip.setDescription("""Display a image in the viewer window. If the input images' pixels are not all in the [0,1] range, they will get compressed into this range by the 'remap'-function. 
If something is connected to the 'B&W or RGB' input, all other inputs will be ignored.""")
    Display_filter_Display___Rotate_and_flip.setParamContent("""Resize (%)""",100)
    Display_filter_Display___Rotate_and_flip.getParam("""Resize (%)""").min = 0
    Display_filter_Display___Rotate_and_flip.getParam("""Resize (%)""").max = 200
    Display_filter_Display___Rotate_and_flip.setParamContent("""Resize method""","""Bilinear""")
    Input_filter_Load___Remap_pixel_range = filters_package.input_filter.Input_filter()
    Input_filter_Load___Remap_pixel_range.setName("""Load - Remap pixel range""")
    Input_filter_Load___Remap_pixel_range.setDescription("""Load frames from image file, video file or camera. The 'original' output type is faster than floating point output since no scaling is necessary. However, some filters might require floating point input and vice versa.If source is monochrome, the output on all channels will be identical""")
    Input_filter_Load___Remap_pixel_range.setParamContent("""Output type""","""original""")
    Input_filter_Load___Remap_pixel_range.setParamContent("""Input type""","""Image file""")
    Input_filter_Load___Remap_pixel_range.setParamContent("""Camera to use""","""0""")
    Input_filter_Load___Remap_pixel_range.setParamContent("""Image file""","""/home/lennart/filter-lab/house.jpg""")
    Input_filter_Load___Remap_pixel_range.setParamContent("""Loop video or sequence""","""No""")
    Input_filter_Load___Remap_pixel_range.setParamContent("""Video file""","""None""")
    Input_filter_Load___Rotate_and_flip = filters_package.input_filter.Input_filter()
    Input_filter_Load___Rotate_and_flip.setName("""Load - Rotate and flip""")
    Input_filter_Load___Rotate_and_flip.setDescription("""Load frames from image file, video file or camera. The 'original' output type is faster than floating point output since no scaling is necessary. However, some filters might require floating point input and vice versa.If source is monochrome, the output on all channels will be identical""")
    Input_filter_Load___Rotate_and_flip.setParamContent("""Output type""","""original""")
    Input_filter_Load___Rotate_and_flip.setParamContent("""Input type""","""Image file""")
    Input_filter_Load___Rotate_and_flip.setParamContent("""Camera to use""","""0""")
    Input_filter_Load___Rotate_and_flip.setParamContent("""Image file""","""/home/lennart/filter-lab/house.jpg""")
    Input_filter_Load___Rotate_and_flip.setParamContent("""Loop video or sequence""","""No""")
    Input_filter_Load___Rotate_and_flip.setParamContent("""Video file""","""None""")
    Input_filter_Load___Edge_detection__Canny_ = filters_package.input_filter.Input_filter()
    Input_filter_Load___Edge_detection__Canny_.setName("""Load - Edge detection (Canny)""")
    Input_filter_Load___Edge_detection__Canny_.setDescription("""Load frames from image file, video file or camera. The 'original' output type is faster than floating point output since no scaling is necessary. However, some filters might require floating point input and vice versa.If source is monochrome, the output on all channels will be identical""")
    Input_filter_Load___Edge_detection__Canny_.setParamContent("""Output type""","""original""")
    Input_filter_Load___Edge_detection__Canny_.setParamContent("""Input type""","""Image file""")
    Input_filter_Load___Edge_detection__Canny_.setParamContent("""Camera to use""","""0""")
    Input_filter_Load___Edge_detection__Canny_.setParamContent("""Image file""","""/home/lennart/filter-lab/house.jpg""")
    Input_filter_Load___Edge_detection__Canny_.setParamContent("""Loop video or sequence""","""No""")
    Input_filter_Load___Edge_detection__Canny_.setParamContent("""Video file""","""None""")
    Display_filter_Display___Resize = filters_package.display_filter.Display_filter()
    Display_filter_Display___Resize.setName("""Display - Resize""")
    Display_filter_Display___Resize.setDescription("""Display a image in the viewer window. If the input images' pixels are not all in the [0,1] range, they will get compressed into this range by the 'remap'-function. 
If something is connected to the 'B&W or RGB' input, all other inputs will be ignored.""")
    Display_filter_Display___Resize.setParamContent("""Resize (%)""",100)
    Display_filter_Display___Resize.getParam("""Resize (%)""").min = 0
    Display_filter_Display___Resize.getParam("""Resize (%)""").max = 200
    Display_filter_Display___Resize.setParamContent("""Resize method""","""Bilinear""")
    Code_input_filter_Code_input = filters_package.code_input_filter.Code_input_filter()
    Code_input_filter_Code_input.setName("""Code input""")
    Code_input_filter_Code_input.setDescription("""Specify any operations to apply to the input data. The command line input will be interpreted as a regular python command, so please be very careful not to do anything dangerous. If nothing is connected to an input, that input will be set as a scalar zero.""")
    Code_input_filter_Code_input.setParamContent("""Code for imports""","""import numpy as np


""")
    Code_input_filter_Code_input.setParamContent("""Variable z""",1)
    Code_input_filter_Code_input.getParam("""Variable z""").min = 0
    Code_input_filter_Code_input.getParam("""Variable z""").max = 1
    Code_input_filter_Code_input.setParamContent("""Variable x""",1)
    Code_input_filter_Code_input.getParam("""Variable x""").min = 0
    Code_input_filter_Code_input.getParam("""Variable x""").max = 1
    Code_input_filter_Code_input.setParamContent("""Variable y""",1)
    Code_input_filter_Code_input.getParam("""Variable y""").min = 0
    Code_input_filter_Code_input.getParam("""Variable y""").max = 1
    Code_input_filter_Code_input.setParamContent("""Processing code""","""outA = inA*x-inB*y-inC*z









""")
    Input_filter_Load___Crop = filters_package.input_filter.Input_filter()
    Input_filter_Load___Crop.setName("""Load - Crop""")
    Input_filter_Load___Crop.setDescription("""Load frames from image file, video file or camera. The 'original' output type is faster than floating point output since no scaling is necessary. However, some filters might require floating point input and vice versa.If source is monochrome, the output on all channels will be identical""")
    Input_filter_Load___Crop.setParamContent("""Output type""","""original""")
    Input_filter_Load___Crop.setParamContent("""Input type""","""Image file""")
    Input_filter_Load___Crop.setParamContent("""Camera to use""","""0""")
    Input_filter_Load___Crop.setParamContent("""Image file""","""/home/lennart/filter-lab/house.jpg""")
    Input_filter_Load___Crop.setParamContent("""Loop video or sequence""","""No""")
    Input_filter_Load___Crop.setParamContent("""Video file""","""None""")
    Rotate_and_flip_filter_Rotate_and_flip = filters_package.rotate_and_flip_filter.Rotate_and_flip_filter()
    Rotate_and_flip_filter_Rotate_and_flip.setName("""Rotate and flip""")
    Rotate_and_flip_filter_Rotate_and_flip.setDescription("""Rotate the input image by 90-degrees increments or flip it.""")
    Rotate_and_flip_filter_Rotate_and_flip.setParamContent("""Rotate:""","""Rotate upside-down""")
    Rotate_and_flip_filter_Rotate_and_flip.setParamContent("""Flip:""","""No""")
    Smooth_filter_Smooth = filters_package.smooth_filter.Smooth_filter()
    Smooth_filter_Smooth.setName("""Smooth""")
    Smooth_filter_Smooth.setDescription("""Smooth the image. 
To disable all smoothing, set all sliders to zero.""")
    Smooth_filter_Smooth.setParamContent("""Smoothing method""","""Gaussian""")
    Smooth_filter_Smooth.setParamContent("""Gaussian standard deviation""",0)
    Smooth_filter_Smooth.getParam("""Gaussian standard deviation""").min = 0
    Smooth_filter_Smooth.getParam("""Gaussian standard deviation""").max = 15
    Smooth_filter_Smooth.setParamContent("""Smoothing kernel width""",3)
    Smooth_filter_Smooth.getParam("""Smoothing kernel width""").min = 0
    Smooth_filter_Smooth.getParam("""Smoothing kernel width""").max = 15
    Smooth_filter_Smooth.setParamContent("""Smoothing kernel height""",0)
    Smooth_filter_Smooth.getParam("""Smoothing kernel height""").min = 0
    Smooth_filter_Smooth.getParam("""Smoothing kernel height""").max = 15
    Crop_filter_Crop = filters_package.crop_filter.Crop_filter()
    Crop_filter_Crop.setName("""Crop""")
    Crop_filter_Crop.setDescription("""Crop the image dimensions.""")
    Crop_filter_Crop.setParamContent("""Width""",320)
    Crop_filter_Crop.getParam("""Width""").min = 0
    Crop_filter_Crop.getParam("""Width""").max = 2048
    Crop_filter_Crop.setParamContent("""Center y-position""",0)
    Crop_filter_Crop.getParam("""Center y-position""").min = 0
    Crop_filter_Crop.getParam("""Center y-position""").max = 2048
    Crop_filter_Crop.setParamContent("""Center x-position""",0)
    Crop_filter_Crop.getParam("""Center x-position""").min = 0
    Crop_filter_Crop.getParam("""Center x-position""").max = 2048
    Crop_filter_Crop.setParamContent("""Height""",240)
    Crop_filter_Crop.getParam("""Height""").min = 0
    Crop_filter_Crop.getParam("""Height""").max = 2048
    Fourier_filter_Fourier_transforms = filters_package.fourier_filter.Fourier_filter()
    Fourier_filter_Fourier_transforms.setName("""Fourier transforms""")
    Fourier_filter_Fourier_transforms.setDescription("""Take the fourier transform or it's inverse of the input image. The 'Real' output will always provide the real portion of the selected transform. If 'Output complex on 'Imag'' is set to 'Yes', the 'Imag' output will output complex numbers (complex datatype) instead of just the imaginary part of the transform. Complex matrices as input on either of the inputs will be autodetected, and if nothing is connected to the other input, the corresponding part (real or imaginary) of the matrix will be copied to the empty input.""")
    Fourier_filter_Fourier_transforms.setParamContent("""Direction of transform""","""Transform""")
    Fourier_filter_Fourier_transforms.setParamContent("""Output complex on 'Imag'""","""No""")
    Fourier_filter_Fourier_transforms.setParamContent("""Shift origin""","""No""")
    Fourier_filter_Fourier_transforms.setParamContent("""Use complex single input""","""Yes""")
    Display_filter_Display___Code_input = filters_package.display_filter.Display_filter()
    Display_filter_Display___Code_input.setName("""Display - Code input""")
    Display_filter_Display___Code_input.setDescription("""Display a image in the viewer window. If the input images' pixels are not all in the [0,1] range, they will get compressed into this range by the 'remap'-function. 
If something is connected to the 'B&W or RGB' input, all other inputs will be ignored.""")
    Display_filter_Display___Code_input.setParamContent("""Resize (%)""",100)
    Display_filter_Display___Code_input.getParam("""Resize (%)""").min = 0
    Display_filter_Display___Code_input.getParam("""Resize (%)""").max = 200
    Display_filter_Display___Code_input.setParamContent("""Resize method""","""Bilinear""")
    Colorspace_filter_Colorspace_transforms = filters_package.colorspace_filter.Colorspace_filter()
    Colorspace_filter_Colorspace_transforms.setName("""Colorspace transforms""")
    Colorspace_filter_Colorspace_transforms.setDescription("""Convert the input image to a new colorspace""")
    Colorspace_filter_Colorspace_transforms.setParamContent("""Transformation""","""RGB->HLS""")
    Display_filter_Display___Color_blindness = filters_package.display_filter.Display_filter()
    Display_filter_Display___Color_blindness.setName("""Display - Color blindness""")
    Display_filter_Display___Color_blindness.setDescription("""Display a image in the viewer window. If the input images' pixels are not all in the [0,1] range, they will get compressed into this range by the 'remap'-function. 
If something is connected to the 'B&W or RGB' input, all other inputs will be ignored.""")
    Display_filter_Display___Color_blindness.setParamContent("""Resize (%)""",100)
    Display_filter_Display___Color_blindness.getParam("""Resize (%)""").min = 0
    Display_filter_Display___Color_blindness.getParam("""Resize (%)""").max = 200
    Display_filter_Display___Color_blindness.setParamContent("""Resize method""","""Bilinear""")
    Display_filter_Display___Adaptation = filters_package.display_filter.Display_filter()
    Display_filter_Display___Adaptation.setName("""Display - Adaptation""")
    Display_filter_Display___Adaptation.setDescription("""Display a image in the viewer window. If the input images' pixels are not all in the [0,1] range, they will get compressed into this range by the 'remap'-function. 
If something is connected to the 'B&W or RGB' input, all other inputs will be ignored.""")
    Display_filter_Display___Adaptation.setParamContent("""Resize (%)""",100)
    Display_filter_Display___Adaptation.getParam("""Resize (%)""").min = 0
    Display_filter_Display___Adaptation.getParam("""Resize (%)""").max = 200
    Display_filter_Display___Adaptation.setParamContent("""Resize method""","""Bilinear""")
    Remap_range_filter_Remap_pixel_range = filters_package.remap_range_filter.Remap_range_filter()
    Remap_range_filter_Remap_pixel_range.setName("""Remap pixel range""")
    Remap_range_filter_Remap_pixel_range.setDescription("""Linearly remap the input image's pixel value range to a new range.""")
    Remap_range_filter_Remap_pixel_range.setParamContent("""End of old range""",0)
    Remap_range_filter_Remap_pixel_range.getParam("""End of old range""").min = -4
    Remap_range_filter_Remap_pixel_range.getParam("""End of old range""").max = 4
    Remap_range_filter_Remap_pixel_range.setParamContent("""Start of new range""",0)
    Remap_range_filter_Remap_pixel_range.getParam("""Start of new range""").min = -4
    Remap_range_filter_Remap_pixel_range.getParam("""Start of new range""").max = 4
    Remap_range_filter_Remap_pixel_range.setParamContent("""Start of old range""",0)
    Remap_range_filter_Remap_pixel_range.getParam("""Start of old range""").min = -4
    Remap_range_filter_Remap_pixel_range.getParam("""Start of old range""").max = 4
    Remap_range_filter_Remap_pixel_range.setParamContent("""End of new range""",1)
    Remap_range_filter_Remap_pixel_range.getParam("""End of new range""").min = -4
    Remap_range_filter_Remap_pixel_range.getParam("""End of new range""").max = 4
    Time_lag_filter_Time_lag = filters_package.time_lag_filter.Time_lag_filter()
    Time_lag_filter_Time_lag.setName("""Time lag""")
    Time_lag_filter_Time_lag.setDescription("""Will act as a time lag and output the n'th frame before the current one. n=0: Current frame, n=1: Previous frame""")
    Time_lag_filter_Time_lag.setParamContent("""Input interval (frames)""","""1""")
    Input_filter_Load___Time_lag = filters_package.input_filter.Input_filter()
    Input_filter_Load___Time_lag.setName("""Load - Time lag""")
    Input_filter_Load___Time_lag.setDescription("""Load frames from image file, video file or camera. The 'original' output type is faster than floating point output since no scaling is necessary. However, some filters might require floating point input and vice versa.If source is monochrome, the output on all channels will be identical""")
    Input_filter_Load___Time_lag.setParamContent("""Output type""","""original""")
    Input_filter_Load___Time_lag.setParamContent("""Input type""","""Image file""")
    Input_filter_Load___Time_lag.setParamContent("""Camera to use""","""0""")
    Input_filter_Load___Time_lag.setParamContent("""Image file""","""/home/lennart/filter-lab/house.jpg""")
    Input_filter_Load___Time_lag.setParamContent("""Loop video or sequence""","""No""")
    Input_filter_Load___Time_lag.setParamContent("""Video file""","""None""")
    Blindness_filter_Color_blindness = filters_package.blindness_filter.Blindness_filter()
    Blindness_filter_Color_blindness.setName("""Color blindness""")
    Blindness_filter_Color_blindness.setDescription("""Simulate different color blindnesses. """)
    Blindness_filter_Color_blindness.setParamContent("""Type of blindness""","""Protanope""")
    Display_filter_Display___Crop = filters_package.display_filter.Display_filter()
    Display_filter_Display___Crop.setName("""Display - Crop""")
    Display_filter_Display___Crop.setDescription("""Display a image in the viewer window. If the input images' pixels are not all in the [0,1] range, they will get compressed into this range by the 'remap'-function. 
If something is connected to the 'B&W or RGB' input, all other inputs will be ignored.""")
    Display_filter_Display___Crop.setParamContent("""Resize (%)""",100)
    Display_filter_Display___Crop.getParam("""Resize (%)""").min = 0
    Display_filter_Display___Crop.getParam("""Resize (%)""").max = 200
    Display_filter_Display___Crop.setParamContent("""Resize method""","""Bilinear""")
    Input_filter_Load___Curve = filters_package.input_filter.Input_filter()
    Input_filter_Load___Curve.setName("""Load - Curve""")
    Input_filter_Load___Curve.setDescription("""Load frames from image file, video file or camera. The 'original' output type is faster than floating point output since no scaling is necessary. However, some filters might require floating point input and vice versa.If source is monochrome, the output on all channels will be identical""")
    Input_filter_Load___Curve.setParamContent("""Output type""","""original""")
    Input_filter_Load___Curve.setParamContent("""Input type""","""Image file""")
    Input_filter_Load___Curve.setParamContent("""Camera to use""","""0""")
    Input_filter_Load___Curve.setParamContent("""Image file""","""/home/lennart/filter-lab/house.jpg""")
    Input_filter_Load___Curve.setParamContent("""Loop video or sequence""","""No""")
    Input_filter_Load___Curve.setParamContent("""Video file""","""None""")
    Display_filter_Display___Clip = filters_package.display_filter.Display_filter()
    Display_filter_Display___Clip.setName("""Display - Clip""")
    Display_filter_Display___Clip.setDescription("""Display a image in the viewer window. If the input images' pixels are not all in the [0,1] range, they will get compressed into this range by the 'remap'-function. 
If something is connected to the 'B&W or RGB' input, all other inputs will be ignored.""")
    Display_filter_Display___Clip.setParamContent("""Resize (%)""",100)
    Display_filter_Display___Clip.getParam("""Resize (%)""").min = 0
    Display_filter_Display___Clip.getParam("""Resize (%)""").max = 200
    Display_filter_Display___Clip.setParamContent("""Resize method""","""Bilinear""")
    Gabor_filter_Gabor = filters_package.gabor_filter.Gabor_filter()
    Gabor_filter_Gabor.setName("""Gabor""")
    Gabor_filter_Gabor.setDescription("""Will convolve the input image with a specified Gabor kernel. Please note that the kernel size at the moment is fixed at 21 pixels. Feel free to edit the code to add an autoadjusted kernel size for improved performance. """)
    Gabor_filter_Gabor.setParamContent("""Frequency (cycles / 100 pixels)""",10)
    Gabor_filter_Gabor.getParam("""Frequency (cycles / 100 pixels)""").min = 2
    Gabor_filter_Gabor.getParam("""Frequency (cycles / 100 pixels)""").max = 50
    Gabor_filter_Gabor.setParamContent("""Field of view (degrees)""",45)
    Gabor_filter_Gabor.getParam("""Field of view (degrees)""").min = 2
    Gabor_filter_Gabor.getParam("""Field of view (degrees)""").max = 180
    Gabor_filter_Gabor.setParamContent("""Phase (degrees)""",0)
    Gabor_filter_Gabor.getParam("""Phase (degrees)""").min = -180
    Gabor_filter_Gabor.getParam("""Phase (degrees)""").max = 180
    Gabor_filter_Gabor.setParamContent("""Scale (pixels)""",3)
    Gabor_filter_Gabor.getParam("""Scale (pixels)""").min = 1
    Gabor_filter_Gabor.getParam("""Scale (pixels)""").max = 20
    Gabor_filter_Gabor.setParamContent("""Kernel angle (degrees)""",45.0)
    Gabor_filter_Gabor.getParam("""Kernel angle (degrees)""").min = 0.0
    Gabor_filter_Gabor.getParam("""Kernel angle (degrees)""").max = 180
    Gabor_filter_Gabor.setParamContent("""Output only positive pixels""","""No""")
    Gabor_filter_Gabor.setParamContent("""Aspect ratio""",0.8)
    Gabor_filter_Gabor.getParam("""Aspect ratio""").min = 0
    Gabor_filter_Gabor.getParam("""Aspect ratio""").max = 2
    Display_filter_Display___Smooth = filters_package.display_filter.Display_filter()
    Display_filter_Display___Smooth.setName("""Display - Smooth""")
    Display_filter_Display___Smooth.setDescription("""Display a image in the viewer window. If the input images' pixels are not all in the [0,1] range, they will get compressed into this range by the 'remap'-function. 
If something is connected to the 'B&W or RGB' input, all other inputs will be ignored.""")
    Display_filter_Display___Smooth.setParamContent("""Resize (%)""",100)
    Display_filter_Display___Smooth.getParam("""Resize (%)""").min = 0
    Display_filter_Display___Smooth.getParam("""Resize (%)""").max = 200
    Display_filter_Display___Smooth.setParamContent("""Resize method""","""Bilinear""")
    Input_filter_Load___Blend_together = filters_package.input_filter.Input_filter()
    Input_filter_Load___Blend_together.setName("""Load - Blend together""")
    Input_filter_Load___Blend_together.setDescription("""Load frames from image file, video file or camera. The 'original' output type is faster than floating point output since no scaling is necessary. However, some filters might require floating point input and vice versa.If source is monochrome, the output on all channels will be identical""")
    Input_filter_Load___Blend_together.setParamContent("""Output type""","""original""")
    Input_filter_Load___Blend_together.setParamContent("""Input type""","""Image file""")
    Input_filter_Load___Blend_together.setParamContent("""Camera to use""","""0""")
    Input_filter_Load___Blend_together.setParamContent("""Image file""","""/home/lennart/filter-lab/house.jpg""")
    Input_filter_Load___Blend_together.setParamContent("""Loop video or sequence""","""No""")
    Input_filter_Load___Blend_together.setParamContent("""Video file""","""None""")
    Display_filter_Display___Curve = filters_package.display_filter.Display_filter()
    Display_filter_Display___Curve.setName("""Display - Curve""")
    Display_filter_Display___Curve.setDescription("""Display a image in the viewer window. If the input images' pixels are not all in the [0,1] range, they will get compressed into this range by the 'remap'-function. 
If something is connected to the 'B&W or RGB' input, all other inputs will be ignored.""")
    Display_filter_Display___Curve.setParamContent("""Resize (%)""",100)
    Display_filter_Display___Curve.getParam("""Resize (%)""").min = 0
    Display_filter_Display___Curve.getParam("""Resize (%)""").max = 200
    Display_filter_Display___Curve.setParamContent("""Resize method""","""Bilinear""")
    Clip_filter_Clip = filters_package.clip_filter.Clip_filter()
    Clip_filter_Clip.setName("""Clip""")
    Clip_filter_Clip.setDescription("""Clip the pixel values of an image to a specified range.""")
    Clip_filter_Clip.setParamContent("""Minimum threshhold""",0)
    Clip_filter_Clip.getParam("""Minimum threshhold""").min = -4
    Clip_filter_Clip.getParam("""Minimum threshhold""").max = 4
    Clip_filter_Clip.setParamContent("""Maximum threshhold""",1)
    Clip_filter_Clip.getParam("""Maximum threshhold""").min = -4
    Clip_filter_Clip.getParam("""Maximum threshhold""").max = 4
    Opponent_filter_Opponent_colors = filters_package.opponent_filter.Opponent_filter()
    Opponent_filter_Opponent_colors.setName("""Opponent colors""")
    Opponent_filter_Opponent_colors.setDescription("""Convert the channels in the input RGB-image to opponent colors channels by simple pixel arithmetic.Note that all inputs have to be connected for the filter to work.""")
    Display_filter_Display___Split_image = filters_package.display_filter.Display_filter()
    Display_filter_Display___Split_image.setName("""Display - Split image""")
    Display_filter_Display___Split_image.setDescription("""Display a image in the viewer window. If the input images' pixels are not all in the [0,1] range, they will get compressed into this range by the 'remap'-function. 
If something is connected to the 'B&W or RGB' input, all other inputs will be ignored.""")
    Display_filter_Display___Split_image.setParamContent("""Resize (%)""",100)
    Display_filter_Display___Split_image.getParam("""Resize (%)""").min = 0
    Display_filter_Display___Split_image.getParam("""Resize (%)""").max = 200
    Display_filter_Display___Split_image.setParamContent("""Resize method""","""Bilinear""")
    Display_filter_Display___Fourier_transforms = filters_package.display_filter.Display_filter()
    Display_filter_Display___Fourier_transforms.setName("""Display - Fourier transforms""")
    Display_filter_Display___Fourier_transforms.setDescription("""Display a image in the viewer window. If the input images' pixels are not all in the [0,1] range, they will get compressed into this range by the 'remap'-function. 
If something is connected to the 'B&W or RGB' input, all other inputs will be ignored.""")
    Display_filter_Display___Fourier_transforms.setParamContent("""Resize (%)""",100)
    Display_filter_Display___Fourier_transforms.getParam("""Resize (%)""").min = 0
    Display_filter_Display___Fourier_transforms.getParam("""Resize (%)""").max = 200
    Display_filter_Display___Fourier_transforms.setParamContent("""Resize method""","""Bilinear""")
    Resize_filter_Resize = filters_package.resize_filter.Resize_filter()
    Resize_filter_Resize.setName("""Resize""")
    Resize_filter_Resize.setDescription("""Resize the input image's dimensions by various methods. IMPORTANT IMPLEMENTATION NOTE: If the input pixels have float type and 'Bicubic' is chosen, the output image will be clipped to the minimum and maximum pixel values of the input image to ensure similar result to the other methods.""")
    Resize_filter_Resize.setParamContent("""Percent of original size""",100)
    Resize_filter_Resize.getParam("""Percent of original size""").min = 0
    Resize_filter_Resize.getParam("""Percent of original size""").max = 200
    Resize_filter_Resize.setParamContent("""New height""",640)
    Resize_filter_Resize.getParam("""New height""").min = 64
    Resize_filter_Resize.getParam("""New height""").max = 2048
    Resize_filter_Resize.setParamContent("""New width""",640)
    Resize_filter_Resize.getParam("""New width""").min = 64
    Resize_filter_Resize.getParam("""New width""").max = 2048
    Resize_filter_Resize.setParamContent("""Resize method""","""Bilinear""")
    Resize_filter_Resize.setParamContent("""Aspect ratio (width:height)""",1)
    Resize_filter_Resize.getParam("""Aspect ratio (width:height)""").min = 0.2
    Resize_filter_Resize.getParam("""Aspect ratio (width:height)""").max = 2
    Resize_filter_Resize.setParamContent("""Resize by""","""percent and aspect ratio""")
    

    connect_filters(Blend_filter_Blend_together,Display_filter_Display___Blend_together,["""Output"""],["""BW or RGB"""])
    connect_filters(Remap_range_filter_Remap_pixel_range,Display_filter_Display___Remap_pixel_range,["""Output"""],["""BW or RGB"""])
    connect_filters(Input_filter_Load___Adaptation,Adaptation_filter_Adaptation,["""Red"""],["""Input"""])
    connect_filters(Input_filter_Load___Edge_detection__Canny_,Canny_filter_Edge_detection__Canny_,["""Red"""],["""Input"""])
    connect_filters(Time_lag_filter_Time_lag,Display_filter_Display___Time_lag,["""Output"""],["""BW or RGB"""])
    connect_filters(Input_filter_Load___Curve,Curve_filter_Curve,["""Red"""],["""Input"""])
    connect_filters(Canny_filter_Edge_detection__Canny_,Display_filter_Display___Edge_detection__Canny_,["""Output"""],["""BW or RGB"""])
    connect_filters(Input_filter_Load___Split_image,Split_filter_Split_image,["""RGB"""],["""Input"""])
    connect_filters(Input_filter_Load___Blend_together,Blend_filter_Blend_together,["""RGB"""],["""Input 1"""])
    connect_filters(Input_filter_Load___Histogram,Histogram_filter_Histogram,["""Red"""],["""Input"""])
    connect_filters(Opponent_filter_Opponent_colors,Display_filter_Display___Opponent_colors,["""Red-Green"""],["""BW or RGB"""])
    connect_filters(Colorspace_filter_Colorspace_transforms,Display_filter_Display___Colorspace_transforms,["""Output 1"""],["""BW or RGB"""])
    connect_filters(Gabor_filter_Gabor,Display_filter_Display___Gabor,["""Gabor filtered"""],["""BW or RGB"""])
    connect_filters(Rotate_and_flip_filter_Rotate_and_flip,Display_filter_Display___Rotate_and_flip,["""Output"""],["""BW or RGB"""])
    connect_filters(Resize_filter_Resize,Display_filter_Display___Resize,["""Output 1"""],["""BW or RGB"""])
    connect_filters(Input_filter_Load___Code_input,Code_input_filter_Code_input,["""RGB"""],["""inA"""])
    connect_filters(Input_filter_Load___Rotate_and_flip,Rotate_and_flip_filter_Rotate_and_flip,["""RGB"""],["""Input"""])
    connect_filters(Input_filter_Load___Smooth,Smooth_filter_Smooth,["""RGB"""],["""Input"""])
    connect_filters(Input_filter_Load___Crop,Crop_filter_Crop,["""RGB"""],["""Input"""])
    connect_filters(Input_filter_Load___Fourier_transforms,Fourier_filter_Fourier_transforms,["""RGB"""],["""Real"""])
    connect_filters(Code_input_filter_Code_input,Display_filter_Display___Code_input,["""outA"""],["""BW or RGB"""])
    connect_filters(Input_filter_Load___Colorspace_transforms,Colorspace_filter_Colorspace_transforms,["""Blue"""],["""Input 3"""])
    connect_filters(Input_filter_Load___Colorspace_transforms,Colorspace_filter_Colorspace_transforms,["""Green"""],["""Input 2"""])
    connect_filters(Input_filter_Load___Colorspace_transforms,Colorspace_filter_Colorspace_transforms,["""Red"""],["""Input 1"""])
    connect_filters(Blindness_filter_Color_blindness,Display_filter_Display___Color_blindness,["""Red"""],["""Ch 1, Red"""])
    connect_filters(Blindness_filter_Color_blindness,Display_filter_Display___Color_blindness,["""Blue"""],["""Ch 3, Blue"""])
    connect_filters(Blindness_filter_Color_blindness,Display_filter_Display___Color_blindness,["""Green"""],["""Ch 2, Green"""])
    connect_filters(Adaptation_filter_Adaptation,Display_filter_Display___Adaptation,["""Output"""],["""BW or RGB"""])
    connect_filters(Input_filter_Load___Remap_pixel_range,Remap_range_filter_Remap_pixel_range,["""RGB"""],["""Input"""])
    connect_filters(Input_filter_Load___Time_lag,Time_lag_filter_Time_lag,["""RGB"""],["""Input"""])
    connect_filters(Input_filter_Load___Color_blindness,Blindness_filter_Color_blindness,["""Blue"""],["""Blue"""])
    connect_filters(Input_filter_Load___Color_blindness,Blindness_filter_Color_blindness,["""Green"""],["""Green"""])
    connect_filters(Input_filter_Load___Color_blindness,Blindness_filter_Color_blindness,["""Red"""],["""Red"""])
    connect_filters(Crop_filter_Crop,Display_filter_Display___Crop,["""Output"""],["""BW or RGB"""])
    connect_filters(Clip_filter_Clip,Display_filter_Display___Clip,["""Output"""],["""BW or RGB"""])
    connect_filters(Input_filter_Load___Gabor,Gabor_filter_Gabor,["""Red"""],["""Input"""])
    connect_filters(Smooth_filter_Smooth,Display_filter_Display___Smooth,["""Output"""],["""BW or RGB"""])
    connect_filters(Curve_filter_Curve,Display_filter_Display___Curve,["""Output"""],["""BW or RGB"""])
    connect_filters(Input_filter_Load___Clip,Clip_filter_Clip,["""RGB"""],["""Input"""])
    connect_filters(Input_filter_Load___Opponent_colors,Opponent_filter_Opponent_colors,["""Blue"""],["""Blue"""])
    connect_filters(Input_filter_Load___Opponent_colors,Opponent_filter_Opponent_colors,["""Green"""],["""Green"""])
    connect_filters(Input_filter_Load___Opponent_colors,Opponent_filter_Opponent_colors,["""Red"""],["""Red"""])
    connect_filters(Split_filter_Split_image,Display_filter_Display___Split_image,["""Upper left"""],["""BW or RGB"""])
    connect_filters(Fourier_filter_Fourier_transforms,Display_filter_Display___Fourier_transforms,["""Real"""],["""BW or RGB"""])
    connect_filters(Input_filter_Load___Resize,Resize_filter_Resize,["""RGB"""],["""Input 1"""])
    positions = [(-281.0, 119.0), (33.0, -16.0), (-250.0, -169.0), (1.0, -128.0), (-308.0, 13.0), (170.0, -185.0), (-1.0, -191.0), (52.0, 116.0), (-153.0, 6.0), (-145.0, 41.0), (-105.0, 87.0), (-219.0, 10.0), (-57.0, -140.0), (-54.0, -27.0), (30.0, -132.0), (-131.0, 109.0), (-314.0, -173.0), (-112.0, -129.0), (136.0, -114.0), (150.0, -27.0), (151.0, 39.0), (-191.0, -186.0), (93.0, 11.0), (202.0, -90.0), (-326.0, 6.0), (145.0, 117.0), (-268.0, 26.0), (-133.0, -80.0), (-280.0, -81.0), (136.0, -124.0), (-115.0, 78.0), (-28.0, -45.0), (181.0, -50.0), (-39.0, 163.0), (174.0, -172.0), (8.0, 56.0), (158.0, -37.0), (-310.0, 97.0), (168.0, 120.0), (48.0, 118.0), (-192.0, -191.0), (6.0, 83.0), (-157.0, 7.0), (-282.0, -69.0), (6.0, 121.0), (-327.0, -35.0), (49.0, -149.0), (-87.0, -61.0), (207.0, -193.0), (-121.0, -120.0), (192.0, -111.0), (104.0, 66.0), (-309.0, -123.0), (187.0, 122.0), (201.0, 30.0), (130.0, -186.0)]
    filter_list = [Input_filter_Load___Color_blindness, Display_filter_Display___Blend_together, Input_filter_Load___Code_input, Display_filter_Display___Remap_pixel_range, Input_filter_Load___Gabor, Adaptation_filter_Adaptation, Canny_filter_Edge_detection__Canny_, Display_filter_Display___Time_lag, Input_filter_Load___Opponent_colors, Curve_filter_Curve, Input_filter_Load___Clip, Input_filter_Load___Adaptation, Input_filter_Load___Smooth, Input_filter_Load___Fourier_transforms, Display_filter_Display___Edge_detection__Canny_, Input_filter_Load___Histogram, Split_filter_Split_image, Input_filter_Load___Resize, Blend_filter_Blend_together, Histogram_filter_Histogram, Display_filter_Display___Opponent_colors, Input_filter_Load___Colorspace_transforms, Display_filter_Display___Colorspace_transforms, Display_filter_Display___Gabor, Input_filter_Load___Split_image, Display_filter_Display___Rotate_and_flip, Input_filter_Load___Remap_pixel_range, Input_filter_Load___Rotate_and_flip, Input_filter_Load___Edge_detection__Canny_, Display_filter_Display___Resize, Code_input_filter_Code_input, Input_filter_Load___Crop, Rotate_and_flip_filter_Rotate_and_flip, Smooth_filter_Smooth, Crop_filter_Crop, Fourier_filter_Fourier_transforms, Display_filter_Display___Code_input, Colorspace_filter_Colorspace_transforms, Display_filter_Display___Color_blindness, Display_filter_Display___Adaptation, Remap_range_filter_Remap_pixel_range, Time_lag_filter_Time_lag, Input_filter_Load___Time_lag, Blindness_filter_Color_blindness, Display_filter_Display___Crop, Input_filter_Load___Curve, Display_filter_Display___Clip, Gabor_filter_Gabor, Display_filter_Display___Smooth, Input_filter_Load___Blend_together, Display_filter_Display___Curve, Clip_filter_Clip, Opponent_filter_Opponent_colors, Display_filter_Display___Split_image, Display_filter_Display___Fourier_transforms, Resize_filter_Resize]
    return positions, filter_list

if __name__ == "__main__":
    import os,sys
    flabfile = os.path.join(os.path.split(os.path.split(__file__)[0])[0],'filter_lab.py')
    os.system("""%s "%s" "%s" """ %(sys.executable, flabfile, __file__))
