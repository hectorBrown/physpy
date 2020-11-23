import pygame, sys, time
import numpy as np, htools.maths as htm
from pygame.locals import *

#setup pygame
pygame.init()

#set up the window
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 700
NO_FLAGS = 0
COLOUR_DEPTH = 32
WIN_TITLE="Pendulum"
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

GRAVITY_SCALE = 0.01
TIME_WAIT = 0.01
F_DISP_SCALE = 500
V_DISP_SCALE = 50
BOB_WIDTH = 10
THE_INIT = np.pi / 3;
M = M_F = 1
G = 9.81 * GRAVITY_SCALE

#set up counter
counter = 0


#system setup
O = np.array([WINDOW_WIDTH/2, WINDOW_HEIGHT / 4])
l = 300
r = np.array([l * np.sin(THE_INIT) + O[0], l * np.cos(THE_INIT) + O[1]])
v = np.array([0.0,0.0])
O_F = np.array([0.0, 0.05 * M_F * G]); O_F = np.array([0,0])
O_v = np.array([0.0,0.0])
E_tot = 1/2 * M * htm.mag(v)**2 + M * G * (WINDOW_HEIGHT - r[1])

#visuals
trail_list = []

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
    rel_r = np.array([r[0] - O[0], r[1] - O[1]])
    r = O + l * htm.unit(rel_r)
    the = np.arctan2(rel_r[0], rel_r[1])
    F_g = np.array([0, M * G])
    T_mag = htm.mag(F_g) * np.cos(the) + htm.mag(v - O_v)**2/l
    F_T = T_mag * htm.unit(-rel_r)
    F = F_g + F_T + (1) * np.dot(O_F, rel_r)
    a = F / M
    O_a = O_F / M_F
    O_v += O_a
    O += O_v
    if not v[0] == 0 and v[1] == 0:
        v = np.sqrt((2 * (E_tot - M * G * (WINDOW_HEIGHT - r[1])))/M) * htm.unit(v)
    v += a
    r += v + O_v
    trail_list.append(r.copy())
    if len(trail_list) > 10:
        trail_list = trail_list[1:]
    
    #draw the black background onto the surface
    WindowSurface.fill(BACKGROUND)
   
    #draw components
    
    pygame.draw.arc(WindowSurface, GREEN, pygame.Rect(O[0] - 0.2 * l, O[1] - 0.2 * l, 0.4 * l, 0.4 * l), -np.pi/2, -np.pi / 2 + the) if the > 0 else pygame.draw.arc(WindowSurface, GREEN, pygame.Rect(O[0] - 0.2 * l, O[1] - 0.2 * l, 0.4 * l, 0.4 * l), -np.pi / 2 + the, -np.pi/2)
    pygame.draw.line(WindowSurface, WHITE, O, r)
    pygame.draw.line(WindowSurface, BLUE, r, r + F_DISP_SCALE * F)
    pygame.draw.line(WindowSurface, RED, r, r + V_DISP_SCALE * v)
    #pygame.draw.ellipse(WindowSurface, WHITE, pygame.Rect(r[0] - BOB_WIDTH / 2, r[1] - BOB_WIDTH / 2, BOB_WIDTH, BOB_WIDTH))
    for size, circle in enumerate(trail_list):
        size *= 1/9
        pygame.draw.ellipse(WindowSurface, WHITE, pygame.Rect(circle[0] - (BOB_WIDTH * (size))/2, circle[1] - (BOB_WIDTH * (size))/2, BOB_WIDTH * size, BOB_WIDTH * size))
    
    counter += 1
    time.sleep(TIME_WAIT)
    pygame.display.update()
