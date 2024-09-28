import unittest
from datetime import datetime, timedelta
from models.customer import Customer
from models.contractor import Contractor
from models.errand import Errand
from models.schedule import Schedule
from algorithms.optimizer import optimize_schedule, is_valid_schedule
from utils.city_map import GRID_SIZE
from constants import WORK_START_TIME, WORK_END_TIME, SCHEDULING_DAYS, ERRAND_TYPES

class TestOptimizer(unittest.TestCase):
    def setUp(self):
        # Create a sample problem for testing
        self.customers = [
            Customer(i, ((i+1)*10, (i+1)*10), Errand(i, *ERRAND_TYPES[i]), 
                     {day: list(range(WORK_START_TIME, WORK_END_TIME, 30)) for day in range(SCHEDULING_DAYS)})
            for i in range(len(ERRAND_TYPES))
        ]
        self.contractors = [
            Contractor(0, (0, 0)),
            Contractor(1, (GRID_SIZE-1, GRID_SIZE-1))
        ]
        self.schedule = Schedule(self.contractors, self.customers)
        
        # Create a simple initial schedule
        self.schedule.assignments = {
            0: [
                (self.customers[0], self.contractors[0], WORK_START_TIME),
                (self.customers[1], self.contractors[0], WORK_START_TIME + 120),
                (self.customers[2], self.contractors[1], WORK_START_TIME)
            ],
            1: [
                (self.customers[3], self.contractors[0], WORK_START_TIME),
                (self.customers[4], self.contractors[1], WORK_START_TIME)
            ],
            2: [
                (self.customers[5], self.contractors[0], WORK_START_TIME)
            ]
        }

    def test_is_valid_schedule(self):
        self.assertTrue(is_valid_schedule(self.schedule))

        # Test invalid schedule (errand ends after working hours)
        invalid_schedule = Schedule(self.contractors, self.customers)
        invalid_schedule.assignments = {
            0: [
                (self.customers[0], self.contractors[0], WORK_END_TIME - 20)  # Starts 20 minutes before end of day
            ]
        }
        self.assertFalse(is_valid_schedule(invalid_schedule))

    def test_optimize_schedule(self):
        initial_profit = self.schedule.calculate_total_profit()
        optimized_schedule = optimize_schedule(self.schedule)
        optimized_profit = optimized_schedule.calculate_total_profit()

        self.assertGreaterEqual(optimized_profit, initial_profit)
        self.assertTrue(is_valid_schedule(optimized_schedule))

    def test_optimize_schedule_respects_constraints(self):
        optimized_schedule = optimize_schedule(self.schedule)

        # Check if all customers are scheduled
        scheduled_customers = set()
        for day_assignments in optimized_schedule.assignments.values():
            for customer, _, _ in day_assignments:
                scheduled_customers.add(customer.id)
        self.assertEqual(len(scheduled_customers), len(self.customers))

        # Check if working hours are respected
        for day_assignments in optimized_schedule.assignments.values():
            for _, _, start_time in day_assignments:
                self.assertGreaterEqual(start_time, WORK_START_TIME)
                self.assertLess(start_time, WORK_END_TIME)

    def test_optimize_schedule_handles_errand_types(self):
        optimized_schedule = optimize_schedule(self.schedule)

        # Check if specific errand type constraints are respected
        for day, assignments in optimized_schedule.assignments.items():
            for customer, contractor, start_time in assignments:
                if customer.desired_errand.type == "Outing":
                    # Outing should take exactly the base time
                    next_start_time = None
                    for next_customer, _, next_time in assignments[assignments.index((customer, contractor, start_time))+1:]:
                        if next_customer.desired_errand.type != "Outing":
                            next_start_time = next_time
                            break
                    if next_start_time:
                        self.assertEqual(next_start_time - start_time, customer.desired_errand.base_time)

    def test_optimize_schedule_improves_profit(self):
        # Create a deliberately inefficient schedule
        inefficient_schedule = Schedule(self.contractors, self.customers)
        inefficient_schedule.assignments = {
            day: [(customer, self.contractors[0], WORK_START_TIME + 60 * i) for i, customer in enumerate(self.customers)]
            for day in range(3)
        }

        initial_profit = inefficient_schedule.calculate_total_profit()
        optimized_schedule = optimize_schedule(inefficient_schedule)
        optimized_profit = optimized_schedule.calculate_total_profit()

        self.assertGreater(optimized_profit, initial_profit)

if __name__ == '__main__':
    unittest.main()