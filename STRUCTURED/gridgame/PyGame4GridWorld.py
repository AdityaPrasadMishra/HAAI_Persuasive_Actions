#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 14:26:39 2018

@author: ASUAD\amishr28
"""

#Code taken from -> http://programarcadegames.com/index.php?chapter=array_backed_grids&lang=en#step_03
import pygame
#, currentstate, boxposition, finalstate, movearray
class Robot(object):
    def __init__(self):
        self.initialstate = [0,0]
        self.boxposition = [2,2]
        self.finalstate = [1,1]
        self.movearray = ['left', 'left', 'left' ,'obs', 'down', 'down', 'right', 'up', 'right', 'exit']
        self.robowobox = [pygame.image.load('robo1.png'), pygame.image.load('robo1obs.png')]
        self.robowbox = [pygame.image.load('robo2.png'), pygame.image.load('robo2obs.png')]
        self.boximage = [pygame.image.load('box.png')]
        self.pickedupbox = False
        self.currentstate = self.initialstate
        self.currentmove = 0

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BROWN = (194,163,160)
SHINY = (148, 198, 229)
# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 193
HEIGHT = 193

WIDTH_image = 150
HEIGHT_image = 150



# This sets the margin between each cell
MARGIN = 5
# Create a 2 dimensional array. A two dimensional
# array is simply a list of lists.
grid = []
for row in range(5):
    # Add an empty array that will hold each cell
    # in this row
    grid.append([])
    for column in range(5):
        grid[row].append(0)  # Append a cell
#grid[1][5] = 1

pygame.init()
 
# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [1000, 1000]
screen = pygame.display.set_mode(WINDOW_SIZE)
 
pygame.display.set_caption("5X5 Grid")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()


def reDrawGameWindow(robo):
    # Draw the grid
    for row in range(5):
        for column in range(5):
            color = WHITE
            if robo.currentstate == robo.boxposition and [row, column] == robo.currentstate:
                robo.pickedupbox = True
                color = SHINY                
            if [row, column] == robo.finalstate:
                color = BROWN
            pygame.draw.rect(screen,
                 color,
                 [(MARGIN + WIDTH) * column + MARGIN ,
                  (MARGIN + HEIGHT) * row + MARGIN,
                  WIDTH,
                  HEIGHT])
            if [row, column] == robo.currentstate:
                if not robo.pickedupbox:
                    x = (MARGIN + WIDTH) * column + MARGIN * 9
                    y = (MARGIN + HEIGHT) * row + MARGIN * 6
                    if robo.movearray[robo.currentmove] == 'obs':
                        screen.blit(robo.robowobox[1],(x,y))
                    else:
                        screen.blit(robo.robowobox[0],(x,y))
                else: 
                    x = (MARGIN + WIDTH) * column + MARGIN * 9
                    y = (MARGIN + HEIGHT) * row + MARGIN * 6
                    if robo.movearray[robo.currentmove] == 'obs':
                        screen.blit(robo.robowbox[1],(x,y))
                    else:
                        screen.blit(robo.robowbox[0],(x,y))
                    

            if [row, column] == robo.boxposition and not robo.pickedupbox:
                x = (MARGIN + WIDTH) * column + MARGIN + 23
                y = (MARGIN + HEIGHT) * row + MARGIN +  23
                screen.blit(robo.boximage[0],(x,y))            

    pygame.display.update()                       

# -------- Main Program Loop -----------

robo = Robot()
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if(robo.movearray[robo.currentmove] != 'exit'):
                # User clicks the mouse. Get the position
                pos = robo.currentstate
                # Change the x/y screen coordinates to grid coordinates
                column = pos[0] 
                row = pos[1]
                print("Click ", pos, "Grid coordinates: ", row, column) 
                # --- Game logic should go here
                item = robo.movearray[robo.currentmove]
                if item == 'left':
                    robo.currentstate[1] +=1            
                if item == 'right':
                    robo.currentstate[1] -=1
                if item == 'up':
                    robo.currentstate[0] -=1
                if item == 'down':
                    robo.currentstate[0] +=1
                robo.currentmove += 1
        
 
    # --- Screen-clearing code goes here
 
    # Here, we clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
 
    # If you want a background image, replace this clear with blit'ing the
    # background image.
    screen.fill(BLACK)
    reDrawGameWindow(robo)
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
pygame.quit()
