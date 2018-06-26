from PIL import Image
from pylab import ginput, figure, imshow
import matplotlib.pyplot as plt
from numpy import int32, array


def calculateDistancePx(p1, p2):
    return p2[1] - p1[1]

def main():
    image_path = input("Image path: ")
    if len(image_path) == 0:
        image_path = './conos.jpg'

    samples = int(input("# Samples: "))

    image = Image.open(image_path)

    figure()
    imshow(image)

    points = int32(ginput(samples))

    print(points)

    distances = [0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0 ,0]

    print("Input distances, starting from nearest")

    for i in range(samples):
        distances[i] = float(input("Distance: "))

    for i in range(0, samples, 2):
        print("\t"+str(calculateDistancePx(points[i], points[i+1])) + "\t->\t" + str(distances[i]))

if __name__ == '__main__':
    main()