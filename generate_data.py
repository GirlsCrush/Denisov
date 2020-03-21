import pygame
import random
import enum
import time
from threading import Timer,Thread,Event
#********************   COLORS  *******************************
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (125, 125, 125)
LIGHT_BLUE = (64, 128, 255)
BLUE = (0, 0, 255)
LIGHT_BLUE_TRANS = (64, 128, 255, 32)
GREEN = (0, 200, 64)
RED = (255, 0, 0)
YELLOW = (225, 225, 0)
PINK = (230, 50, 230)
#********************   CONSTANTS  *******************************
FPS = 60
DISTANCE_PRECISION = 1
game_running = True
PLAYER_X_ERROR = 0.
PLAYER_Y_ERROR = 0.
DISTANCE_ERROR = 0.

#********************   REMOVE PREVIOUS TXT  *******************
rmCommand = "rm reciever*"
import subprocess
subprocess.Popen(rmCommand.split()).communicate()

#******************* CLASS DECLARATIONS *************************
class MyTimer:

   def __init__(self,t,hFunction):
      self.t=t
      self.hFunction = hFunction
      self.thread = Timer(self.t,self.handle_function)

   def handle_function(self):
      self.hFunction()
      self.thread = Timer(self.t,self.handle_function)
      self.thread.start()

   def start(self):
      self.thread.start()

   def cancel(self):
      self.thread.cancel()

            
class Motion(enum.Enum):
    STOP = 0
    LEFT = 1
    UP = 2
    DOWN = 3
    RIGHT = 4

class Player:
    def __init__(self, sc, coord, motion = Motion.STOP, color = BLACK):
        self.sc = sc
        self.coord = list(coord)
        self.motion = motion
        self.color = color
    def move(self):
        if self.motion != Motion.STOP:
            if self.motion == Motion.UP:
                self.coord[1] -= 1
            elif self.motion == Motion.DOWN:
                self.coord[1] += 1
            elif self.motion == Motion.LEFT:
                self.coord[0] -= 1
            elif self.motion == Motion.RIGHT:
                self.coord[0] += 1
    def change_direction(self, keys):
        if keys[pygame.K_UP]:
            self.motion = Motion.UP
        elif keys[pygame.K_DOWN]:
            self.motion = Motion.DOWN
        elif keys[pygame.K_LEFT]:
            self.motion = Motion.LEFT
        elif keys[pygame.K_RIGHT]:
            self.motion = Motion.RIGHT
        else: self.motion = Motion.STOP
    def draw(self):
        pygame.draw.circle(sc, self.color, self.coord, 1, 1)

class Reciever:
    def __init__(self, sc, coord, id, radius = 1, color = LIGHT_BLUE_TRANS) :
        self.sc = sc
        self.id = id
        self.coord = coord
        self.radius = radius
        self.color = color
        f = open("recievers.txt", "a")
        f.write("reciever" + str(id) + ".txt " + str(coord[0]) + " " + str(coord[1]) + "\n")
        f.close()

    def draw(self) :
        pygame.draw.circle(sc, self.color, self.coord, self.radius)
        pygame.draw.circle(sc, BLUE , self.coord, self.radius, 1)
        pygame.draw.circle(sc, RED, self.coord, 1, 1)

    def increment_radius(self) :
        self.radius += 1

    def check_player_pos(self, player) :
        if ((self.coord[0] - player.coord[0]) ** 2 + (self.coord[1] - player.coord[1]) ** 2) ** 0.5 - self.radius < DISTANCE_PRECISION:
            f = open("reciever" + str(self.id) + ".txt", "a")
            f.write(str(player.coord[0]
                    # + random.uniform(-PLAYER_X_ERROR, PLAYER_X_ERROR)
                    ) +
            " " + str(player.coord[1]
                    #   + random.uniform(-PLAYER_Y_ERROR, PLAYER_Y_ERROR)
                      ) +
            " " + str(self.radius
                    #   + random.uniform(-DISTANCE_ERROR, DISTANCE_ERROR)
                      ) +
            " " + str(time.time() - start) +
            "\n")
            f.close()
            self.radius = 0
        elif self.radius > 100 :
            self.radius = 0

def save_player_position() :
    f = open("player_pos.txt", "a")
    f.write(str(player.coord[0]) + " " + str(player.coord[1]) + "\n")
    f.close()

#********************   GLOBAL OBJECTS  *******************************
pygame.init()
sc = pygame.display.set_mode((600, 400), pygame.RESIZABLE)
clock = pygame.time.Clock()
# circle = Reciever(sc, (240, 240))
player = Player(sc, (-100, -100))
recievers = list()
start = time.time()
timer = MyTimer(1.0, save_player_position)
#******************* MAIN LOOP ***************************************
pygame.display.set_caption("Moving point.")

while game_running:
    clock.tick(FPS)
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            game_running = False
        elif i.type == pygame.KEYDOWN or i.type == pygame.KEYUP:
            player.change_direction(pygame.key.get_pressed())
#****************** INPUT RECIEVERS AND PLAYER ********************************
        elif i.type == pygame.MOUSEBUTTONDOWN:
            if i.button == 1:
                recievers.append(Reciever(sc, i.pos, len(recievers)))
            elif i.button == 3:
                player.coord = list(i.pos)
                timer.start()
    pygame.Surface.fill(sc, WHITE)

    player.move()
    player.draw()
    for i in range (0, len(recievers)):
        recievers[i].increment_radius()
        recievers[i].draw()
        recievers[i].check_player_pos(player)

    pygame.display.update()
timer.cancel()