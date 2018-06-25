from sys import argv as args, stderr
from PIL import Image, ImageFilter
from pylab import imshow, figure, show
from numpy import array
import classification_mahalanobis as segmentation


def convertPx2Cm(distance, pixels):
    # 744.079888132296 cuando la  imagen es de 540 * 960
    return distance * pixels / 744.079888132296


def main(image_path='./pic.jpg'):
    distance = True
    while distance is True:
        try:
            distance = float(input("Distance to object: "))
            if distance < 0:
                print("NON POSITIVE DISTANCE", file=stderr)
                distance = True
            elif distance == 0:
                print("DISTANCE CANNOT BE 0", file=stderr)
                distance = True
        except ValueError:
            distance = True
            print("NOT A VALID DISTANCE !!!", file=stderr)
    try:
        image = Image.open(image_path)
    except FileNotFoundError as err:
        print("FILE NOT FOUND !!!\n", file=stderr)
        print(err.strerror + ": " + err.filename, file=stderr)
        exit(1)

    image = image.filter(ImageFilter.SHARPEN)
    image = array(image)

    sample_points = segmentation.getSamples(image)

    print("----------------")
    print("  SEGMENTATION  ")
    print("----------------")
    image_segmented, boundaries = segmentation.segmentate(image, sample_points)

    w, h = boundaries['x2'] - boundaries['x1'], boundaries['y2'] - boundaries['y1']

    figure()
    imshow(image_segmented)
    show()

    rows, cols, channels = image.shape

    print("width: " + str(w) + " px\theight: " + str(h) + " px\n")
    w = convertPx2Cm(distance, w)
    h = convertPx2Cm(distance, h)
    if cols != 540:
        print("Image width is not 540, scaling factor: " + str(540 / cols))
        w = w * (540 / cols)
    if rows != 960:
        print("Image height is not 960, scaling factor: " + str(960 / rows))
        h = h * (960 / rows)
    print("width: " + str(w) + " cm\theight: " + str(h) + " cm")


if __name__ == '__main__':
    length = len(args)
    if length == 2:
        main(args[1])
    elif length == 1:
        main()
    else:
        print("ERROR.\n\nUsage: dimensions.py [image_path]")