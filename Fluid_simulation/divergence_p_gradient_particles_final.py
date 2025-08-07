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
WIDTH, HEIGHT = 800, 800

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
initial_intensity = 255  # Starting intensity of light
max_radius = 400  # Maximum radius of diffusion
list_of_centers = [(250, 250), (400, 400), (0, 0)]  # List of light sources

# Gaussian falloff parameters
sigma = 100  # Controls the spread of the light, adjust this for smoother/diffuse light


# Function to calculate intensity based on distance using Gaussian falloff
def calculate_intensity(distance, max_radius, initial_intensity, sigma):
    if distance >= max_radius:
        return 0.0
    return int(initial_intensity * math.exp(-(distance**2) / (2 * sigma**2)))


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

sample_step = 25
pressure_sample_points = [
    (i, j) for i in range(0, WIDTH, sample_step) for j in range(0, HEIGHT, sample_step)
]
point_vectors = [[[0, 0] for i in range(WIDTH)] for j in range(HEIGHT)]


# Function to convert color to grayscale value
def color_to_value(color):
    return -1 * round(color[0] / 255, 2)  # Normalize to range [0, 1]


def calculate_divergence(topleft, vector_field):
    all_points = [
        topleft,
        (p[0] + sample_step, p[1]),
        (p[0], p[1] + sample_step),
        (p[0] + sample_step, p[1] + sample_step),
    ]
    all_vectors = [
        vector_field[all_points[0][0]][all_points[0][1]],
        vector_field[all_points[1][0]][all_points[1][1]],
        vector_field[all_points[2][0]][all_points[2][1]],
        vector_field[all_points[3][0]][all_points[3][1]],
    ]
    # avergae components and multiply by length of side
    all_vectors_faces = [
        (np.array(all_vectors[0]) + np.array(all_vectors[1])) / 2,
        (np.array(all_vectors[1]) + np.array(all_vectors[3])) / 2,
        (np.array(all_vectors[3]) + np.array(all_vectors[2])) / 2,
        (np.array(all_vectors[2]) + np.array(all_vectors[0])) / 2,
    ]

    all_flux = [
        all_vectors_faces[0][1] * sample_step,
        all_vectors_faces[1][0] * sample_step,
        all_vectors_faces[2][1] * sample_step,
        all_vectors_faces[3][0] * sample_step,
    ]
    divergence = (all_flux[0] + all_flux[1] + all_flux[2] + all_flux[3]) / (
        sample_step * sample_step
    )
    text_surface = font.render(f"{divergence:.2f}", True, WHITE)
    center = (
        (topleft[0] + topleft[0] + sample_step) // 2,
        (topleft[1] + topleft[1] + sample_step) // 2,
    )
    # print((int(120 + 120 * divergence / 5), 0, 0))
    pygame.draw.rect(
        visualization_layer,
        map_divergence_to_color(divergence),
        pygame.Rect(topleft[0], topleft[1], sample_step, sample_step),
    )
    text_rect = text_surface.get_rect(center=center)
    visualization_layer.blit(text_surface, text_rect)
    return divergence


def map_divergence_to_color(divergence):
    """
    Maps the divergence value to a gradient color.
    - Negative divergence (e.g., -5): Blue
    - Zero divergence: White
    - Positive divergence (e.g., +5): Red
    """
    # Normalize divergence to the range [-5, 5]
    normalized_div = max(-5, min(5, divergence))
    if normalized_div < 0:
        # Map negative values to blue-white gradient with a more gradual transition
        intensity = int(255 * (1 + normalized_div / 5))  # Scale from blue to white
        blue_intensity = max(127, intensity)  # Ensure blue doesn't get too dark
        return (blue_intensity, blue_intensity, 255)  # More gradual blue gradient
    else:
        # Map positive values to white-red gradient
        intensity = int(255 * (1 - normalized_div / 5))  # Scale from white to red
        return (255, intensity, intensity)  # Red channel


def map_divergence_to_color(divergence):
    """
    Maps the divergence value to a gradient color with smoother transitions.
    - Negative divergence (e.g., -5): Black to Blue
    - Zero divergence: Black
    - Positive divergence (e.g., +5): Red to Black
    """
    # Normalize divergence to the range [-5, 5]
    normalized_div = max(-5, min(5, divergence))

    if normalized_div < 0:
        # Map negative values to black-blue gradient
        intensity = int(255 * ((-normalized_div / 5) ** 0.5))  # Quadratic scaling
        return (0, 0, intensity)  # Blue gradient
    elif normalized_div > 0:
        # Map positive values to red-black gradient
        intensity = int(255 * ((normalized_div / 5) ** 0.5))  # Quadratic scaling
        return (intensity, 0, 0)  # Red gradient
    else:
        # Zero divergence maps to black
        return (0, 0, 0)


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
    left = (
        end[0] - head_length * math.cos(angle - math.pi / 6),
        end[1] - head_length * math.sin(angle - math.pi / 6),
    )
    right = (
        end[0] - head_length * math.cos(angle + math.pi / 6),
        end[1] - head_length * math.sin(angle + math.pi / 6),
    )

    # Draw the arrowhead
    pygame.draw.polygon(surface, color, [end, left, right])


num_particles = 1000
particle_pos = [
    (random.random() * WIDTH, random.random() * HEIGHT) for part in range(num_particles)
]



def update_and_draw_particles(particle_pos, vector_field):
    randomnized = False
    new_poses = []
    for part in particle_pos:
        if (
            part[0] + 2 * sample_step >= WIDTH
            or part[0] - 2 * sample_step < 0
            or part[1] + 2 * sample_step >= HEIGHT
            or part[1] - 2 * sample_step < 0
        ):
            part = (random.random() * WIDTH, random.random() * HEIGHT)
            randomnized = True
        closest_point = (
            max(0, min(sample_step * round(part[0] / sample_step), WIDTH - sample_step)),
            max(0, min(sample_step * round(part[1] / sample_step), HEIGHT - sample_step)),
        )

        def clamp_point(point):
            """Clamp point to ensure it is within bounds."""
            return (
                max(0, min(point[0], WIDTH - 1)),
                max(0, min(point[1], HEIGHT - 1)),
            )

        def get_valid_vectors(points):
            """Retrieve vectors, ensuring points are within bounds."""
            valid_vectors = []
            for p in points:
                clamped_p = clamp_point(p)
                valid_vectors.append(vector_field[clamped_p[0]][clamped_p[1]])
            return valid_vectors

        if part[0] < closest_point[0]:
            if part[1] < closest_point[1]:
                # Upper left
                points_to_get = [
                    closest_point,
                    clamp_point((closest_point[0] - sample_step, closest_point[1] - sample_step)),
                    clamp_point((closest_point[0] - sample_step, closest_point[1])),
                    clamp_point((closest_point[0], closest_point[1] - sample_step)),
                ]
            else:
                # Lower left
                points_to_get = [
                    closest_point,
                    clamp_point((closest_point[0] - sample_step, closest_point[1] + sample_step)),
                    clamp_point((closest_point[0] - sample_step, closest_point[1])),
                    clamp_point((closest_point[0], closest_point[1] + sample_step)),
                ]
        else:
            if part[1] < closest_point[1]:
                # Upper right
                points_to_get = [
                    closest_point,
                    clamp_point((closest_point[0] + sample_step, closest_point[1] - sample_step)),
                    clamp_point((closest_point[0] + sample_step, closest_point[1])),
                    clamp_point((closest_point[0], closest_point[1] - sample_step)),
                ]
            else:
                # Lower right
                points_to_get = [
                    closest_point,
                    clamp_point((closest_point[0] + sample_step, closest_point[1] + sample_step)),
                    clamp_point((closest_point[0] + sample_step, closest_point[1])),
                    clamp_point((closest_point[0], closest_point[1] + sample_step)),
                ]

        # Get valid vectors and compute distances
        vectors_to_interpolate = get_valid_vectors(points_to_get)
        distances_to_points = [
            math.sqrt((part[0] - point[0]) ** 2 + (part[1] - point[1]) ** 2)
            / math.sqrt(8 * sample_step**2)
            for point in points_to_get
        ]

        # Interpolate final vector
        final_vector = [0, 0]
        for i, v in enumerate(vectors_to_interpolate):
            final_vector[0] += distances_to_points[i] * v[0]
            final_vector[1] += distances_to_points[i] * v[1]

        newpos = (part[0] - final_vector[0], part[1] - final_vector[1])
        if (
            newpos[0] + 2 * sample_step >= WIDTH
            or newpos[0] - 2 * sample_step < 0
            or newpos[1] + 2 * sample_step >= HEIGHT
            or newpos[1] - 2 * sample_step < 0
        ):
            newpos = (random.random() * WIDTH, random.random() * HEIGHT)
            randomnized = True

        # Draw line trail
        pygame.draw.circle(visualization_layer, (0, 255, 0), newpos, 2)
        if not randomnized: pygame.draw.line(visualization_layer, (0, 255, 0), part, newpos, 2)

        new_poses.append(newpos)

    return new_poses

while running:
    # Clear the layers
    gradient_layer.fill(BLACK)
    visualization_layer.fill((0, 0, 0, 0))  # Fully transparent background
    #visualization_layer.fill((0, 0, 0, 10), special_flags=pygame.BLEND_RGBA_SUB)
    # Get mouse position for dynamic light diffusion
    mouse_pos = pygame.mouse.get_pos()
    list_of_centers[0] = mouse_pos  # Update the first center to follow the mouse

    # Draw the gradient on the gradient layer
    for x in range(0, WIDTH, 5):  # Using a step of 5 for performance
        for y in range(0, HEIGHT, 5):
            combined_intensity = 0  # Start with no light

            # Calculate intensity from each light source
            for center in list_of_centers:
                distance = math.sqrt((x - center[0]) ** 2 + (y - center[1]) ** 2)
                combined_intensity += calculate_intensity(
                    distance, max_radius, initial_intensity, sigma
                )

            # Cap the combined intensity at 255
            combined_intensity = min(combined_intensity, 255)

            # Draw the pixel with the calculated intensity (grayscale)
            color = (combined_intensity, combined_intensity, combined_intensity)
            pygame.draw.rect(gradient_layer, color, pygame.Rect(x, y, 5, 5))

    # Visualize sampling and intensity differences
    for i, p in enumerate(pressure_sample_points):
        curr_val = color_to_value(
            gradient_layer.get_at(p)
        )  # Sample from the gradient layer

        # Get adjacent points and calculate intensity differences
        if (
            p[0] + sample_step >= WIDTH
            or p[0] - sample_step < 0
            or p[1] + sample_step >= HEIGHT
            or p[1] - sample_step < 0
        ):
            diffs_scaled = [0, 0, 0, 0]
            partial_diffs = [0, 0]
            mag = 0
        else:
            pressures = [
                color_to_value(
                    gradient_layer.get_at((p[0], p[1] + sample_step))
                ),  # Top
                color_to_value(
                    gradient_layer.get_at((p[0], p[1] - sample_step))
                ),  # Bottom
                color_to_value(
                    gradient_layer.get_at((p[0] + sample_step, p[1]))
                ),  # Right
                color_to_value(
                    gradient_layer.get_at((p[0] - sample_step, p[1]))
                ),  # Left
            ]
            diffs = [a - curr_val for a in pressures]
            diffs_scaled = [1000 * d / sample_step for d in diffs]
            # partial_diffs = [-1*abs(diffs_scaled[2]) + abs(diffs_scaled[3]), -1*abs(diffs_scaled[0]) + abs(diffs_scaled[1])]
            partial_diffs = [
                -diffs_scaled[2] + diffs_scaled[3],
                -diffs_scaled[0] + diffs_scaled[1],
            ]
            mag = math.sqrt(partial_diffs[0] ** 2 + partial_diffs[1] ** 2)

        # Draw visualization graphics on the visualization layer
        pygame.draw.circle(visualization_layer, WHITE, p, 1)
        # draw_arrow(visualization_layer, (255, 255, 255), (p[0], p[1]), (p[0] - partial_diffs[0], p[1] - partial_diffs[1]), 1, 5, 2)
        point_vectors[p[0]][p[1]] = partial_diffs
        if p[0] + sample_step < WIDTH and p[1] + sample_step < HEIGHT:
            calculate_divergence(p, point_vectors)
        pygame.draw.line(
            visualization_layer,
            (255, 255, 255),
            (p[0], p[1]),
            (p[0] - partial_diffs[0], p[1] - partial_diffs[1]),
        )
    # Combine layers by blitting them onto the main screen
    particle_pos = update_and_draw_particles(particle_pos, point_vectors)
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
