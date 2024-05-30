import pygame
import math

pygame.init()
pygame.display.set_caption("particle simulation #1")
surface = pygame.display.set_mode((800, 650))
background = pygame.Surface((800, 650))
running = True
t = 0
w = surface.get_width()
h = surface.get_height()
mass = 0
sx = w/2
sy = h/2
vx = 0
vy = 0
ax = 0
ay = 9.8
me = mass * ay * sy
kex = 0.5 * mass * vx**2
key = 0.5 * mass * vy**2
# position at any time t can be calculated with the equation:
# x1 = x0 + v0*t + 0.5 *  a * t^2
while running: 
    surface.fill((0, 0 ,0))
    print(sy)
    if sy >= h:
        print("triggered")
        vy = -vy
        ay = 0
        
        dx = vx * t + 0.5 * ax * t**2
        dy = vy * t + 0.5 * ay * t**2
        ay = -9.8
        sx += dx
        sy += dy
    else:
        dx = vx * t + 0.5 * ax * t**2
        dy = vy * t + 0.5 * ay * t**2
        sx += dx
        sy += dy
    surface.set_at((int(sx), int(sy)), (255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False        
    t += 1/2
    pygame.display.update()


