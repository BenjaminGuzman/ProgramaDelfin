from PIL import Image
from numpy import array, int32, mean
from pylab import imshow, ginput, show, figure
from matplotlib.pyplot import close
from sys import argv
from classification_mahalanobis import mahalanobisDistance


def getRectangleFromPoints(points):
    p1 = points[0]
    p2 = points[1]
    if p1[0] < p2[0]:
        min_x = p1[0]
        max_x = p2[0]
    else:
        min_x = p2[0]
        max_x = p1[0]

    if p1[1] < p2[1]:
        min_y = p1[1]
        max_y = p2[1]
    else:
        min_y = p2[1]
        max_y = p1[1]
    return [(min_x, min_y), (max_x, max_y)]


def binarizeImage(image, color_samples):
    rows, cols, channels = image.shape
    # do segmentation

def calcCentroid():
    return False


def main(first_image='caminata.jpg', video_path='caminata.mp4'):
    image = array(Image.open(first_image))
    i = 0
    rectangles = []
    while i < 4:
        print("Set {} boundaries (2 points)".format(i))
        fig = figure()
        imshow(image)
        points = int32(ginput(2))
        show()
        close(fig)
        rectangles.append(getRectangleFromPoints(points))
        i = i+1

    i = 0
    centroids = []
    while i < 4:
        x = int(input("# samples: "))
        fig = figure()
        imshow(image)
        points = int32(ginput(x))
        show()
        close(fig)
        centroids.append(calcCentroid(binarizeImage(points)))
        i = i + 1

    print(rectangles)


def needsHelp():
    return argv[1] == '--help' or argv[1] == '-h'


def showHelp():
    print("-----------------------------------")
    print("  Caminata Programa Delfin UPIITA  ")
    print("-----------------------------------")
    print("BenjaminGuzman\n")
    print("Usage: caminata.py [path_to_first_image.jpg] [path_to_video.mp4]\n")


if __name__ == '__main__':
    args_count = len(argv)
    if args_count == 3:
        if needsHelp():
            showHelp()
        else:
            main(argv[1], argv[2])
    elif args_count == 2:
        if needsHelp():
            showHelp()
        else:
            main(argv[1])
    elif args_count == 1:
        main()
    else:
        showHelp()