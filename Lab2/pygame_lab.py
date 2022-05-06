# ============= Imports ==================
from re import X
import pygame
import numpy as np
# from math import *

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

scale = 100
WIDTH, HEIGHT = 800, 600
screen_center = [WIDTH/2, HEIGHT/2]  # x, y

pygame.display.set_caption("3D projection Lab#2")
screen = pygame.display.set_mode((WIDTH, HEIGHT))



points = []
p1 = np.matrix([-1, -1, 1])
p2 = np.matrix([1, -1, 1])

# # all the cube vertices
# points.append(np.matrix([-1, -1, 1]))
# points.append(np.matrix([1, -1, 1]))
# points.append(np.matrix([1,  1, 1]))
# points.append(np.matrix([-1, 1, 1]))
# points.append(np.matrix([-1, -1, -1]))
# points.append(np.matrix([1, -1, -1]))
# points.append(np.matrix([1, 1, -1]))
# points.append(np.matrix([-1, 1, -1]))

# ============= Matrices ==================


# rotation_y = np.matrix([
#     [np.cos(angle), 0, np.sin(angle)],
#     [0, 1, 0],
#     [-np.sin(angle), 0, np.cos(angle)],
# ])

# matrix = np.matrix([
#     [1, 0, 0],
#     [0, 1, 0],
#     [0, 0, 1]])

projection_matrix = np.matrix([
    [1, 0, 0],
    [0, 1, 0]
])


def rotation_matrix(angle):
    rotation_matrix = np.matrix([
        [np.cos(angle), -np.sin(angle), 0],
        [np.sin(angle), np.cos(angle), 0],
        [0, 0, 1]])

    return rotation_matrix


def translation_matrix(tx, ty):
    translation_matrix = np.matrix([
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]])
    return translation_matrix

# ============= Functions ==================
def drawline(point1, point2):
    # tuple1 = (point1.vec[0, 0], point1.vec[1, 0])
    # tuple2 = (point2.vec[0, 0], point2.vec[1, 0])
    pygame.draw.line(screen, BLACK, (point1.x,
                        point1.y), (point2.x, point2.y), width = 4)


# ============= Classes ==================
class Point():
    def __init__(self, x, y):
        self.vec = np.matrix([[x], [y], [1]])
        self.x = self.vec[0, 0]
        self.y = self.vec[1, 0]

    # def __add__(self, other_point):

    def vecprod(self, matrix):
        self.vec = matrix @ self.vec
        self.x = self.vec[0, 0]
        self.y = self.vec[1, 0]
        return self


class Wheel:
    def __init__(self, radius, x=screen_center[0], y=screen_center[1], color='black'):

        self.radius = radius
        self.diag_coef = radius/np.sqrt(2)
        self.color = color

        self.center = Point(x, y)
        self.cirle_points = []
        self.cirle_points.append( Point(self.center.x, self.center.y + self.radius ))
        self.cirle_points.append( Point(self.center.x + self.diag_coef, self.center.y + self.diag_coef))
        self.cirle_points.append( Point(self.center.x + self.radius, self.center.y ))
        self.cirle_points.append( Point(self.center.x + self.diag_coef, self.center.y - self.diag_coef))
        self.cirle_points.append( Point(self.center.x, self.center.y - self.radius ))
        self.cirle_points.append( Point(self.center.x - self.diag_coef, self.center.y - self.diag_coef))
        self.cirle_points.append( Point(self.center.x - self.radius, self.center.y ))
        #self.cirle_points.append( Point( - self.center.x - self.diag_coef, - self.center.y - self.diag_coef ))

        self.points = list(self.cirle_points)

        #self.cirle_points.append(  )

    def translate_2_origin(self,):
        for i in range(len(self.points)):
            self.points[i].vecprod(
                translation_matrix(-self.center.x, -self.center.y))
        return self

    def translate(self, tx, ty):
        for i in range(len(self.points)):
            self.points[i].vecprod(translation_matrix(tx,ty))
        return self

    def rotate(self, angle):
        cx, cy = self.center.x, self.center.y
        self.translate_2_origin()
        for i in range(len(self.points)):
            self.points[i].vecprod(rotation_matrix(angle))
        self.translate(cx, cy)
        return self



    def draw(self):
        for i in range(len(self.cirle_points)):
            drawline(self.points[i], (self.points[(i+1) % len(self.cirle_points)]) )


if __name__ == '__main__':
    '''Main method'''
    FPS = 30

    # ============= Window and Draw ==================
    pygame.init()
    bg = pygame.Surface(screen.get_size())
    bg.fill((255, 255, 255))
    bg.convert()
    clock = pygame.time.Clock()
    milliseconds = clock.tick(FPS)
    screen.fill(WHITE)
    screen.blit(bg, (0,0))

    w = Wheel(100, x=screen_center[0], y=screen_center[1])

    while True:
        screen.blit(bg, (0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

        # update stuff

        w.translate(0.5,0)
        # w.rotate(0.001)
        # w.translate(0.1, 0)

        w.draw()



        pygame.display.update()
