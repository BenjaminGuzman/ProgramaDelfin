# -*- coding: utf-8 -*-

from PIL import Image
from numpy import array, sqrt, int32
from pylab import linalg, figure, imshow, show, ginput
from math import sqrt as squareRoot
#-----------------------
import numpy as np
import matplotlib.pyplot as plt
#-----------------------

import sys


def euclideanDistance(p1, p2):
    return squareRoot(abs((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2))


def mahalanobisDistance(color, avarage, covariance):
    # mahalanobis distance: sqrt((x - y)^T * cov^-1 * (x - y))
    # x: color
    # y: avarage

    # linalg: linear algebra

    # d1: x - y * cov^-1
    d1 = (color - avarage.dot(linalg.inv(covariance)))

    # d2: (x -y)^T
    d2 = d1.dot((color - avarage).T)

    d3 = sqrt(d2)

    return d3

def getSamples(image):
    x = True
    while x is True:
        try:
            x = int(input("¿Cuántas muestras tomarás? (only digits): "))
            if x <= 0:
                print("Only positive integers please\n")
                x = True
            elif x < 5:
                print("Take more than 4 samples\n")
                x = True
            elif x > 100:
                print("Take less than 100 samples\n")
                x = True
        except ValueError:
            print("Only integers please!\nIf you wrote x.0 please write only x")
            x = True

    fig = figure()
    imshow(image)

    # ginput: graphic input
    pos = int32(ginput(x))

    plt.close(fig)

    return pos

def segmentate(image, sample_points, center, radius):
                # y primero porque el array contiene las filas primero, dentro de estas estan las columnas
    values = image[sample_points[:, 1], sample_points[:, 0]]

    rows, cols, channels = image.shape

    covariance = np.cov(values.T, ddof=0)

    # mean: media ~ promedio
    mean = np.mean(values, axis=0)

    boundaries = {'x1': 10000000000, 'y1': 10000000000, 'x2': 0, 'y2': 0}

    start_row = int(round(center[1] - radius if center[1] - radius > 0 else 0))
    start_col = int(round(center[0] - radius if center[0] - radius > 0 else 0))
    end_row = int(round(center[1] + radius if center[1] + radius < rows else rows - 1))
    end_col = int(round(center[0] + radius if center[0] + radius < cols else cols - 1))

    for i in range(start_row, end_row + 1):
        for j in range(start_col, end_col + 1):

            if euclideanDistance((j, i), center) <= radius: # if pixel is in the circle

                # from the i row, take the j col, and then take all the rgb values
                pixel = image[i, j, :]

                distance = mahalanobisDistance(pixel, mean, covariance)

                # output_image[i, j, :] = 255 if distance > 15 else 0

                if distance <= 60:  # if pixel is from the object
                    if j < boundaries['x1']:
                        boundaries['x1'] = j
                    elif i < boundaries['y1']:
                        boundaries['y1'] = i
                    elif j > boundaries['x2']:
                        boundaries['x2'] = j
                    elif i > boundaries['y2']:
                        boundaries['y2'] = i

                    image[i, j, :] = 255
                else:
                    image[i, j, :] = 0

        print(str(i / end_row * 100) + '%')
    return image, boundaries


def main(image_path='./pic.jpg'):
    try:
        image = array(Image.open(image_path))
        # image:

        # [ -> image array
        #   [[R, G, B]...[R, G, B]] -> row array
        #   [[R, G, B]...[R, G, B]] -> row array
        # ] -> image array

        # [R, G, B] -> pixel array
    except FileNotFoundError as err:
        print("FILE NOT FOUND !!!\n")
        print(err.strerror + ": " + err.filename)
        exit(1)

    # channels: 3 if it's rgb
    rows, cols, channels = image.shape

    output_image = image

    x = True
    while x is True:
        try:
            x = int(input("¿Cuántas muestras tomarás? (only digits): "))
        except ValueError:
            print("Only integers please!\n")
            x = True

    figure()
    imshow(image)

    # ginput: graphic input
    pos = int32(ginput(x))

    # pos[:, 1]: all values from last col   Y
    # pos[:, 0]: all values from first col  X
    values = image[pos[:, 1], pos[:, 0]]
    
    show()
    
    covariance = np.cov(values.T, ddof=0)
    
    # mean: media ~ promedio
    mean = np.mean(values, axis=0)

    boundaries = {'x1': -1, 'y1': -1, 'x2': 0, 'y2': 0}

    for i in range(rows):
        for j in range(cols):

            # from the i row, take the j col, and then take all the rgb values
            pixel = image[i, j, :]

            distance = mahalanobisDistance(pixel, mean, covariance)

            #output_image[i, j, :] = 255 if distance > 15 else 0

            if distance <= 30: # if pixel is from the object
                if j < boundaries['x1']:
                    boundaries['x1'] = j
                elif i < boundaries['y1']:
                    boundaries['y1'] = i
                elif j > boundaries['x2']:
                    boundaries['x2'] = j
                elif i > boundaries['y2']:
                    boundaries['y2'] = i

                output_image[i, j, :] = 255
            else:
                output_image[i, j, :] = 0

        print(str(i / rows * 100) + '%')

    print('width: ' + str(boundaries['x2'] - boundaries['x1']) + ' px')
    print('height: ' + str(boundaries['y2'] - boundaries['y1']) + ' px')
    print('\n' + str(boundaries))

    figure()
    imshow(output_image)
    show()

    print(str(rows) + ' ' + str(cols) + ' ' + str(values))

    
if __name__ == '__main__':
    length = len(sys.argv)
    # if the image_path is given, pass it
    if length == 2:
        main(sys.argv[1])
    elif length == 1:
        main()
    else:
        print("ERROR.\nUsage: classification_mahalanobis.py [image_path]")
