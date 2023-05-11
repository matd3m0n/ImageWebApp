from image import Image
from math import radians
from os.path import splitext
from ipdb import set_trace

from scipy.ndimage import gaussian_filter

def process_image(fp,theta, use_filter, sigma, kernel):

    # given filepath saves rotated image and returns new fp
    # load image
    img = Image(fp)
    # rotate image
    if 1==1: # rotate
        img_rot = img.rotate(radians(theta))

        if use_filter:
            img_rot.ar = gaussian_filter(img_rot.ar,
                    sigma=sigma, radius=kernel)

        # save image
        new_fp = '%s_rot%s'%(splitext(fp)[0], splitext(fp)[1])
        img_rot.save(new_fp)
        # return new fp
        return new_fp

    else: # debug
        # save image
        new_fp = '%s_rot%s'%(splitext(fp)[0], splitext(fp)[1])
        img.save(new_fp)
        # return new fp
        return new_fp


