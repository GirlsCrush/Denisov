import matplotlib
from matplotlib import collections  as mc
# matplotlib.use("GTK")
import matplotlib.pyplot as plt
import pylab as pl
import numpy as np
import copy
PRECISION = 10e-4
ITERATIONS_AMOUNT = 100

# def lamda(iter) -> float:
#     return 1 / np.log(iter + 1) ** 0.1

def lamda(iter) -> float:
    return 0.5 + 1 / (2 * float(iter + 1))

# def lamda(iter) -> float:
#     return 1

def dist(point1, point2):
    return ((point1[0] - point2[0])** 2 + (point1[1] - point2[1]) ** 2) ** 0.5


class ObservationPoint:
    def __init__(self, x, y, radius, timestamp = 0):
        self.x = x
        self.y = y
        self.radius = radius
        self.timestamp = timestamp
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

def approximate_point(points):
    # TODO: modify entry point choice.
    # currentPoint = np.array([points[0].x + points[0].radius / (2. ** 0.5), points[0].y + points[0].radius / (2. ** 0.5)])
    if len(points) < 2:
        return np.array([-1, -1])
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
    return currentPoint

fn = open("recievers.txt")
recieversLines = fn.readlines()
fn.close()
recievers_approx = np.empty([len(recieversLines), 2])
recievers_real = np.empty([len(recieversLines), 2])
timesteps = {}



for i in range(0, len(recieversLines)):
    input = recieversLines[i].split()
    recievers_real[i] = [int(input[1]), int(input[2])]
    f = open(input[0])
    pointsLines = f.readlines()
    f.close()
    if len(pointsLines) == 0:
        continue

    obsPoints = list()
    for j in range(0, len(pointsLines)):
        input = pointsLines[j].split()
        obsPoints.append(ObservationPoint(int(input[0]),
                                          int(input[1]),
                                          int(input[2]),
                                          int(float(input[3]))
                                          ))
        # print(str(obsPoints[j].x) + ", " + str(obsPoints[j].y))

    recievers_approx[i] = approximate_point(obsPoints)
    for obsPoint in obsPoints:
        timestep = int(obsPoint.timestamp)
        if timestep not in timesteps.keys() :
            timesteps[timestep] = list()
        timesteps[timestep].append(ObservationPoint(recievers_approx[i][0], recievers_approx[i][1], obsPoint.radius))

        # timesteps[timestep].append([currentPoint, reciever.radius])
    # print(currentPoint)
    # print(recievers_real[i])
    # print("\n\n")
players_positions = np.empty([len(timesteps), 2])
i = 0
for timestep in sorted(timesteps.keys()) :
    position = approximate_point(timesteps[timestep])
    if position[0] != -1 :
        players_positions[i] = position
        i += 1


print(recievers_approx)
# print(recievers_real)
# print(players_positions)
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
