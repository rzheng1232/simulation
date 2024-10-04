import copy
import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 600, 600  # Screen dimensions
CELL_SIZE = 1  # Size of each cell
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

# Create a grid of WIDTH x HEIGHT
array_colors = [[[0,0,0] for j in range(GRID_WIDTH)] for i in range(GRID_HEIGHT)]
BG_COLOR = (0, 0, 0)  # Background color (black for non-activated cells)
ACTIVATED_COLOR = (255, 255, 255)  # Activated cells (white)

init_pixel = (0, 0) #(GRID_WIDTH // 2, GRID_HEIGHT // 2)
array_colors[init_pixel[0]][init_pixel[1]] = [255, 255, 255]  # Initialize with a starting pixel
array_colors[init_pixel[0] +500][init_pixel[1]] = [255, 255, 255]

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Grid Activation Visualization')

def check_proximity(curr_pos):
    x, y = curr_pos
    total = 0
    if x + 1 < GRID_WIDTH and array_colors[x + 1][y] != [0, 0, 0]:
        total += 1
    if x - 1 >= 0 and array_colors[x - 1][y] != [0, 0, 0]:
        total += 1
    if y + 1 < GRID_HEIGHT and array_colors[x][y + 1] != [0, 0, 0]:
        total += 1
    if y - 1 >= 0 and array_colors[x][y - 1] != [0, 0, 0]:
        total += 1
    return total

def toggle_cellblue(probability, pos):
    x, y = pos
    if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
        if random.random() < probability:
            # Activate, ensuring RGB values stay within valid range
            array_colors[x][y][2] = min(array_colors[x][y][2] + 50, 255)
        else:
            # Deactivate or dim down the RGB values
            array_colors[x][y][2] = max(array_colors[x][y][2] - 5, 0)
def toggle_cellred(probability, pos):
    x, y = pos
    if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
        if random.random() < probability:
            # Activate, ensuring RGB values stay within valid range
            array_colors[x][y][0] = min(array_colors[x][y][0] + 50, 255)
        else:
            # Deactivate or dim down the RGB values
            array_colors[x][y][0] = max(array_colors[x][y][0] - 5, 0)
def toggle_cellblack(probability, pos):
    x, y = pos
    if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
        if random.random() > probability:
            # Activate, ensuring RGB values stay within valid range
            array_colors[x][y][0] = min(array_colors[x][y][0] + 1, 125)
            array_colors[x][y][1] = min(array_colors[x][y][1] + 1, 125)
            array_colors[x][y][2] = min(array_colors[x][y][2] + 1, 125)
        else:
            # Deactivate or dim down the RGB values
            array_colors[x][y][0] = max(array_colors[x][y][0] - 5, 0)
            array_colors[x][y][1] = max(array_colors[x][y][1] - 10, 0)
            array_colors[x][y][2] = max(array_colors[x][y][2] - 5, 0)
def iterate_function():
    
    for i in range(GRID_WIDTH):
        for j in range(GRID_HEIGHT):
            if array_colors[i][j] != [0, 0, 0]:  # If the cell is activated
                total_proximity = check_proximity((i, j))
                
                # Apply activation/deactivation rules
                if total_proximity == 0:
                    toggle_cellred(0.5, (i+1, j))
                    toggle_cellred(0.5, (i-1, j))
                    toggle_cellblack(0.5, (i, j+1))
                    toggle_cellblack(0.5, (i, j-1))
                if total_proximity == 1:
                    toggle_cellred(0.4, (i+1, j))
                    toggle_cellred(0.4, (i-1, j))
                    toggle_cellblack(0.4, (i, j+1))
                    toggle_cellblack(0.4, (i, j-1))
                if total_proximity == 2:
                    toggle_cellred(0.3, (i+1, j))
                    toggle_cellred(0.3, (i-1, j))
                    toggle_cellblack(0.3, (i, j+1))
                    toggle_cellblack(0.3, (i, j-1))
                if total_proximity == 3:
                    toggle_cellred(0.2, (i+1, j))
                    toggle_cellred(0.2, (i-1, j))
                    toggle_cellblack(0.2, (i, j+1))
                    toggle_cellblack(0.2, (i, j-1))
                if total_proximity == 4:
                    toggle_cellred(0, (i+1, j))
                    toggle_cellred(0, (i-1, j))
                    toggle_cellblack(0, (i, j+1))
                    toggle_cellblack(0, (i, j-1))

def draw_grid():
    for i in range(GRID_WIDTH):
        for j in range(GRID_HEIGHT):
            color = array_colors[i][j]  # Get the RGB color value
            pygame.draw.rect(screen, color, pygame.Rect(i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Main loop
running = True
while running:
    screen.fill(BG_COLOR)  # Clear the screen
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
    
    iterate_function()  # Update the grid
    draw_grid()  # Draw the updated grid
    
    pygame.display.flip()  # Update the display
    pygame.time.delay(1)  # Control the speed of the update