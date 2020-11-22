import pygame, sys, time, random
from pygame.locals import *

#setup pygame
pygame.init()

#set up the window
WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 900
NO_FLAGS = 0
COLOUR_DEPTH = 32
WindowSurface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT), FULLSCREEN, COLOUR_DEPTH)
pygame.display.set_caption("Eating Game")

#set up the rectangle
gravRect = pygame.Rect(300,300,50,50)

#set up the speed variables
speedx = 0
speedy = 0

#set gravForce + upForce
gravForce = 5
upForce = 0



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
    if keys[K_w] and gravRect.bottom >= WINDOW_HEIGHT:
        upForce = 15
    if keys[K_a] and gravRect.left >= 0:
        speedx = -5
    if keys[K_d] and gravRect.right <= WINDOW_WIDTH:
        speedx = 5

    
    #calculate speed variables
    speedy = gravForce - upForce
    
    #move by the speed variables every tick
    gravRect.left += speedx
    gravRect.top += speedy

    #make sure you can't go under

    if gravRect.bottom >= WINDOW_HEIGHT:
        gravRect.bottom = WINDOW_HEIGHT

    #move upforce down

    if upForce > 0:
        upForce -= 0.1
    if upForce < 0:
        upForce = 0

    #adjust x speed to friction

    if speedx > 0:
        speedx -= 0.1
        if speedx < 0:
            speedx = 0
    elif speedx < 0:
        speedx += 0.1
        if speedx > 0:
            speedx = 0

    if gravRect.left < 0:
        gravRect.left = 0
    elif gravRect.right > WINDOW_WIDTH:
        gravRect.right = WINDOW_WIDTH
    #draw the black background onto the surface
    WindowSurface.fill(BACKGROUND)

    #print the rectangle to the screen
    pygame.draw.rect(WindowSurface,GREEN,gravRect)
    
    #draw the winodw onto the screen
    pygame.display.update()
    time.sleep(0.004)
