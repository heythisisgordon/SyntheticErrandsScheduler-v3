import numpy as np
from typing import Tuple

GRID_SIZE: int = 100

def create_city_grid() -> np.ndarray:
    grid: np.ndarray = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
    grid[::10, :] = 1  # Horizontal roads
    grid[:, ::10] = 1  # Vertical roads
    return grid

def is_valid_road_location(x: int, y: int) -> bool:
    return x % 10 == 0 or y % 10 == 0

# Create the city grid
city_grid: np.ndarray = create_city_grid()