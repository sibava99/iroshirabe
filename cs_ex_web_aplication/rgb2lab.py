RGB2XYZ_D65 = (0.412453, 0.357580, 0.180423,0.212671, 0.715160, 0.072169,0.019334, 0.119193, 0.950227
)

D65 = ( 0.950456, 1., 1.088754 );

_coff = (
     RGB2XYZ_D65[0]*(1.0/D65[0]),RGB2XYZ_D65[1]*(1.0/D65[0]),RGB2XYZ_D65[2]*(1.0/D65[0]),
     RGB2XYZ_D65[3]*(1.0/D65[1]),RGB2XYZ_D65[4]*(1.0/D65[1]),RGB2XYZ_D65[5]*(1.0/D65[1]),
     RGB2XYZ_D65[6]*(1.0/D65[2]),RGB2XYZ_D65[7]*(1.0/D65[2]),RGB2XYZ_D65[8]*(1.0/D65[2]),
)

def _conv_func(v):
    if v > 0.008856:
        return v ** (1.0 / 3.0)
    else:
        return (903.3 * v + 16 ) / 116.0

def rgb2lab(rgb):
    rgb = [x/255.0 for x in rgb]
    xyz = (
        rgb[0]*_coff[0] + rgb[1]*_coff[1] + rgb[2]*_coff[2],
        rgb[0]*_coff[3] + rgb[1]*_coff[4] + rgb[2]*_coff[5],
        rgb[0]*_coff[6] + rgb[1]*_coff[7] + rgb[2]*_coff[8],
    )

    fX, fY, fZ = map(_conv_func, xyz) 
    L = 116.*fY - 16.;
    a = 500.*(fX - fY);
    b = 200.*(fY - fZ);
    return (L, a, b)

rgb = (255,255,255)
print(rgb2lab(rgb))
