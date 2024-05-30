import pygame
import random
import math
pygame.init()
pygame.display.set_caption("particle simulation #1")
surface = pygame.display.set_mode((800, 600))
background = pygame.Surface((800, 600))
w = surface.get_width()
h = surface.get_height()
background.fill(pygame.Color('#000000'))
is_running = True
x = w/2-10
y = h/2
x2 = w/2+10
y2 = h/2
rand = random.random()*2
dc =0
while is_running:
    #surface.fill((0, 0, 0))
    surface.set_at((int(x), int(y)), (0, 255, 255))
    surface.set_at((int(x+1), int(y)), (0, 255, 255))
    surface.set_at((int(x+1), int(y+1)), (0, 255, 255))
    surface.set_at((int(x), int(y+1)), (0, 255, 255))
    
    surface.set_at((int(x2), int(y2)), (255, 255, 0))
    surface.set_at((int(x2+1), int(y2)), (255, 255, 0))
    surface.set_at((int(x2+1), int(y2+1)), (255, 255, 0))
    surface.set_at((int(x2), int(y2+1)), (255, 255, 0))
    #pygame.draw.rect(surface, (255, 255, 255), pygame.Rect(x, y, 20, 20))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
    if x != x2 and y != y2:
        if x <= w and x >= 0 and x < x2:
            x+=1
        if x <= w and x >= 0 and x > x2:
            x-=1

        if y <= h and y >= 0 and y < y2:
            y+=1
        if y <= h and y >= 0 and y > y2:
            y-=1
            
        rand = random.random()*2
        if x2 <= w and x2 >= 0:
            x2+=round(rand)-1
        rand = random.random()*2
        if y2 <= h and y2 >= 0:
            y2-=round(rand)-1
        
    elif dc < 100:
        
        if x <= w and x >= 0:
            x+=round(rand)-1
        rand = random.random()*4
        if y <= h and y >= 0:
            y-=round(rand)-1
        rand = random.random()*4
        # if x2 <= w and x2 >= 0:
        #     x2+=round(rand)-1
        # rand = random.random()*2
        # if y2 <= h and y2 >= 0:
        #     y2-=round(rand)-1
        # rand = random.random()*2
        dc += 1
    else:
        dc = 0
        
    pygame.display.update()

