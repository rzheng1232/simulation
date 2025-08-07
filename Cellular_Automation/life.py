import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 600, 600  # Screen dimensions
CELL_SIZE = 10  # Size of each cell
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

# Create a grid of WIDTH x HEIGHT
array_colors = [[0 for j in range(GRID_WIDTH)] for i in range(GRID_HEIGHT)]

BG_COLOR = (0, 0, 0)  # Background color (black for non-activated cells)
ACTIVATED_COLOR = (255, 255, 255)  # Activated cells (white)

init_pixel = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
array_colors[init_pixel[0]][init_pixel[1]] = 1  # Initialize with a starting pixel
array_colors[init_pixel[0] + 1][init_pixel[1]+1] = 1
# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Grid Activation Visualization')

def check_proximity(curr_pos):
    x, y = curr_pos
    total = 0
    if x + 1 < GRID_WIDTH and array_colors[x + 1][y] != 0:
        total += 1
    if x - 1 >= 0 and array_colors[x - 1][y] != 0:
        total += 1
    if y + 1 < GRID_HEIGHT and array_colors[x][y + 1] != 0:
        total += 1
    if y - 1 >= 0 and array_colors[x][y - 1] != 0:
        total += 1
    return total

def toggle_cell(probability, pos):
    x, y = pos
    if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
        if random.random() < probability:
            array_colors[x][y] = 1  # Activate
        else:
            array_colors[x][y] = 0  # Deactivate

def iterate_function():
    for i in range(GRID_WIDTH):
        for j in range(GRID_HEIGHT):
            if array_colors[i][j] != 0:  # If the cell is activated
                total_proximity = check_proximity((i, j))
                
                # Apply activation/deactivation rules
                if total_proximity == 0:
                    toggle_cell(0.5, (i+1, j))
                    toggle_cell(0.5, (i-1, j))
                    toggle_cell(0.5, (i, j+1))
                    toggle_cell(0.5, (i, j-1))
                if total_proximity == 1:
                    toggle_cell(0.4, (i+1, j))
                    toggle_cell(0.4, (i-1, j))
                    toggle_cell(0.4, (i, j+1))
                    toggle_cell(0.4, (i, j-1))
                if total_proximity == 2:
                    toggle_cell(0.3, (i+1, j))
                    toggle_cell(0.3, (i-1, j))
                    toggle_cell(0.3, (i, j+1))
                    toggle_cell(0.3, (i, j-1))
                if total_proximity == 3:
                    toggle_cell(0.2, (i+1, j))
                    toggle_cell(0.2, (i-1, j))
                    toggle_cell(0.2, (i, j+1))
                    toggle_cell(0.2, (i, j-1))
                if total_proximity == 4:
                    toggle_cell(0, (i+1, j))
                    toggle_cell(0, (i-1, j))
                    toggle_cell(0, (i, j+1))
                    toggle_cell(0, (i, j-1))

def draw_grid():
    for i in range(GRID_WIDTH):
        for j in range(GRID_HEIGHT):
            color = ACTIVATED_COLOR if array_colors[i][j] == 1 else BG_COLOR
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
    pygame.time.delay(100)  # Control the speed of the update