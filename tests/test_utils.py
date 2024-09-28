import unittest
import numpy as np
from utils.city_map import create_city_grid, is_valid_road_location, GRID_SIZE
from utils.travel_time import calculate_travel_time, get_nearest_road_point
from utils.errand_utils import calculate_errand_time
from models.errand import Errand
from constants import DELIVERY_ADDITIONAL_TIME, ERRAND_TYPES

class TestUtils(unittest.TestCase):
    def test_create_city_grid(self):
        grid = create_city_grid()
        self.assertIsInstance(grid, np.ndarray)
        self.assertEqual(grid.shape, (GRID_SIZE, GRID_SIZE))
        
        # Check if roads are correctly placed
        for i in range(0, GRID_SIZE, 10):
            self.assertTrue(np.all(grid[i, :] == 1))  # Horizontal roads
            self.assertTrue(np.all(grid[:, i] == 1))  # Vertical roads

    def test_is_valid_road_location(self):
        # Test road locations
        self.assertTrue(is_valid_road_location(0, 0))
        self.assertTrue(is_valid_road_location(10, 20))
        self.assertTrue(is_valid_road_location(50, 50))
        
        # Test non-road locations
        self.assertFalse(is_valid_road_location(1, 1))
        self.assertFalse(is_valid_road_location(15, 25))
        self.assertFalse(is_valid_road_location(99, 99))

    def test_get_nearest_road_point(self):
        self.assertEqual(get_nearest_road_point((0, 0)), (0, 0))
        self.assertEqual(get_nearest_road_point((5, 5)), (0, 0))
        self.assertEqual(get_nearest_road_point((12, 18)), (10, 20))
        self.assertEqual(get_nearest_road_point((95, 95)), (90, 90))

    def test_calculate_travel_time(self):
        # Test same location
        travel_time, route = calculate_travel_time((0, 0), (0, 0))
        self.assertEqual(travel_time, 0)
        self.assertEqual(route, [(0, 0)])
        
        # Test horizontal travel
        travel_time, route = calculate_travel_time((0, 0), (10, 0))
        self.assertEqual(travel_time, 10)
        self.assertEqual(route, [(0, 0), (10, 0)])
        
        # Test vertical travel
        travel_time, route = calculate_travel_time((0, 0), (0, 20))
        self.assertEqual(travel_time, 20)
        self.assertEqual(route, [(0, 0), (0, 20)])
        
        # Test diagonal travel (Manhattan distance)
        travel_time, route = calculate_travel_time((0, 0), (30, 40))
        self.assertEqual(travel_time, 70)
        self.assertEqual(route, [(0, 0), (30, 0), (30, 40)])
        
        # Test travel from non-road point
        travel_time, route = calculate_travel_time((5, 5), (30, 40))
        self.assertEqual(travel_time, 70)
        self.assertEqual(route, [(5, 5), (0, 0), (30, 0), (30, 40)])
        
        # Test travel to non-road point
        travel_time, route = calculate_travel_time((0, 0), (35, 45))
        self.assertEqual(travel_time, 80)
        self.assertEqual(route, [(0, 0), (30, 40), (35, 45)])

    def test_calculate_errand_time(self):
        start_location = (0, 0)
        end_location = (10, 10)
        
        for errand_type, base_time, _, _ in ERRAND_TYPES:
            errand = Errand(0, errand_type, base_time, 1.0, None)
            errand_time = calculate_errand_time(errand, start_location, end_location)
            
            expected_time = base_time + 20  # 20 is the Manhattan distance between (0,0) and (10,10)
            if errand_type == "Delivery":
                expected_time += DELIVERY_ADDITIONAL_TIME
            elif errand_type == "Outing":
                expected_time = base_time  # Outing doesn't include travel time
            
            self.assertEqual(errand_time, expected_time, f"Failed for errand type: {errand_type}")

if __name__ == '__main__':
    unittest.main()