import pygame
import random
import math
import sys

pygame.init()
WIDTH, HEIGHT = 1200, 1200  # Screen dimensions
BG_COLOR = (0, 0, 0)  # Background color
POINT_COLOR = (0, 0, 255)  # Point color
POINT_RADIUS = 5  # Point radius

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Emergent Behavior")
clock = pygame.time.Clock()
objects_array = {}
# color_dict = {
#     "red": (255, 0, 0),
#     "green": (0, 255, 0),
#     "blue": (0, 0, 255),
#     "yellow": (255, 255, 0),
#     "purple": (128, 0, 128),
#     "orange": (255, 165, 0),
#     "black": (0, 0, 0),
#     "white": (255, 255, 255)
# }
color_dict = {
    "color_1": (255, 0, 255),
    "color_2": (245, 24, 252),
    "color_3": (236, 48, 249),
    "color_4": (227, 72, 246),
    "color_5": (218, 96, 243),
    "color_6": (209, 120, 241),
    "color_7": (200, 144, 238),
    "color_8": (191, 168, 235),
    "color_9": (182, 192, 232),
    "color_10": (173, 216, 230)
}

def plot_points(objects_arrays):
    for key in objects_arrays.keys():
        points = objects_arrays.get(key)
        for point in points:
            pygame.draw.circle(screen, color_dict[key], (int(point[0]), int(point[1])), POINT_RADIUS)

def initialize_population(color, amount, space_w, space_h):
    objects_init_position = []
    for i in range(amount):
        # (x, y, velocity x, velocity y)
        objects_init_position.append([random.randint(0, space_w-1), random.randint(0, space_h-1), 0, 0])
    objects_array[color] = objects_init_position

def update_all_particles(rule_array, objects_array):
    for rule in rule_array:
        color1_particles = objects_array.get(rule[0], [])
        color2_particles = objects_array.get(rule[1], [])
        for i, particle1 in enumerate(color1_particles):
            x1, y1, vx1, vy1 = particle1
            fx = 0
            fy = 0
            for particle2 in color2_particles:
                x2, y2, vx2, vy2 = particle2

                dx = x1 - x2
                dy = y1 - y2
                distance = math.sqrt(dx**2 + dy**2)
                max_distance = 100
                min_distance = 20

                if distance < min_distance:
                    g = 0.5 * (1.5 - distance/min_distance)
                    fx += g * dx * 2
                    fy += g * dy * 2
                
                elif min_distance <= distance <= max_distance:
                    norm_dist = (distance - min_distance) / (max_distance - min_distance)
                    if norm_dist < 0.5:
                        g = rule[2] * norm_dist
                    else:
                        g = rule[2] * (1 - norm_dist)
                    fx += g * dx 
                    fy += g * dy 
            for other_color, other_particles in objects_array.items():
                for j, particle2 in enumerate(other_particles):
                    if rule[0] == other_color and i == j:
                        continue  # Skip the particle itself

                    x2, y2, _, _ = particle2

                    dx = x1 - x2
                    dy = y1 - y2
                    distance = math.sqrt(dx**2 + dy**2)
                    repulsion_distance = 10  # Define the range of repulsion

                    if distance < repulsion_distance:
                        # Repulsive force proportional to 1/distance
                        force_strength = 50 / (distance**2 + 0.1)  # Small constant to avoid division by zero
                        fx += force_strength * dx
                        fy += force_strength * dy
            vx1 = (vx1 + fx) * 0.3 *0.3 
            vy1 = (vy1 + fy) * 0.3 *0.3

            x1 += vx1
            y1 += vy1

            if x1 >= WIDTH or x1 <= 0:
                vx1 *= -1
            if y1 >= HEIGHT or y1 <= 0:
                vy1 *= -1

            particle1[0] = x1
            particle1[1] = y1
            particle1[2] = vx1
            particle1[3] = vy1
            color1_particles[i] = particle1

        objects_array[rule[0]] = color1_particles
    return objects_array

initialize_population("color_1", 100, WIDTH-200, HEIGHT-200)
initialize_population("color_5", 100, WIDTH-200, HEIGHT-200)
# initialize_population("color_7", 175, WIDTH-200, HEIGHT-100)
initialize_population("color_10", 200, WIDTH-200, HEIGHT-200)

running = True
rules = [

        ("color_1", "color_10",  0.2),
        ("color_1", "color_1", -1),
        ("color_1", "color_5", -0.6),
        ("color_5", "color_1", 0.2),
        ("color_5", "color_10", -0.9),
        ("color_10", "color_1", -0.2),
        ("color_10", "color_10", 1),
        ("color_10", "color_5", -0.6),

        
]
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background
    screen.fill(BG_COLOR)
    # rules = [
    #     ("red", "red", 0.5), 
    #     ("purple", "purple", -0.9),
    #     ("purple", "green", 0.12),
    #     ("purple", "red", 0.32),
    #     ("red", "purple", -0.7),
    #     ("green", "purple", 0.5),
    #     ("green", "red", -0.5),
    #     ("green", "green", 0.1),
    #     ("red", "green", -0.3)
    # ]

    objects_array = update_all_particles(rules, objects_array)

    # Draw points
    plot_points(objects_array)
    
    # Update the display
    pygame.display.flip()

    clock.tick(30)

# Quit Pygame
pygame.quit()
sys.exit()
