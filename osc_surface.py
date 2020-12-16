# -*- coding: utf-8 -*-
"""
Created on Sun Nov 22 15:08:24 2020

@author: Hector
"""

import pygame, sys, time
import numpy as np, htools.maths as htm, htools.physx as htp
from pygame.locals import *
import pygame.gfxdraw

#setup pygame
pygame.init()

#set up the window
W_W = 700
W_H = 700
NO_FLAGS = 0
COLOUR_DEPTH = 32
WIN_TITLE="TITLE"
W_S = pygame.display.set_mode((W_W,W_H), NO_FLAGS, COLOUR_DEPTH)
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
CLOCK = 0.01


#set up counter
counter = 0


#system setup
harmonics = [(1,1)]
psi_0_s = [1]
v = 140
a = 0.5
b = 0.2
def normal_psi(x,y,t,harmonic, psi_0):
    ome = v * np.sqrt(((harmonic[0] * np.pi)/a)**2 + ((harmonic[1] * np.pi)/b)**2)
    return psi_0 * np.sin((harmonic[0] * np.pi * x)/a) * np.sin((harmonic[1] * np.pi * y)/b) * np.sin(ome*t)
def psi(x,y,t,harmonics, psi_0_s):
    return sum([normal_psi(x,y,t,harmonic,psi_0) for harmonic,psi_0 in zip(harmonics,psi_0_s)])

#visuals
factor = 500
normal_factor = 1
time_normal = 0.0001
disp_rect = pygame.Rect(W_W / 2 - (factor * a) / 2, W_H / 2 - (factor * b) / 2,factor * a,factor * b)
def normalise_color(t):
    res = []
    for item in t:
        if item < 0:
            res.append(0)
        elif item > 255:
            res.append(255)
        else:
            res.append(item)
    return tuple(res)
#run the loop

while True:
    
    #check for the QUIT event
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    #check for keys
    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]:
        pygame.quit()
        sys.exit()
    
    #maths
    t = counter * time_normal 
    #draw the black background onto the surface
    W_S.fill(BACKGROUND)
   
    for x in range(disp_rect.width):
        for y in range(disp_rect.height):
            pygame.gfxdraw.pixel(W_S,x + disp_rect.left,y + disp_rect.top,normalise_color(tuple([int((psi(x/factor,y/factor,t,harmonics,psi_0_s) * normal_factor + 1) * 128)] * 3)))
    #draw components
    
    
    counter += 1
    time.sleep(CLOCK)
    pygame.display.update()
