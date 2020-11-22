# -*- coding: utf-8 -*-
"""
Created on Sun Nov 22 15:08:24 2020

@author: Hector
"""

import pygame, sys, time, random
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


#visuals


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
    
    #draw the black background onto the surface
    W_S.fill(BACKGROUND)
   
    #draw components
    
    
    counter += 1
    time.sleep(CLOCK)
    pygame.display.update()