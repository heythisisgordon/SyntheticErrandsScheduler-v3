import numpy as np

GRID_SIZE = 100

def create_city_grid():
    grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
    grid[::10, :] = 1  # Horizontal roads
    grid[:, ::10] = 1  # Vertical roads
    return grid

def is_valid_road_location(x, y):
    return x % 10 == 0 or y % 10 == 0

# Create the city grid
city_grid = create_city_grid()