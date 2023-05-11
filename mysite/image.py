import PIL
import numpy as np
import matplotlib.pyplot as plt
from math import sin, cos, floor, ceil


from tqdm import tqdm

def point_span(ht):
    all_x, all_y = [], []
    for x,y in ht.keys():
        all_x.append(x)
        all_y.append(y)

    print('x span: %d %d so %d'%(min(all_x), max(all_x),
        max(all_x)-min(all_x)))
    print('y span: %d %d so %d'%(min(all_y), max(all_y),
        max(all_y)-min(all_y)))



class Image:
    def __init__(self, fp):
        img = PIL.Image.open(fp)
        self.ar = np.asarray(img)
        self.center = round(self.ar.shape[0]/2),\
                round(self.ar.shape[1]/2)

    @classmethod
    def from_numpy(cls, ar):
        instance = cls.__new__(cls)
        instance.ar = ar
        instance.center = round(ar.shape[0]/2),\
                round(ar.shape[1]/2)
        return instance

    @property
    def shape(self):
        return self.ar.shape

    def save(self, fp):
        tmp_img = PIL.Image.fromarray(self.ar)
        tmp_img.save(fp)


    def rotate(self, theta):
        def rotate_point(p, theta):
            x,y = p
            x_rot = x * cos(theta) + y*sin(theta)
            y_rot = -1*x * sin(theta) + y*cos(theta)
            return round(x_rot), round(y_rot)

        def to_orig_coord(p, center):
            p_orig = (p[0]-center[0], p[1]-center[1])
            return p_orig

        def to_np_coord(p, center):
            p_np = (p[0]+center[0], p[1]+center[1])
            return p_np


        # compute size of new image
        x_np_min, y_np_min = 0,0
        x_np_max = self.ar.shape[0]
        y_np_max = self.ar.shape[1]

        p1, p2, p3, p4 = (x_np_min, y_np_min), (x_np_min, y_np_max),\
                (x_np_max, y_np_min), (x_np_max, y_np_max)

        p1r = rotate_point(to_orig_coord(p1,self.center), theta)
        p2r = rotate_point(to_orig_coord(p2,self.center), theta)
        p3r = rotate_point(to_orig_coord(p3,self.center), theta)
        p4r = rotate_point(to_orig_coord(p4,self.center), theta)

        new_img_size_x = max([p1r[0], p2r[0], p3r[0], p4r[0]])\
                - min([p1r[0], p2r[0], p3r[0], p4r[0]])
        new_img_size_y = max([p1r[1], p2r[1], p3r[1], p4r[1]])\
                - min([p1r[1], p2r[1], p3r[1], p4r[1]])
        new_ar = np.zeros((new_img_size_x+2, new_img_size_y+2,3),
                dtype=self.ar.dtype)-1
        new_img = Image.from_numpy(new_ar)


        # rotate each pixel to new image
        for x in tqdm(range(self.ar.shape[0])): # i
            for y in range(self.ar.shape[1]): # j

                # np(old) to orgig coord
                x_o, y_o = to_orig_coord((x,y), self.center)

                # rotate point
                x_rot, y_rot = rotate_point((x_o, y_o), theta)

                # orig coord to np(new)
                x_np_new, y_np_new = to_np_coord((x_rot,y_rot), new_img.center)

                assert x_np_new >= 0 and x_np_new < new_img.shape[0],\
                        'x is %d and image is %s'%(x_np_new, new_img.shape)
                assert y_np_new >= 0 and y_np_new < new_img.shape[1],\
                    'y is %d and image is %s'%(y_np_new, new_img.shape)
                new_ar[x_np_new, y_np_new] = self.ar[x,y]

        new_img.ar = new_ar
        #new_img.show()
        return new_img

        # maybe fix aliasing

    def show(self):
        plt.imshow(self.ar)
        plt.show()

    def square(self):
        new_dim = min(self.ar.shape[:2])
        return Image.from_numpy(self.ar[:new_dim, :new_dim])
