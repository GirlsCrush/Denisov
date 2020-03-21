import matplotlib
from matplotlib import collections  as mc
import matplotlib.pyplot as plt
import pylab as pl
import numpy as np
import copy

# def lamda(iter) -> float:
#     return 1 / np.log(iter + 1) ** 0.1

# def lamda(iter) -> float:
#     return 1

#****** FUNCTION RETURNING COEF ACCORDING TO CURRENT ITERATION *********
def lamda(iter) -> float:
    return 0.5 + 1 / (2 * float(iter + 1))

def validate_point(point) :
    if (point[0] < 0) :
        point[0] = 0
    if (point[1] < 0) :
        point[1] = 0

#****** MAIN CLASS CONTAINING POINT AND DISTANCE FROM IT (ALSO THE TIME OF MEASUREMENT) *********

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

#*********** MAIN FUNCTION RETURNING APPROXIMATED POINT ACCORDING TO OBS POINTS *************

def approximate_point(points):
    # TODO: modify entry point choice.
    # currentPoint = np.array([points[0].x + points[0].radius / (2. ** 0.5), points[0].y + points[0].radius / (2. ** 0.5)])
    if len(points) < 2:
        return np.array([-1, -1])
    currentPoint = np.array([100, 100])
    prevPoint = np.array([0, 0])
    iteration = 0
    next_func_matrix = np.empty([len(points)])
    func_matrix = np.empty([len(points)])
    for j in range(0, len(points)):
            func_matrix[j] = points[j].func(currentPoint)

    while  iteration < iter_amnt:
        iteration += 1
        prevPoint = copy.copy(currentPoint)
        jacobian = np.zeros([len(points), 2])
        func_matrix = np.empty([len(points)])

        for j in range(0, len(points)):
            jacobian[j][0] = points[j].derivX(currentPoint)
            jacobian[j][1] = points[j].derivY(currentPoint)
            func_matrix[j] = points[j].func(currentPoint)

        A = (jacobian.transpose().dot(jacobian) + np.identity(2) * lamda(iter_amnt))
        currentPoint = currentPoint - np.linalg.inv(A).dot(jacobian.transpose().dot(func_matrix))

        for j in range(0, len(points)):
            next_func_matrix[j] = points[j].func(currentPoint)
        validate_point(currentPoint)
        if np.sum(func_matrix * func_matrix) < np.sum(next_func_matrix * next_func_matrix):
            break
        func_matrix = copy.copy(next_func_matrix)
    return currentPoint

#**************** READING INPUT RECIEVERS AND PLAYER REAL POSITIONS ********************
fn = open("recievers.txt")
recieversLines = fn.readlines()
fn.close()
fn = open("player_pos.txt")
real_player_positions_lines = fn.readlines()
fn.close()

#***************************** ALL THE NEEDED VARIABLES *****************************
iter_amnt = 100
real_player_positions = np.empty([len(real_player_positions_lines), 2])
recievers_approx = np.empty([len(recieversLines), 2])
recievers_real = np.empty([len(recieversLines), 2])
approximate_timesteps = {}
timesteps = {}

#***************************** STORING PLAYER'S REAL POSITIONS *****************************
for i in range(0, len(real_player_positions_lines)):
    input = real_player_positions_lines[i].split()
    real_player_positions[i][0] = int(input[0])
    real_player_positions[i][1] = int(input[1])

#***************************** APPROXIMATING RECIEVERS' POSITIONS *****************************
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
        if timestep not in approximate_timesteps.keys() :
            approximate_timesteps[timestep] = list()
            timesteps[timestep] = list()
        approximate_timesteps[timestep].append(ObservationPoint(recievers_approx[i][0], recievers_approx[i][1], obsPoint.radius))
        timesteps[timestep].append(ObservationPoint(recievers_real[i][0], recievers_real[i][1], obsPoint.radius))


#***************************** ADDITIONAL VARIABLES TO OUTPUT RESULTS *****************************
approximate_player_positions = np.empty([len(approximate_timesteps), 2])
player_positions = np.empty([len(timesteps), 2])

#***************************** STORING RESULTS *****************************
i = 0
for timestep in sorted(approximate_timesteps.keys()) :
    position = approximate_point(approximate_timesteps[timestep])
    if position[0] != -1 :
        approximate_player_positions[i] = position
        i += 1
i = 0
for timestep in sorted(timesteps.keys()) :
    position = approximate_point(timesteps[timestep])
    if position[0] != -1 :
        player_positions[i] = position
        i += 1

print(approximate_player_positions)
print(player_positions)
#***************************** OUTPUTING RESULTS *****************************
fig = plt.figure()
ax = fig.add_subplot(111)
plt.ylim(0, 800)
plt.grid(True)
plt.gca().invert_yaxis()

#***************************** RECIVERS' POSITIONS *****************************
ax.scatter(recievers_real[:, 0], recievers_real[:, 1], c='blue', label='Real recievers\' position')
ax.scatter(recievers_approx[:, 0], recievers_approx[:, 1], c='red', label='Approximated recievers\' position')

#***************************** PLAYER'S REAL AND APPROXIMATED TRAJECTORY *****************************
ax.plot(approximate_player_positions[:, 0], approximate_player_positions[:, 1], linewidth=2, color='black', label='Approx player pos using appox recv pos')
ax.plot(player_positions[:, 0], player_positions[:, 1], linewidth=2, color='red', label='Approx player pos using real recv pos')
ax.plot(real_player_positions[:, 0], real_player_positions[:, 1], linewidth=2, color='blue', label='Real player pos')

plt.legend(prop={'size': 10})
plt.show()
