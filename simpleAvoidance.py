import pygame
import math
from SimpleObject import SimpleObject

pygame.init()
pygame.display.set_caption("simpleavoidance")
surface = pygame.display.set_mode((600, 600))
background = pygame.Surface((600, 600))
running = True
t = 0
object = SimpleObject(300, 300, 0, 0, 0)
while running: 
    surface.fill((0, 0 ,0))
    pygame.draw.circle(surface, (255, 255, 255), (object.px, object.py), 5)
    t += 1
    print(object.fFactor)
    object.update()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False     
    

