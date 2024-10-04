import pygame
import random
import math
import sys

pygame.init()
WIDTH, HEIGHT = 800, 800  # Screen dimensions
BG_COLOR = (0, 0, 0)  # Background color
POINT_COLOR = (0, 0, 255)  # Point color
POINT_RADIUS = 3  # Point radius

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("emergent behavior")
clock = pygame.time.Clock()
objects_array = {}
color_dict = {
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "purple": (128, 0, 128),
    "orange": (255, 165, 0),
    "black": (0, 0, 0),
    "white": (255, 255, 255)
}

def plot_points(objects_arrays):
    for key in objects_arrays.keys():
       points = objects_arrays.get(key)
       for point in points:
           pygame.draw.circle(screen, color_dict[key], (point[0], point[1]), POINT_RADIUS)

def initialize_population(color, amount, space_w, space_h):
    objects_init_position = []
    for i in range(amount):
        # (x, y, velocity x, velocity y)
        objects_init_position.append([random.randint(0, space_w-1), random.randint(0, space_h-1), 0, 0])
    objects_array.update({f'{color}': objects_init_position})

def update_all_particles(rule_array, objects_array):
    for rule in rule_array:
        color1_particles = objects_array[rule[0]]
        color2_particles = objects_array[rule[1]]
        for i, particle1 in enumerate(color1_particles):
            x1 = particle1[0]
            y1 = particle1[1]
            vx1 = particle1[2]
            vy1 = particle1[3]
            fx = 0
            fy = 0
            for j, particle2 in enumerate(color2_particles):
                x2 = particle2[0]
                y2 = particle2[1]
                vx2 = particle2[2]
                vy2 = particle2[3]

                dx = x1 - x2
                dy = y1 - y2
                distance = math.sqrt(dx**2 + dy**2)

                if (distance > 5 and distance < 30):
                    g = rule[2]
                    fx += g * dx
                    fy += g * dy
            if vx1 < 20 and vy1 < 20:
                vx1 = (vx1 + fx)*0.1
                vy1 += (vy1 + fy) * 0.1

            x1 += vx1
            y1 += vy1
            if x1 >= WIDTH or x1 <= 0:
                vx1 *= -1
                #x1 = max(0, min(WIDTH, x1))  # Ensure x1 is within bounds
            if y1 >= HEIGHT or y1 <= 0:
                vy1 *= -1
                #y1 = max(0, min(HEIGHT, y1))
            particle1[0] = x1
            particle1[1] = y1
            particle1[2] = vx1
            particle1[3] = vy1
            color1_particles[i] = particle1
        objects_array[rule[0]] = color1_particles
    return objects_array
            
        
    # for color1 in objects_array.keys():
    #     for i in range(objects_array[color1]):
    #         integrated_force_x = 0
    #         integrated_force_y = 0

    #         for color2 in objects_array.keys():
    #             for j in range(objects_array[color2]):

            

    
    
points_r = initialize_population("red", 200, WIDTH, HEIGHT)
points_g = initialize_population("green", 200, WIDTH, HEIGHT)
# points_b = initialize_population("blue", 100, WIDTH, HEIGHT)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background
    screen.fill(BG_COLOR)
    
    objects_array = update_all_particles([("red", "red", -0.01), ("red", "green", -0.005), ("green", "red", -0.005), ("green", "green", -0.01)], objects_array)

    # Draw points
    plot_points(objects_array)
    
    # Update the display
    pygame.display.flip()

    clock.tick(10)

# Quit Pygame
pygame.quit()
sys.exit()