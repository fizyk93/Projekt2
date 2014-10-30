from __future__ import division             # Division in Python 2.7
import matplotlib
# matplotlib.use('Agg')                       # So that we can render files without GUI
import matplotlib.pyplot as plt

from matplotlib.colors import LightSource
from matplotlib.colors import LinearSegmentedColormap
from numpy import *

from PIL import Image, ImageDraw

font = {'family' : 'times new roman',
        'size' : 12}

plt.rc('font', **font)


def main():

    with open('big.dem') as f:
        f.readline()

        points = zeros(500)

        for line in f:
            temp = line.split(' ')
            temp = array([float(point) for point in temp[0:(len(temp)-1)]])
            points = vstack((points, temp))

        points = points[1:]
        min = points.min()
        max = points.max()
        for n in range(len(points)):
            points[n] = array([(point - min)/(max-min) for point in points[n]])


        angles = empty([len(points), len(points)])
        for y in range(len(points[:len(points)-1])):
            row = []
            for x in range(len(points[y])-1):
                angles[x+1][y+1] = points[x][y]-points[x+1][y+1]

        angles = (angles-angles.min())
        angles /= angles.max()
        angles -= 0.5

        cmap = empty([len(points), len(points), 3])
        for y in range(len(points)):
            for x in range(len(points[y])):
                t = gradient_hsv_map(points[x,y],angles[x,y])
                cmap[x][y] = array([t[0], t[1], t[2]])

        fig = plt.figure()
        plt.subplot(111)
        plt.imshow(cmap)
        plt.xticks([0,100,200,300,400]); plt.yticks([0,100,200,300,400])

        plt.show()
        fig.savefig('map.pdf')


def gradient_hsv_map(v,a):
    if a < 0:
        return hsv2rgb(120 - v*120, 1+3*a, 1)
    else:
        return hsv2rgb(120 - v*120, 1+a, 1-1.5*a)
def hsv2rgb(h, s, v):

    c = v * s
    h = h / 60
    x = c * (1 - abs(h%2 - 1))
    m = v - c


    if h < 1:
        result = (c+m, x+m, m)
    elif h < 2:
        result = (x+m, c+m, m)
    elif h < 3:
        result = (m, c+m, x+m)
    elif h < 4:
        result = (m, x+m, c+m)
    elif h < 5:
        result = (x+m, m, c+m)
    else:
        result = (c+m, m, x+m)

    result = [0. if i<0 else i for i in result]
    result = [1. if i>1 else i for i in result]
    return tuple(result)

def gradient_rgb_bw(v):

    return (v, v, v)


def gradient_rgb_gbr(v):

    if v < 0.5:
        return (0, 1-2*v, 2*v)
    else:
        return (2*(v-0.5), 0, 1-2*(v-0.5))


def gradient_rgb_gbr_full(v):

    if v <= 0.25:
        return (0, 1, 4*v)
    elif v <= 0.5:
        return (0, 1-4*(v-0.25), 1)
    elif v <= 0.75:
        return (4*(v-0.5), 0, 1)
    else:
        return (1, 0, 1-4*(v-0.75))


def gradient_rgb_wb_custom(v):
    if v <= 0.1428:
        return (1, 1-7*v, 1)
    elif v <= 0.2857:
        return (1-7*(v-0.1428), 0, 1)
    elif v <= 0.4285:
        return (0, 7*(v-0.2857), 1)
    elif v <= 0.5714:
        return (0, 1, 1-7*(v-0.4285))
    elif v <= 0.7142:
        return (7*(v-0.5714), 1, 0)
    elif v <= 0.8571:
        return (1, 1-7*(v-0.7142), 0)
    else:
        return (1-7*(v-0.8571), 0, 0)


def gradient_hsv_bw(v):

    return hsv2rgb(0, 0, v)


def gradient_hsv_gbr(v):

    return hsv2rgb(120 + v*240, 1, 1)


def gradient_hsv_unknown(v):

    return hsv2rgb(120 - v*120, 0.5, 1)


def gradient_hsv_custom(v):

    return hsv2rgb(0+360*v, 1-v, 1)



def gradient_to_dict(gradient_func):
    cdict = {'red': [], 'green': [], 'blue': []}

    for i, v in enumerate(linspace(0, 1, 10)):
        color = gradient_func(v)
        cdict['red'].append([v, color[0], color[0]])
        cdict['green'].append([v, color[1], color[1]])
        cdict['blue'].append([v, color[2], color[2]])

    return cdict


if __name__ == '__main__':

    main()
