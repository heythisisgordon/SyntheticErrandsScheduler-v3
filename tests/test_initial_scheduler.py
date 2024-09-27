import unittest
from models.customer import Customer
from models.contractor import Contractor
from models.errand import Errand
from models.schedule import Schedule
from algorithms.initial_scheduler import initial_schedule
from utils.city_map import GRID_SIZE
from utils.travel_time import calculate_travel_time
from utils.errand_utils import calculate_errand_time

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
            for i, (customer, contractor, start_time) in enumerate(assignments):
                # Check if the start time is within working hours
                self.assertGreaterEqual(start_time, 480)  # 8:00 AM
                self.assertLess(start_time + customer.desired_errand.base_time, 1020)  # 5:00 PM
                
                if i > 0:
                    # Check if there's enough time between assignments
                    prev_customer, prev_contractor, prev_start_time = assignments[i-1]
                    prev_end_time = prev_start_time + calculate_errand_time(prev_customer.desired_errand, prev_contractor.location, prev_customer.location)
                    travel_time, _ = calculate_travel_time(prev_customer.location, customer.location)
                    self.assertGreaterEqual(start_time, prev_end_time + travel_time)

    def test_contractor_assignment(self):
        schedule = initial_schedule(self.customers, self.contractors)
        
        for day, assignments in schedule.assignments.items():
            contractor_assignments = {contractor.id: 0 for contractor in self.contractors}
            for _, contractor, _ in assignments:
                contractor_assignments[contractor.id] += 1
            
            # Check if all contractors are used (if possible)
            if len(assignments) >= len(self.contractors):
                for count in contractor_assignments.values():
                    self.assertGreater(count, 0)

    def test_dynamic_scheduling(self):
        schedule = initial_schedule(self.customers, self.contractors)
        
        for day, assignments in schedule.assignments.items():
            for i, (customer, contractor, start_time) in enumerate(assignments):
                if i > 0:
                    prev_customer, prev_contractor, prev_start_time = assignments[i-1]
                    prev_errand_time = calculate_errand_time(prev_customer.desired_errand, prev_contractor.location, prev_customer.location)
                    prev_end_time = prev_start_time + prev_errand_time
                    travel_time, _ = calculate_travel_time(prev_customer.location, customer.location)
                    expected_start_time = prev_end_time + travel_time
                    self.assertGreaterEqual(start_time, expected_start_time, 
                                     f"Start time should be at least {expected_start_time}, but got {start_time}")

    def test_no_fixed_interval(self):
        schedule = initial_schedule(self.customers, self.contractors)
        
        for day, assignments in schedule.assignments.items():
            start_times = [start_time for _, _, start_time in assignments]
            time_differences = [start_times[i+1] - start_times[i] for i in range(len(start_times)-1)]
            
            # Check that not all time differences are the same (i.e., not fixed interval)
            self.assertFalse(all(diff == time_differences[0] for diff in time_differences),
                             "Schedules should not have a fixed interval between all assignments")

if __name__ == '__main__':
    unittest.main()