import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from models.customer import Customer
from models.contractor import Contractor
from models.errand import Errand
from models.schedule import Schedule
from algorithms.initial_scheduler import initial_schedule
from utils.city_map import GRID_SIZE

class TestInitialScheduler(unittest.TestCase):
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

    def test_initial_schedule_creation(self):
        schedule = initial_schedule(self.customers, self.contractors)
        
        # Check if the schedule is an instance of Schedule
        self.assertIsInstance(schedule, Schedule)
        
        # Check if all customers are assigned
        assigned_customers = set()
        for day, assignments in schedule.assignments.items():
            for customer, _, _ in assignments:
                assigned_customers.add(customer.id)
        
        self.assertEqual(len(assigned_customers), len(self.customers))
        
    def test_schedule_validity(self):
        schedule = initial_schedule(self.customers, self.contractors)
        
        for day, assignments in schedule.assignments.items():
            for customer, _, start_time in assignments:
                # Check if the start time is within working hours
                self.assertGreaterEqual(start_time, 480)  # 8:00 AM
                self.assertLess(start_time + customer.desired_errand.base_time, 1020)  # 5:00 PM

    def test_contractor_assignment(self):
        schedule = initial_schedule(self.customers, self.contractors)
        
        for day, assignments in schedule.assignments.items():
            contractor_assignments = {contractor.id: 0 for contractor in self.contractors}
            for _, contractor, _ in assignments:
                contractor_assignments[contractor.id] += 1
            
            # Check if at least one contractor is used
            self.assertGreater(sum(contractor_assignments.values()), 0)

    def test_customer_order_preservation(self):
        # Create a list of customers with different errand types and locations
        test_customers = [
            Customer(0, (10, 10), Errand(0, "Grocery Shopping", 60, 1.5, None), {0: list(range(480, 1020, 30))}),
            Customer(1, (20, 20), Errand(1, "Dry Cleaning", 30, 1.5, None), {0: list(range(480, 1020, 30))}),
            Customer(2, (30, 30), Errand(2, "Package Delivery", 45, 1.5, None), {0: list(range(480, 1020, 30))}),
            Customer(3, (40, 40), Errand(3, "Dog Walking", 40, 1.5, None), {0: list(range(480, 1020, 30))}),
            Customer(4, (50, 50), Errand(4, "House Cleaning", 120, 1.5, None), {0: list(range(480, 1020, 30))})
        ]
        
        schedule = initial_schedule(test_customers, self.contractors)
        
        # Extract the order of scheduled customers
        scheduled_customer_order = []
        for day in range(14):
            if day in schedule.assignments:
                scheduled_customer_order.extend([customer.id for customer, _, _ in schedule.assignments[day]])
        
        # Check if the scheduled order matches the input order
        expected_order = [customer.id for customer in test_customers]
        self.assertEqual(scheduled_customer_order, expected_order,
                         "Customers should be scheduled in the same order they were provided")

if __name__ == '__main__':
    unittest.main()