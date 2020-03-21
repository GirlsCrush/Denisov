import matplotlib
import matplotlib.pyplot as plt
from matplotlib import collections  as mc
import pylab as pl
import numpy as np
import copy
PRECISION = 10e-2
ITERATIONS_AMOUNT = 1000

def lamda(iter) -> float:
    return float(1)

def dist(point1, point2):
    return ((point1[0] - point2[0])** 2 + (point1[1] - point2[1]) ** 2) ** 0.5


class ObservationPoint:
    def __init__(self, input):
        self.x = float(input[0])
        self.y = float(input[1])
        self.radius = float(input[2])
    def func(self, point):
        return (self.x - point[0]) ** 2 + (self.y - point[1]) ** 2 - self.radius ** 2
    def derivX(self, point):
        return 2 * (point[0] - self.x)
        # return 2 * (point[0] - self.x)
    def derivY(self, point):
        return 2 * (point[1] - self.y)
        # return 2 * (point[1] - self.y)

# class Point:
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
#     def dist(self, point):
#         return ((self.x - point.x)** 2 + (self.y - point.y) ** 2) ** 0.5


fn = open("recievers.txt")
recieversLines = fn.readlines()
fn.close()
recievers_approx = np.empty([len(recieversLines), 2])
recievers_real = np.empty([len(recieversLines), 2])

for i in range(0, len(recieversLines)):
    input = recieversLines[i].split()
    recievers_real[i] = [int(input[1]), int(input[2])]
    f = open(input[0])
    pointsLines = f.readlines()
    f.close()
    if len(pointsLines) == 0:
        continue

    points = list()
    for j in range(0, len(pointsLines)):
        input = pointsLines[j].split()
        points.append(ObservationPoint(input))
        # print(str(points[j].x) + ", " + str(points[j].y))

    # TODO: modify entry point choice.
    # currentPoint = np.array([points[0].x + points[0].radius / (2. ** 0.5), points[0].y + points[0].radius / (2. ** 0.5)])
    currentPoint = np.array([0, 0])
    prevPoint = np.array([currentPoint[0] + 2 * PRECISION , currentPoint[1]])
    iter_amnt = 0
    next_func_matrix = np.empty([len(points)])
    func_matrix = np.empty([len(points)])
    for j in range(0, len(points)):
            func_matrix[j] = points[j].func(currentPoint)

    while  iter_amnt < ITERATIONS_AMOUNT:
        iter_amnt += 1
        prevPoint = copy.copy(currentPoint)
        # print(currentPoint)
        # print(prevPoint)
        jacobian = np.zeros([len(points), 2])
        func_matrix = np.empty([len(points)])

        for j in range(0, len(points)):
            jacobian[j][0] = points[j].derivX(currentPoint)
            jacobian[j][1] = points[j].derivY(currentPoint)
            func_matrix[j] = points[j].func(currentPoint)


        # print(jacobian)
        # print(func_matrix)
        A = (jacobian.transpose().dot(jacobian) + np.identity(2) * lamda(iter_amnt))
        currentPoint = currentPoint - np.linalg.inv(A).dot(jacobian.transpose().dot(func_matrix))

        for j in range(0, len(points)):
            next_func_matrix[j] = points[j].func(currentPoint)
        if np.sum(func_matrix * func_matrix) < np.sum(next_func_matrix * next_func_matrix):
            break
        func_matrix = copy.copy(next_func_matrix)
        # print (currentPoint)
        # print(np.linalg.inv(A).dot(jacobian.transpose().dot(func_matrix)))
    recievers_approx[i] = currentPoint
    # print(currentPoint)
    # print(recievers_real[i])
    # print("\n\n")
matplotlib.use("GTK")

print(recievers_approx)
print(recievers_real)
fig = plt.figure()
ax = fig.add_subplot(111)
plt.ylim(0, 400)
plt.grid(True)
plt.gca().invert_yaxis()
ax.plot([recievers_approx[:, 0], recievers_real[:, 0]],
[recievers_approx[:, 1], recievers_real[:, 1]], color='black')
ax.scatter(recievers_real[:, 0], recievers_real[:, 1], c='blue', label='Real recievers\' position')
ax.scatter(recievers_approx[:, 0], recievers_approx[:, 1], c='red', label='Approximated recievers\' position')


plt.legend(prop={'size': 10})
plt.show()
