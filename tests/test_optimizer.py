import unittest
from typing import List, Dict, Tuple, Optional
from datetime import datetime, timedelta
from models.customer import Customer
from models.contractor import Contractor
from models.errand import Errand
from models.schedule import Schedule
from algorithms.optimizer import optimize_schedule, is_valid_schedule
from utils.city_map import GRID_SIZE
from constants import WORK_START_TIME, WORK_END_TIME, SCHEDULING_DAYS, ERRAND_TYPES, ErrandType

class TestOptimizer(unittest.TestCase):
    def setUp(self) -> None:
        # Create a sample problem for testing
        self.customers: List[Customer] = [
            Customer(i, ((i+1)*10, (i+1)*10), Errand(i, ERRAND_TYPES[i][0], timedelta(minutes=ERRAND_TYPES[i][1]), ERRAND_TYPES[i][2], ERRAND_TYPES[i][3]), 
                     {day: list(range(WORK_START_TIME, WORK_END_TIME, 30)) for day in range(SCHEDULING_DAYS)})
            for i in range(len(ERRAND_TYPES))
        ]
        self.contractors: List[Contractor] = [
            Contractor(0, (0, 0)),
            Contractor(1, (GRID_SIZE-1, GRID_SIZE-1))
        ]
        self.schedule: Schedule = Schedule(self.contractors, self.customers)
        
        # Create a simple initial schedule
        start_date = datetime.now().date()
        self.schedule.assignments: Dict[datetime, List[Tuple[Customer, Contractor, datetime]]] = {
            start_date + timedelta(days=0): [
                (self.customers[0], self.contractors[0], datetime.combine(start_date, datetime.min.time().replace(hour=WORK_START_TIME // 60, minute=WORK_START_TIME % 60))),
                (self.customers[1], self.contractors[0], datetime.combine(start_date, datetime.min.time().replace(hour=WORK_START_TIME // 60, minute=WORK_START_TIME % 60)) + timedelta(minutes=120)),
                (self.customers[2], self.contractors[1], datetime.combine(start_date, datetime.min.time().replace(hour=WORK_START_TIME // 60, minute=WORK_START_TIME % 60)))
            ],
            start_date + timedelta(days=1): [
                (self.customers[3], self.contractors[0], datetime.combine(start_date + timedelta(days=1), datetime.min.time().replace(hour=WORK_START_TIME // 60, minute=WORK_START_TIME % 60))),
                (self.customers[4], self.contractors[1], datetime.combine(start_date + timedelta(days=1), datetime.min.time().replace(hour=WORK_START_TIME // 60, minute=WORK_START_TIME % 60)))
            ],
            start_date + timedelta(days=2): [
                (self.customers[5], self.contractors[0], datetime.combine(start_date + timedelta(days=2), datetime.min.time().replace(hour=WORK_START_TIME // 60, minute=WORK_START_TIME % 60)))
            ]
        }

    def test_is_valid_schedule(self) -> None:
        self.assertTrue(is_valid_schedule(self.schedule))

        # Test invalid schedule (errand ends after working hours)
        invalid_schedule: Schedule = Schedule(self.contractors, self.customers)
        start_date = datetime.now().date()
        invalid_schedule.assignments = {
            start_date: [
                (self.customers[0], self.contractors[0], datetime.combine(start_date, datetime.min.time().replace(hour=WORK_END_TIME // 60 - 1, minute=(WORK_END_TIME % 60) + 40)))  # Starts 20 minutes before end of day
            ]
        }
        self.assertFalse(is_valid_schedule(invalid_schedule))

    def test_optimize_schedule(self) -> None:
        initial_profit: float = self.schedule.calculate_total_profit()
        optimized_schedule: Schedule = optimize_schedule(self.schedule)
        optimized_profit: float = optimized_schedule.calculate_total_profit()

        self.assertGreaterEqual(optimized_profit, initial_profit)
        self.assertTrue(is_valid_schedule(optimized_schedule))

    def test_optimize_schedule_respects_constraints(self) -> None:
        optimized_schedule: Schedule = optimize_schedule(self.schedule)

        # Check if all customers are scheduled
        scheduled_customers: set = set()
        for day_assignments in optimized_schedule.assignments.values():
            for customer, _, _ in day_assignments:
                scheduled_customers.add(customer.id)
        self.assertEqual(len(scheduled_customers), len(self.customers))

        # Check if working hours are respected
        for day_assignments in optimized_schedule.assignments.values():
            for _, _, start_time in day_assignments:
                self.assertGreaterEqual(start_time.time(), datetime.min.time().replace(hour=WORK_START_TIME // 60, minute=WORK_START_TIME % 60))
                self.assertLess(start_time.time(), datetime.min.time().replace(hour=WORK_END_TIME // 60, minute=WORK_END_TIME % 60))

    def test_optimize_schedule_handles_errand_types(self) -> None:
        optimized_schedule: Schedule = optimize_schedule(self.schedule)

        # Check if specific errand type constraints are respected
        for day, assignments in optimized_schedule.assignments.items():
            for customer, contractor, start_time in assignments:
                if customer.desired_errand.type == ErrandType.OUTING:
                    # Outing should take exactly the base time
                    next_start_time: Optional[datetime] = None
                    for next_customer, _, next_time in assignments[assignments.index((customer, contractor, start_time))+1:]:
                        if next_customer.desired_errand.type != ErrandType.OUTING:
                            next_start_time = next_time
                            break
                    if next_start_time:
                        self.assertEqual(next_start_time - start_time, customer.desired_errand.base_time)

    def test_optimize_schedule_improves_profit(self) -> None:
        # Create a deliberately inefficient schedule
        inefficient_schedule: Schedule = Schedule(self.contractors, self.customers)
        start_date = datetime.now().date()
        inefficient_schedule.assignments = {
            start_date + timedelta(days=day): [
                (customer, self.contractors[0], datetime.combine(start_date + timedelta(days=day), datetime.min.time().replace(hour=WORK_START_TIME // 60, minute=WORK_START_TIME % 60)) + timedelta(minutes=60 * i))
                for i, customer in enumerate(self.customers)
            ]
            for day in range(3)
        }

        initial_profit: float = inefficient_schedule.calculate_total_profit()
        optimized_schedule: Schedule = optimize_schedule(inefficient_schedule)
        optimized_profit: float = optimized_schedule.calculate_total_profit()

        self.assertGreater(optimized_profit, initial_profit)

if __name__ == '__main__':
    unittest.main()