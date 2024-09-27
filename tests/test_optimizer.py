import unittest
from models.customer import Customer
from models.contractor import Contractor
from models.errand import Errand
from models.schedule import Schedule
from algorithms.optimizer import optimize_schedule, is_valid_schedule
from utils.city_map import GRID_SIZE

class TestOptimizer(unittest.TestCase):
    def setUp(self):
        # Create a sample problem for testing
        self.customers = [
            Customer(0, (10, 10), Errand(0, "Grocery Shopping", 60, 1.5, None), {0: list(range(480, 1020, 30))}),
            Customer(1, (20, 20), Errand(1, "Dry Cleaning", 30, 1.5, None), {0: list(range(480, 1020, 30))}),
            Customer(2, (30, 30), Errand(2, "Package Delivery", 45, 1.5, None), {0: list(range(480, 1020, 30))})
        ]
        self.contractors = [
            Contractor(0, (0, 0)),
            Contractor(1, (GRID_SIZE-1, GRID_SIZE-1))
        ]
        self.schedule = Schedule(self.contractors, self.customers)
        
        # Create a simple initial schedule
        self.schedule.assignments = {
            0: [
                (self.customers[0], self.contractors[0], 480),
                (self.customers[1], self.contractors[0], 600),
                (self.customers[2], self.contractors[1], 480)
            ]
        }

    def test_is_valid_schedule(self):
        self.assertTrue(is_valid_schedule(self.schedule))

        # Test invalid schedule (errand ends after working hours)
        invalid_schedule = Schedule(self.contractors, self.customers)
        invalid_schedule.assignments = {
            0: [
                (self.customers[0], self.contractors[0], 1000)  # Starts at 4:40 PM, ends after 5 PM
            ]
        }
        self.assertFalse(is_valid_schedule(invalid_schedule))

    def test_optimize_schedule(self):
        initial_profit = self.schedule.calculate_total_profit()
        optimized_schedule = optimize_schedule(self.schedule)
        optimized_profit = optimized_schedule.calculate_total_profit()

        self.assertGreaterEqual(optimized_profit, initial_profit)
        self.assertTrue(is_valid_schedule(optimized_schedule))

if __name__ == '__main__':
    unittest.main()