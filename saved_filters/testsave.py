# -*- coding:utf-8 -*-
#This python code creates a list of connected filter instances.


import os,sys
sys.path.append(os.path.split(os.path.split(__file__)[0])[0])
import filters_package
from filters_package.filter_base import connect_filters


def getFilterList():
    Blindness_filter_Color_blindness = filters_package.blindness_filter.Blindness_filter()
    Blindness_filter_Color_blindness.setName("""Color blindness""")
    Blindness_filter_Color_blindness.setDescription("""Simulate different color blindnesses. """)
    Blindness_filter_Color_blindness.setParamContent("""Type of blindness""","""Protanope""")
    Display_filter_Display = filters_package.display_filter.Display_filter()
    Display_filter_Display.setName("""Display""")
    Display_filter_Display.setDescription("""Display a image in the viewer window. If the input images' pixels are not all in the [0,1] range, they will get compressed into this range by the 'remap'-function. 
If something is connected to the 'B&W or RGB' input, all other inputs will be ignored.""")
    Display_filter_Display.setParamContent("""Resize (%)""",100)
    Display_filter_Display.getParam("""Resize (%)""").min = 0
    Display_filter_Display.getParam("""Resize (%)""").max = 200
    Display_filter_Display.setParamContent("""Resize method""","""Bilinear""")
    Input_filter_Load_image = filters_package.input_filter.Input_filter()
    Input_filter_Load_image.setName("""Load image""")
    Input_filter_Load_image.setDescription("""Load frames from image file, video file or camera. The 'original' output type is faster than floating point output since no scaling is necessary. However, some filters might require floating point input and vice versa.If source is monochrome, the output on all channels will be identical""")
    Input_filter_Load_image.setParamContent("""Image file""","""C:\My Dropbox\eclipse workspace\ImageFilterLab\src\house.jpg""")
    Input_filter_Load_image.setParamContent("""Loop video or sequence""","""No""")
    Input_filter_Load_image.setParamContent("""Output type""","""as float, range 0-1""")
    Input_filter_Load_image.setParamContent("""Input type""","""Image file""")
    Input_filter_Load_image.setParamContent("""Video file""","""None""")
    

    connect_filters(Input_filter_Load_image,Blindness_filter_Color_blindness,["""Green"""],["""Blue"""])
    connect_filters(Input_filter_Load_image,Blindness_filter_Color_blindness,["""Red"""],["""Green"""])
    connect_filters(Input_filter_Load_image,Blindness_filter_Color_blindness,["""Blue"""],["""Red"""])
    connect_filters(Blindness_filter_Color_blindness,Display_filter_Display,["""Red"""],["""BW or RGB"""])
    positions = [(63.0, -272.0), (262.0, -196.0), (-121.0, -341.0)]
    filter_list = [Blindness_filter_Color_blindness, Display_filter_Display, Input_filter_Load_image]
    return positions, filter_list

if __name__ == "__main__":
    import os,sys
    flabfile = os.path.join(os.path.split(os.path.split(__file__)[0])[0],'filter_lab.py')
    os.system("""%s "%s" "%s" """ %(sys.executable, flabfile, __file__))
