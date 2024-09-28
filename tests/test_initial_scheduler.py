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
from constants import WORK_START_TIME, WORK_END_TIME, SCHEDULING_DAYS, ERRAND_TYPES

class TestInitialScheduler(unittest.TestCase):
    def setUp(self):
        # Create a sample problem for testing
        self.customers = [
            Customer(0, (10, 10), Errand(0, ERRAND_TYPES[0][0], ERRAND_TYPES[0][1], ERRAND_TYPES[0][2], ERRAND_TYPES[0][3]), {0: list(range(WORK_START_TIME, WORK_END_TIME, 30))}),
            Customer(1, (20, 20), Errand(1, ERRAND_TYPES[1][0], ERRAND_TYPES[1][1], ERRAND_TYPES[1][2], ERRAND_TYPES[1][3]), {0: list(range(WORK_START_TIME, WORK_END_TIME, 30))}),
            Customer(2, (30, 30), Errand(2, ERRAND_TYPES[2][0], ERRAND_TYPES[2][1], ERRAND_TYPES[2][2], ERRAND_TYPES[2][3]), {0: list(range(WORK_START_TIME, WORK_END_TIME, 30))})
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
                self.assertGreaterEqual(start_time, WORK_START_TIME)
                self.assertLess(start_time + customer.desired_errand.base_time, WORK_END_TIME)

    def test_contractor_assignment(self):
        schedule = initial_schedule(self.customers, self.contractors)
        
        for day, assignments in schedule.assignments.items():
            contractor_assignments = {contractor.id: [] for contractor in self.contractors}
            for customer, contractor, start_time in assignments:
                contractor_assignments[contractor.id].append((customer, start_time))
            
            # Check if contractors are assigned in order
            for contractor_id, assigned_errands in contractor_assignments.items():
                self.assertEqual(sorted(assigned_errands, key=lambda x: x[1]), assigned_errands,
                                 f"Errands for contractor {contractor_id} are not in chronological order")

    def test_earliest_possible_scheduling(self):
        schedule = initial_schedule(self.customers, self.contractors)
        
        for day, assignments in schedule.assignments.items():
            contractor_end_times = {contractor.id: WORK_START_TIME for contractor in self.contractors}
            
            for customer, contractor, start_time in assignments:
                self.assertEqual(start_time, contractor_end_times[contractor.id],
                                 f"Errand for customer {customer.id} not scheduled at earliest possible time")
                contractor_end_times[contractor.id] = start_time + customer.desired_errand.base_time

    def test_customer_order_preservation(self):
        # Create a list of customers with different errand types and locations
        test_customers = [
            Customer(i, (10*(i+1), 10*(i+1)), Errand(i, ERRAND_TYPES[i % len(ERRAND_TYPES)][0], ERRAND_TYPES[i % len(ERRAND_TYPES)][1], ERRAND_TYPES[i % len(ERRAND_TYPES)][2], ERRAND_TYPES[i % len(ERRAND_TYPES)][3]), {0: list(range(WORK_START_TIME, WORK_END_TIME, 30))})
            for i in range(5)
        ]
        
        schedule = initial_schedule(test_customers, self.contractors)
        
        # Extract the order of scheduled customers
        scheduled_customer_order = []
        for day in range(SCHEDULING_DAYS):
            if day in schedule.assignments:
                scheduled_customer_order.extend([customer.id for customer, _, _ in schedule.assignments[day]])
        
        # Check if the scheduled order matches the input order
        expected_order = [customer.id for customer in test_customers]
        self.assertEqual(scheduled_customer_order, expected_order,
                         "Customers should be scheduled in the same order they were provided")

if __name__ == '__main__':
    unittest.main()