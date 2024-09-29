import unittest
import os
from typing import Dict, List
from models.customer import Customer
from models.contractor import Contractor
from models.errand import Errand
from models.schedule import Schedule
from utils.visualization import visualize_schedule, print_schedule
from io import StringIO
import sys
from constants import ErrandType

class TestVisualization(unittest.TestCase):
    def setUp(self) -> None:
        self.errand: Errand = Errand(0, ErrandType.GROCERY_SHOPPING, 60, 1.5, None)
        self.customer: Customer = Customer(0, (10, 10), self.errand, {0: list(range(480, 1020, 30))})
        self.contractor: Contractor = Contractor(0, (0, 0))
        self.schedule: Schedule = Schedule([self.contractor], [self.customer])
        self.schedule.assignments: Dict[int, List[tuple[Customer, Contractor, int]]] = {0: [(self.customer, self.contractor, 480)]}

    def test_visualize_schedule(self) -> None:
        filename: str = "test_schedule_visualization.png"
        
        # Call visualize_schedule with the filename parameter
        visualize_schedule(self.schedule, filename)
        
        # Check if the file was created
        self.assertTrue(os.path.exists(filename))
        
        # Check if the file is not empty
        self.assertGreater(os.path.getsize(filename), 0)
        
        # Clean up
        os.remove(filename)

    def test_print_schedule(self) -> None:
        # Redirect stdout to capture print output
        captured_output: StringIO = StringIO()
        sys.stdout = captured_output

        print_schedule(self.schedule)

        # Restore stdout
        sys.stdout = sys.__stdout__

        output: str = captured_output.getvalue()

        # Check if the output contains expected information
        self.assertIn("Synthetic Errands Schedule:", output)
        self.assertIn("Day 1:", output)
        self.assertIn("Contractor 1 - Customer 1:", output)
        self.assertIn("Errand: GROCERY_SHOPPING", output)
        self.assertIn("Start Time: 08:00", output)
        self.assertIn("Location: (10, 10)", output)
        self.assertIn("Total Profit: $", output)

if __name__ == '__main__':
    unittest.main()