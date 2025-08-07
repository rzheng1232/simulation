import math
import pygame
import sys
import numpy as np
import random

# to approximate divergence, create grid using the grid boxes as approximates of
# a cell is defined by 4 points, points being the cell's vertices. Each of these poitns are a cvertice of a new box, excluding the points on very right and very bottom
# cycle throug these cells and for each, calculate net flow
# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 500, 500

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
initial_intensity = 30  # Starting intensity of light
max_radius = 30  # Maximum radius of diffusion
m_radius = 100
list_of_centers = [(250, 250)]  # List of light sources

# Gaussian falloff parameters


# Function to calculate intensity based on distance using Gaussian falloff
def calculate_intensity(distance, max_radius, initial_intensity, sigma):
    if distance >= max_radius:
        return 0.0
    return int(initial_intensity * (1 - distance / max_radius))
    #return int(initial_intensity * math.exp(-(distance**2) / (2 * sigma**2)))


# Create Pygame window
main_screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Smooth Light Diffusion")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Create separate surfaces for layers
gradient_layer = pygame.Surface((WIDTH, HEIGHT))  # Layer for the gradient
visualization_layer = pygame.Surface(
    (WIDTH, HEIGHT), pygame.SRCALPHA
)  # Layer for visualizations

sample_step = 10
pressure_sample_points = [
    (i, j) for i in range(0, WIDTH, sample_step) for j in range(0, HEIGHT, sample_step)
]
point_vectors = [[[0, 0] for i in range(WIDTH)] for j in range(HEIGHT)]


# num_particles = 500
# particle_pos = [
#     (random.random() * WIDTH, random.random() * HEIGHT) for part in range(num_particles)
# ]
pWIDTH = 400  # Replace with your desired width
pHEIGHT = 400  # Replace with your desired height

num_particles = 500
particle_pos = [
    (50 + random.random() * pWIDTH, 50 + random.random() * pHEIGHT) for _ in range(num_particles)
]
particle_grads = [(0, 0) for part in range(num_particles)]
particle_vs = [[0, 0] for part in range(num_particles)]
particle_viscs = [(0, 0) for part in range(num_particles)]
# # Calculate rows and columns for the grid
# cols = int(np.sqrt(num_particles * WIDTH / HEIGHT))
# rows = num_particles // cols

# # Spacing between particles
# x_spacing = 0.5 * WIDTH / cols 
# y_spacing = 0.5 * HEIGHT / rows 

# # Generate particle positions
# particle_pos = [
#     (x * x_spacing + x_spacing / 2, y * y_spacing + y_spacing / 2)
#     for x in range(cols)
#     for y in range(rows)
# ]
# while len(particle_pos) < num_particles:
#     particle_pos.append((np.random.uniform(0, WIDTH), np.random.uniform(0, HEIGHT)))


import math
import pygame
def mouse_particle_force(mouse_pos, particle_pos, m_radius, m_val):
    forces = []
    print(m_val)
    for p in particle_pos:
        dx = mouse_pos[0] - p[0]
        dy = mouse_pos[1] - p[1]
        distance = math.sqrt(dx**2 + dy**2)

        if distance < m_radius:
            force_magnitude = smoothing_kernel(m_radius, distance)*m_val/100#-1.5 #(1 - distance / m_radius)  # Linear decay
            force_direction = (-1*dx / distance, -1*dy / distance)  # Normalized direction vector
            force = (force_direction[0] * force_magnitude, force_direction[1] * force_magnitude)
        else:
            force = (0, 0)
        
        forces.append(force)
    return forces

def gaussian_intensity(distance, sigma):
    # Gaussian intensity function
    return math.exp(-distance**2 / (2 * sigma**2))


def smoothing_kernel(radius, dst):
    volume = math.pi * ((radius/2) ** 8) / 4
    value = max(0, radius*radius-dst*dst)
    # if value > 0: print(value * value * value, volume, value * value * value  / volume)
    return value * value * value / volume
def calculate_density(sample_point, particle_pos, printthings=False):
    density = 0
    mass = 1
    dsts = []
    for pos in particle_pos:
        
        dst = np.hypot(pos[0] - sample_point[0], pos[1] - sample_point[1])
        
        influence = smoothing_kernel(max_radius, dst)
        density += mass * influence
        dsts.append(dst)
    # if printthings: print(dsts)
    return density
def density_to_pressure(density, target, p_factor):
    pressure = (density - target) * p_factor
    return pressure
def calculate_gradient(sample_point, particle_pos):
    diff = 1
    # curr_density = calculate_density(sample_point, particle_pos)
    # dx = calculate_density((sample_point[0]+diff, sample_point[1]), particle_pos) - curr_density
    # dy = calculate_density((sample_point[0], sample_point[1]+diff), particle_pos) - curr_density
    curr_density = density_to_pressure(calculate_density(sample_point, particle_pos), 0.5, 0.5)
    dx = density_to_pressure(calculate_density((sample_point[0]+diff, sample_point[1]), particle_pos), 0.5,0.5) - curr_density
    dy = density_to_pressure(calculate_density((sample_point[0], sample_point[1]+diff), particle_pos), 0.5, 0.5) - curr_density
    gradient = (-dx/diff, -dy/diff)
    mag = np.hypot(gradient[0], gradient[1])
    # if mag > 0.1: print(gradient)
    return gradient
visc_strength = 0.08
def calculate_viscosity(curr_ind, close_points, particle_pos):
    visc_f = [0, 0]
    sample_point = particle_pos[curr_ind]
    for i, pos in enumerate(close_points):
        dst = np.hypot(pos[0] - sample_point[0], pos[1] - sample_point[1])
        inf = smoothing_kernel(max_radius, dst)
        visc_f[0] += (particle_vs[i][0] - particle_vs[curr_ind][0])*inf
        visc_f[1] += (particle_vs[i][1] - particle_vs[curr_ind][1])*inf
    # print(visc_f)
    return (visc_f[0] * visc_strength, visc_f[1] * visc_strength)
def draw_arrow(surface, color, start, end, width=3, head_length=15, head_width=10):
    # Draw the shaft of the arrow
    pygame.draw.line(surface, color, start, end, width)

    # Calculate the angle of the arrow
    angle = math.atan2(end[1] - start[1], end[0] - start[0])

    # Calculate the points for the arrowhead
    left = (end[0] - head_length * math.cos(angle - math.pi / 6),
            end[1] - head_length * math.sin(angle - math.pi / 6))
    right = (end[0] - head_length * math.cos(angle + math.pi / 6),
             end[1] - head_length * math.sin(angle + math.pi / 6))
    
    # Draw the arrowhead
    pygame.draw.polygon(surface, color, [end, left, right])
reverse_x = [1 for i in range(num_particles)]
reverse_y = [1 for i in range(num_particles)]
# def update_particle_pos(particles, gradients, m_p, m_on, viscs):
#     TRANSPARENT = (255, 0, 255)  # Transparent color key
#     particle_surf = pygame.Surface((max_radius*2, max_radius*2), pygame.SRCALPHA)  # Transparent surface for particles
#     particle_surf.fill(TRANSPARENT)
#     particle_surf.set_colorkey(TRANSPARENT)
#     pygame.draw.circle(particle_surf, (0, 255, 255, 30), (max_radius, max_radius), max_radius)  # Draw translucent circle

#     new_particles = []
#     if m_on:mouse_force=  mouse_particle_force(m_p, particles, m_radius)
#     else: mouse_force=[(0,0) for p in particles]
    
#     for i, p in enumerate(particles):
#         curr_gradient = gradients[i]
#         curr_visc = viscs[i]
#         px, py = p

#         # Boundary conditions
#         if px > WIDTH - 10:
#             px = WIDTH - 15
#             particle_vs[i][0] *= -0.5
#         if px < 0 + 10:
#             px = 15
#             particle_vs[i][0] *= -0.5
#         if py > HEIGHT - 10:
#             py = HEIGHT - 15
#             particle_vs[i][1] *= -0.5
#         if py < 0 + 10:
#             py = 15
#             particle_vs[i][1] *= -0.5
        
#         # Update velocity and position
#         particle_vs[i][0] += curr_gradient[0] + mouse_force[i][0] + curr_visc[0]
#         particle_vs[i][1] += curr_gradient[1] + mouse_force[i][1]  +0.009 + curr_visc[1]
#         new_p = (px + 100 * particle_vs[i][0], py + 100 * particle_vs[i][1])
        
#         # Calculate the magnitude of the velocity
#         velocity_magnitude = np.hypot(particle_vs[i][0], particle_vs[i][1])
#         # Map the velocity magnitude to a color intensity
#         color_intensity = min(255, int(255 * velocity_magnitude/0.5))  # Multiply by 10 for better visibility
        
#         # Map the intensity to a color (from blue to red)
#         color = (color_intensity, 0, 255 - color_intensity)  # Red for high velocity, Blue for low velocity
        
#         new_particles.append(new_p)
#         # Draw the particle with the velocity-based color
#         # pygame.draw.circle(visualization_layer, color, new_p, 2)
        
#         # Blit the particle surface onto the visualization layer
#         visualization_layer.blit(particle_surf, (new_p[0] - max_radius, new_p[1] - max_radius))

#     return new_particles
def update_particle_pos(particles, gradients, m_p, m_on, m_val, viscs):
    TRANSPARENT = (255, 0, 255)  # Transparent color key
    particle_surf = pygame.Surface((max_radius*2, max_radius*2), pygame.SRCALPHA)  # Transparent surface for particles
    particle_surf.fill(TRANSPARENT)
    particle_surf.set_colorkey(TRANSPARENT)
    
    

    new_particles = []
    if m_on:mouse_force=  mouse_particle_force(m_p, particles, m_radius, m_val)
    else: mouse_force=[(0,0) for p in particles]
    
    for i, p in enumerate(particles):
        curr_gradient = gradients[i]
        curr_visc = viscs[i]
        px, py = p

        # Boundary conditions
        if px > WIDTH - 10:
            px = WIDTH - 10
            particle_vs[i][0] *= -0.5
        if px < 0 + 10:
            px = 10
            particle_vs[i][0] *= -0.5
        if py > HEIGHT - 10:
            py = HEIGHT - 10
            particle_vs[i][1] *= -0.5
        if py < 0 + 10:
            py = 10
            particle_vs[i][1] *= -0.5
        
        # Update velocity and position
        particle_vs[i][0] += curr_gradient[0] + mouse_force[i][0] + curr_visc[0]
        particle_vs[i][1] += curr_gradient[1] + mouse_force[i][1] + curr_visc[1] +0.002
        new_p = (px + 100 * particle_vs[i][0], py + 100 * particle_vs[i][1])
        
        # Calculate the magnitude of the velocity
        velocity_magnitude = np.hypot(particle_vs[i][0], particle_vs[i][1])
        # Map the velocity magnitude to a color intensity
        # print(velocity_magnitude)
        color_intensity = min(255, int(255 * (velocity_magnitude/0.2)**0.33))  # Multiply by 10 for better visibility
        
        # Map the intensity to a color (from blue to red)
        color = (color_intensity, 0, 255 - color_intensity)  # Red for high velocity, Blue for low velocity
        
        new_particles.append(new_p)
        # Draw the particle with the velocity-based color
        pygame.draw.circle(particle_surf, (color[0], color[1], color[2], 50), (max_radius, max_radius), max_radius)  # Draw translucent circle
        pygame.draw.circle(visualization_layer, color, new_p, 2)
        
        # Blit the particle surface onto the visualization layer
        visualization_layer.blit(particle_surf, (new_p[0] - max_radius, new_p[1] - max_radius))

    return new_particles
running = True
# Font for displaying text
font = pygame.font.SysFont(None, 10)
particle_densities = [0 for i in range(num_particles)]

        
mouse_on = False
mousewheel = 0
while running:
    grid = [[[] for i in range(WIDTH)] for j in range(HEIGHT)]

    for particle in particle_pos:
        grid[int(particle[0] / 10)][int(particle[1] / 10)].append(particle)
    # Clear the layers
    gradient_layer.fill(BLACK)
    visualization_layer.fill((0, 0, 0, 0))  # Fully transparent background
    #visualization_layer.fill((0, 0, 0, 10), special_flags=pygame.BLEND_RGBA_SUB)
    # Get mouse position for dynamic light diffusion
    mouse_pos = pygame.mouse.get_pos()

    pygame.draw.circle(visualization_layer, (255, 0, 0), mouse_pos, m_radius, 1)
    density = calculate_density(mouse_pos, particle_pos)

    text_surface = font.render(f"Density: {density:.2f}", True, (255, 255, 255))
    visualization_layer.blit(text_surface, (mouse_pos[0] + 10, mouse_pos[1] + 10))
    list_of_centers[0] = mouse_pos  # Update the first center to follow the mouse

    # curr_gradient = calculate_gradient(mouse_pos, particle_pos)
    # pygame.draw.line(visualization_layer, (255, 255, 255), mouse_pos, (mouse_pos[0] + 500*curr_gradient[0], mouse_pos[1] + 500*curr_gradient[1]))
    for k, particle in enumerate(particle_pos):
        # get points within influence radius:
        # how many "boxes" is the radius:
        boxes = math.ceil(max_radius / 10)
        curr_boxi, curr_boxj = int(particle[0] / 10), int(particle[1] / 10)
        points_to_calc = []
        total_boxes = 0
        # for i in range(min(max(0, curr_boxi - boxes), min(len(grid), curr_boxi + boxes)), max(max(0, curr_boxi - boxes), min(len(grid), curr_boxi + boxes))):
            
        #     for j in range(min(max(0, curr_boxj - boxes), min(len(grid[0]), curr_boxi + boxes)), max(max(0, curr_boxj - boxes), min(len(grid[0]), curr_boxi + boxes))):
        for i in range(max(0, curr_boxi - boxes), min(len(grid), curr_boxi + boxes + 1)):
            for j in range(max(0, curr_boxj - boxes), min(len(grid[0]), curr_boxj + boxes + 1)):
                points_to_calc.extend(grid[i][j])
                total_boxes +=1
        
        # if total_boxes == 0:print(f"{max(0, curr_boxi - boxes)}end: {min(len(grid), curr_boxi + boxes)}, {max(0, curr_boxj - boxes)}end: {min(len(grid[0]), curr_boxi + boxes)}")
        # calculate density at that point only using closest points:
        
        curr_gradient = calculate_gradient(particle, points_to_calc)
        curr_visc= calculate_viscosity(k, points_to_calc, particle_pos)
        # if curr_gradient[0] ==0 and curr_gradient[1] == 0:
        #     print(total_boxes, "beg: {}, end {}")
            # print(calculate_density(particle, points_to_calc, printthings=True))
        particle_grads[k] = curr_gradient
        particle_viscs[k] = curr_visc
        # print(total_boxes)
        # pygame.draw.line(visualization_layer, (255, 255, 255), particle, (particle[0] + 500*curr_gradient[0], particle[1] + 500*curr_gradient[1]))
        # gradient_text = f"{curr_gradient}"#f"({curr_gradient[0]:.2f}, {curr_gradient[1]:.2f})"
        # text_surface = font.render(gradient_text, True, (255, 255, 255))
        # visualization_layer.blit(text_surface, (particle[0]-10, particle[1] + 10))

    particle_pos = update_particle_pos(particle_pos,  particle_grads, mouse_pos, mouse_on, mousewheel, particle_viscs)
    # update_and_draw_pressure(particle_pos, pressure_sample_points, 1, 1)
    # for center in particle_pos:
    # smooth_particles(particle_pos, max_radius, sigma)
    # # Draw the gradient on the gradient layer
    # for x in range(0, WIDTH, 5):  # Using a step of 5 for performance
    #     for y in range(0, HEIGHT, 5):
    #         combined_intensity = 0  # Start with no light

    #         for center in particle_pos:
    #             distance = math.sqrt((x - center[0]) ** 2 + (y - center[1]) ** 2)
    #             combined_intensity += calculate_intensity(
    #                 distance, max_radius, initial_intensity, sigma
    #             )

    #         # Cap the combined intensity at 255
    #         combined_intensity = min(combined_intensity, 255)

    #         # Draw the pixel with the calculated intensity (grayscale)
    #         color = (combined_intensity, combined_intensity, combined_intensity)
    #         pygame.draw.rect(gradient_layer, color, pygame.Rect(x, y, 5, 5))

    # Combine layers by blitting them onto the main screen
    # particle_pos = update_and_draw_particles(particle_pos, point_vectors)
    main_screen.blit(gradient_layer, (0, 0))
    main_screen.blit(visualization_layer, (0, 0))

    # Handle events (quit, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                #send pulse
                mouse_on = not mouse_on
        elif event.type == pygame.MOUSEWHEEL:
            # The `event.y` value is positive for scrolling up and negative for scrolling down
            mousewheel += event.y

    # Update the display
    pygame.display.flip()

    # Limit the frame rate to 60 FPS
    clock.tick(120)

# Clean up and quit
pygame.quit()
sys.exit()
