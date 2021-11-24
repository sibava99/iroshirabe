from skimage import color
import numpy as np

'''
from colormath.color_diff import delta_e_cie2000 as cm_delta_e_cie2000
from colormath.color_objects import sRGBColor as cm_sRGBColor, LabColor as cm_LabColor
from colormath.color_conversations import conver_color as cm_convert_color
'''
def convert(rgb):
	return color.rgb2lab([[[rgb]]])

#def colormath_rgb2lab(rgb):
#	return cm_convert_color(cm_sRGBColor(*(rgb / 255)), cm_LabColor, target_illuminant='d65')


rgb1 = np.array([0,0,0],np.int8)
rgb2 = np.array([255,255,255],np.int8)
print(color.deltaE_ciede2000(convert(rgb1),convert(rgb2),1,1,1))
print(color.deltaE_cie76(convert(rgb1),convert(rgb2)))
print(color.deltaE_cie76([0,0,0],[100,0,0]))
print(convert(rgb1))
print(convert(rgb2))
#print(cm_delta_e_cie2000(colormath_rgb2lab(rgb1), colormath_rgb2lab(rgb2)))
