from PIL import Image
from pylab import ginput, figure, imshow
import matplotlib.pyplot as plt
from numpy import int32, array


class Graph:
    table = []
    eqn = None

    def add2Table(self, width, distance):
        self.table.append([width['px'], width['real'], distance])

    def printTable(self):
        print("\n|\tPixels\t|\treal\t|\tdistance\t|")
        for i in range(len(self.table)):
            print("|\t"+str(self.table[i][0])+"\t|\t"+str(self.table[i][1])+"\t|\t"+str(self.table[i][2])+"\t|")


def getPoints(image_arr):
    fig = figure()
    imshow(image_arr)
    points = int32(ginput(2))
    plt.close(fig)
    return points[0], points[1]


def main():
    width = {'px': -1, 'real': -1}
    height = {'px': -1, 'real': -1}

    image_path = input("Image path: ")

    graph = Graph()

    while image_path != 'q':

        times_width = 0
        times_height = 0

        image = Image.open(image_path)

        distance = float(input("Distance: "))

        while times_width != 3:

            print("Width " + str(times_width))

            p1, p2 = getPoints(image)
            width['px'] = p2[0] - p1[0]
            width['real'] = float(input("Real width: "))

            graph.add2Table(width, distance)

            times_width = times_width + 1

        while times_height != 3:

            print("Height " + str(times_height))

            p1, p2 = getPoints(image)
            height['px'] = p2[1] - p1[1]
            height['real'] = float(input("Real height: "))

            graph.add2Table(height, distance)

            times_height = times_height + 1

        graph.printTable()

        image_path = input("Image path: ")

    graph.printTable()


if __name__ == '__main__':
    main()
