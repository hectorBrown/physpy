# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 20:48:19 2020

@author: Hector
"""

import pygame, sys, time, random, math
import numpy as np, htools.maths as htm, htools.physx as htp
from pygame.locals import *
import pygame.gfxdraw

G = 9.81 * 0.0001
e = 0.7
class Ball:
    def __init__(self, m, r, x, v, colour, bound):
        self.m = m
        self.r = r
        self.x = np.array(x)
        self.v = np.array(v)
        self.bound = bound
        self.colour = colour
    def propagate(self):
        self.v[1] += G
        #self.v[0] += G
        self.x += self.v
        if self.get_rect().right >= self.bound.right:
            self.v[0] *= -e
            self.set_right(self.bound.right)
        elif self.x[0] - self.r <= self.bound.left:
            self.v[0] *= -e
            self.x[0] = self.bound.left + self.r
        if self.get_rect().bottom >= self.bound.bottom:
            self.v[1] *= -e
            self.set_bottom(self.bound.bottom)
        elif self.x[1] - self.r <= self.bound.top:
            self.v[1] *= -e
            self.x[1] = self.bound.top + self.r
    def get_rect(self):
        return pygame.Rect(*(self.x - self.r), *([2 * self.r] * 2))
    def set_right(self, x):
        self.x[0] = x - self.r
    def set_bottom(self, x):
        self.x[1] = x - self.r
    def collide(self, ball):
        rel_x = self.x - ball.x
        if htm.mag(rel_x) <= self.r + ball.r:
            self.x = (self.r + ball.r) * htm.unit(rel_x) + ball.x
            trans_v_1 = np.array([np.dot(self.v, htm.unit(htm.perp2d(rel_x))), np.dot(self.v,htm.unit(rel_x))])
            trans_v_2 = np.array([np.dot(ball.v, htm.unit(htm.perp2d(rel_x))), np.dot(ball.v,htm.unit(rel_x))])
            trans_v_1_f = (self.m - e * ball.m)/(self.m + ball.m) * trans_v_1[1] + ((1 + e) * ball.m)/(self.m + ball.m) * trans_v_2[1]
            trans_v_2_f = ((1 + e) * self.m)/(self.m + ball.m) * trans_v_1[1] + (ball.m - e * self.m)/(self.m + ball.m) * trans_v_2[1]
            trans_v_1[1] = trans_v_1_f; trans_v_2[1] = trans_v_2_f          
            the = np.arctan2(*rel_x)
            self.v = htm.rotate2d(trans_v_1, the)
            ball.v = htm.rotate2d(trans_v_2, the)
        
#setup pygame
pygame.init()

#set up the window
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000
NO_FLAGS = 0
COLOUR_DEPTH = 32
WIN_TITLE="Collisions"
WindowSurface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT), NO_FLAGS, COLOUR_DEPTH)
pygame.display.set_caption(WIN_TITLE)

#set up the colours
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
CYAN = (0,255,255)
MAGENTA = (255,0,255)
BACKGROUND = BLACK

#other constants
TIME_WAIT = 0.0001
V_SCALE = 0.1

#set up counter
counter = 0


#system setup
balls = []
for i in range(0, 30):
    mass = np.random.randint(1,20)
    balls.append(Ball(mass, ((mass - 1) * 5) + 10, np.array([float(np.random.randint(50, WINDOW_WIDTH - 50)), float(np.random.randint(50, WINDOW_HEIGHT - 50))]), np.array([np.random.randint(-30,30) * V_SCALE, np.random.randint(-30, 30) * V_SCALE]), (np.random.randint(0,256),np.random.randint(0,256),np.random.randint(0,256)), pygame.Rect(0,0,WINDOW_WIDTH, WINDOW_HEIGHT)))
# for x in range(100, WINDOW_WIDTH - 100, 120):
#     for y in range(100, WINDOW_HEIGHT - 500, 120):
#         balls.append(Ball(1, np.random.randint(40,80), np.array([float(x) + np.random.randint(-1,2) * 0.01,float(y)]),np.array([np.random.randint(-30,30) * 0.01,np.random.randint(-30,30) * 0.01]), tuple([np.random.randint(0, 256) for x in range(3)]), pygame.Rect(0,0,WINDOW_WIDTH, WINDOW_HEIGHT)))
# balls.append(Ball(10,40,np.array([WINDOW_WIDTH / 4, WINDOW_HEIGHT / 2]), np.array([0.1, 0]), RED, pygame.Rect(0,0,WINDOW_WIDTH, WINDOW_HEIGHT)))
# balls.append(Ball(1,40,np.array([3 * WINDOW_WIDTH / 4, WINDOW_HEIGHT / 2]), np.array([-0.1, 0]), BLUE, pygame.Rect(0,0,WINDOW_WIDTH, WINDOW_HEIGHT)))

# balls.append(Ball(1,100,np.array([WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2]), np.array([-0.1,-0.1]), RED, pygame.Rect(0,0,WINDOW_WIDTH, WINDOW_HEIGHT)))
# balls.append(Ball(1,10,np.array([WINDOW_WIDTH / 4, WINDOW_HEIGHT / 4]), np.array([0.1,0.1]), BLUE, pygame.Rect(0,0,WINDOW_WIDTH, WINDOW_HEIGHT)))
#visuals

#run the game loop
while True:
    
    #check for the QUIT event
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]:
        pygame.quit()
        sys.exit()
    
    #maths
    
    for ball in balls:
        ball.propagate()
    for i,ball in enumerate(balls):
        for ball2 in balls[i + 1:]:
            ball.collide(ball2)
    
    #draw the black background onto the surface
    WindowSurface.fill(BACKGROUND)
    #draw components
    for ball in balls:
        pygame.gfxdraw.filled_ellipse(WindowSurface, *[int(x) for x in ball.x], *([ball.r] * 2), ball.colour)
        pygame.gfxdraw.aaellipse(WindowSurface, *[int(x) for x in ball.x], *([ball.r] * 2), ball.colour)

    counter += 1
    #time.sleep(TIME_WAIT)
    pygame.display.update()