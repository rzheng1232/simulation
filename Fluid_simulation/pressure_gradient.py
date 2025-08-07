import math
import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 800

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
initial_intensity = 255  # Starting intensity of light
max_radius = 400         # Maximum radius of diffusion
list_of_centers = [(250, 250), (100, 100)]  # List of light sources

# Gaussian falloff parameters
sigma = 100  # Controls the spread of the light, adjust this for smoother/diffuse light

# Function to calculate intensity based on distance using Gaussian falloff
def calculate_intensity(distance, max_radius, initial_intensity, sigma):
    if distance >= max_radius:
        return 0.0
    return int(initial_intensity * math.exp(- (distance ** 2) / (2 * sigma ** 2)))

# Create Pygame window
main_screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Smooth Light Diffusion")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Create separate surfaces for layers
gradient_layer = pygame.Surface((WIDTH, HEIGHT))  # Layer for the gradient
visualization_layer = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)  # Layer for visualizations

sample_step = 25
pressure_sample_points = [(i, j) for i in range(0, WIDTH, sample_step) for j in range(0, HEIGHT, sample_step)]

# Function to convert color to grayscale value
def color_to_value(color):
    return round(color[0] / 255, 2)  # Normalize to range [0, 1]

# Initialize font for displaying values
font = pygame.font.Font(None, 16)

# Main loop
running = True
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

while running:
    # Clear the layers
    gradient_layer.fill(BLACK)
    visualization_layer.fill((0, 0, 0, 0))  # Fully transparent background

    # Get mouse position for dynamic light diffusion
    mouse_pos = pygame.mouse.get_pos()
    list_of_centers[0] = mouse_pos  # Update the first center to follow the mouse

    # Draw the gradient on the gradient layer
    for x in range(0, WIDTH, 5):  # Using a step of 5 for performance
        for y in range(0, HEIGHT, 5):
            combined_intensity = 0  # Start with no light
            
            # Calculate intensity from each light source
            for center in list_of_centers:
                distance = math.sqrt((x - center[0])**2 + (y - center[1])**2)
                combined_intensity += calculate_intensity(distance, max_radius, initial_intensity, sigma)
            
            # Cap the combined intensity at 255
            combined_intensity = min(combined_intensity, 255)
            
            # Draw the pixel with the calculated intensity (grayscale)
            color = (combined_intensity, combined_intensity, combined_intensity)
            pygame.draw.rect(gradient_layer, color, pygame.Rect(x, y, 5, 5))

    # Visualize sampling and intensity differences
    for p in pressure_sample_points:
        curr_val = color_to_value(gradient_layer.get_at(p))  # Sample from the gradient layer
        
        # Get adjacent points and calculate intensity differences
        if p[0] + sample_step >= WIDTH or p[0] - sample_step < 0 or p[1] + sample_step >= HEIGHT or p[1] - sample_step < 0:
            diffs_scaled = [0, 0, 0, 0]
            partial_diffs = [0, 0]
            mag = 0
        else:
            pressures = [
                color_to_value(gradient_layer.get_at((p[0], p[1] + sample_step))),  # Top
                color_to_value(gradient_layer.get_at((p[0], p[1] - sample_step))),  # Bottom
                color_to_value(gradient_layer.get_at((p[0] + sample_step, p[1]))),  # Right
                color_to_value(gradient_layer.get_at((p[0] - sample_step, p[1])))   # Left
            ]
            diffs = [a - curr_val for a in pressures]
            diffs_scaled = [5000 * d / sample_step for d in diffs]
            partial_diffs = [-1*abs(diffs_scaled[2]) + abs(diffs_scaled[3]), -1*abs(diffs_scaled[0]) + abs(diffs_scaled[1])]
            mag = math.sqrt(partial_diffs[0]**2 + partial_diffs[1]**2)
        # Draw visualization graphics on the visualization layer
        pygame.draw.circle(visualization_layer, WHITE, p, 1)
        draw_arrow(visualization_layer, (255, 255, 255), (p[0], p[1]), (p[0] - partial_diffs[0], p[1] - partial_diffs[1]), 1, 5, 2)

    # Combine layers by blitting them onto the main screen
    main_screen.blit(gradient_layer, (0, 0))
    main_screen.blit(visualization_layer, (0, 0))

    # Handle events (quit, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the display
    pygame.display.flip()

    # Limit the frame rate to 60 FPS
    clock.tick(60)

# Clean up and quit
pygame.quit()
sys.exit()