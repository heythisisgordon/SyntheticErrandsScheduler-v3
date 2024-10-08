import sys
import os
from typing import List, Dict, Set, Tuple
from io import StringIO
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from datetime import datetime, timedelta, time
from models.customer import Customer
from models.contractor import Contractor
from models.errand import Errand
from models.schedule import Schedule
from models.master_contractor_calendar import MasterContractorCalendar
from algorithms.initial_greedy_scheduler import initial_greedy_schedule, InitialSchedulingError
from utils.city_map import GRID_SIZE
from utils.scheduling_utils import (
    calculate_total_time,
    is_valid_assignment,
    calculate_assignment_profit
)
from constants import WORK_START_TIME_OBJ, WORK_END_TIME_OBJ, SCHEDULING_DAYS, ERRAND_TYPES
import logging
from contextlib import contextmanager

DEFAULT_CONTRACTOR_RATE = 0.5

class TestInitialGreedyScheduler(unittest.TestCase):
    def setUp(self) -> None:
        self.customers: List[Customer] = self._generate_customers(3)
        self.contractors: List[Contractor] = [
            Contractor(0, (0, 0), DEFAULT_CONTRACTOR_RATE),
            Contractor(1, (GRID_SIZE-1, GRID_SIZE-1), DEFAULT_CONTRACTOR_RATE + 0.1)
        ]
        self.master_calendar = MasterContractorCalendar()
        for contractor in self.contractors:
            self.master_calendar.add_contractor(contractor)
        # Set up logging
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        self.log_capture = StringIO()
        self.handler = logging.StreamHandler(self.log_capture)
        self.handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.handler.setFormatter(formatter)
        self.logger.addHandler(self.handler)

    def tearDown(self) -> None:
        self.logger.removeHandler(self.handler)
        print(self.log_capture.getvalue())

    def _generate_customers(self, num_customers: int) -> List[Customer]:
        start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        return [
            Customer(
                i,
                (10 * (i + 1), 10 * (i + 1)),
                Errand(i, ERRAND_TYPES[i % len(ERRAND_TYPES)][0], timedelta(minutes=ERRAND_TYPES[i % len(ERRAND_TYPES)][1]), ERRAND_TYPES[i % len(ERRAND_TYPES)][2], ERRAND_TYPES[i % len(ERRAND_TYPES)][3]),
                {start_date + timedelta(days=day): [(datetime.combine(start_date + timedelta(days=day), WORK_START_TIME_OBJ), 
                                                    datetime.combine(start_date + timedelta(days=day), WORK_END_TIME_OBJ))] for day in range(SCHEDULING_DAYS)}
            )
            for i in range(num_customers)
        ]

    @contextmanager
    def capture_logging(self, logger_name: str):
        logger = logging.getLogger(logger_name)
        previous_level = logger.level
        logger.setLevel(logging.INFO)
        log_capture = StringIO()
        handler = logging.StreamHandler(log_capture)
        logger.addHandler(handler)
        try:
            yield log_capture
        finally:
            logger.removeHandler(handler)
            logger.setLevel(previous_level)

    def test_initial_greedy_schedule_creation(self) -> None:
        schedule: Schedule = initial_greedy_schedule(self.customers, self.contractors)
        
        self.assertIsInstance(schedule, Schedule)
        
        assigned_customers: Set[int] = {customer.id for assignments in schedule.assignments.values() for customer, _, _ in assignments}
        self.assertEqual(len(assigned_customers), len(self.customers))
        
    def test_schedule_validity(self) -> None:
        schedule: Schedule = initial_greedy_schedule(self.customers, self.contractors)
        
        for day, assignments in schedule.assignments.items():
            for customer, contractor, start_time in assignments:
                self.assertGreaterEqual(start_time.time(), WORK_START_TIME_OBJ)
                end_time = start_time + customer.desired_errand.base_time
                self.assertLess(end_time.time(), WORK_END_TIME_OBJ)
                
                self.assertFalse(self.master_calendar.is_contractor_available(contractor.id, start_time, end_time),
                                 f"Time slot for customer {customer.id} should not be available in contractor {contractor.id}'s calendar")

    def test_contractor_assignment(self) -> None:
        schedule: Schedule = initial_greedy_schedule(self.customers, self.contractors)
        
        for day, assignments in schedule.assignments.items():
            contractor_assignments: Dict[int, List[Tuple[Customer, datetime]]] = {contractor.id: [] for contractor in self.contractors}
            for customer, contractor, start_time in assignments:
                contractor_assignments[contractor.id].append((customer, start_time))
            
            for contractor_id, assigned_errands in contractor_assignments.items():
                prev_end_time = datetime.combine(day.date(), WORK_START_TIME_OBJ)
                prev_location = self.contractors[contractor_id].location
                for customer, start_time in assigned_errands:
                    total_time = calculate_total_time(self.contractors[contractor_id], customer, customer.desired_errand)
                    next_slot = self.master_calendar.get_contractor_next_available_slot(contractor_id, prev_end_time, total_time)
                    self.assertIsNotNone(next_slot)
                    self.assertGreaterEqual(start_time, next_slot['start'],
                                            f"Errand for customer {customer.id} scheduled too early, not accounting for travel time")
                    self.assertLess(start_time - next_slot['start'], timedelta(minutes=1),
                                    f"Excessive gap between errands for customer {customer.id}")
                    prev_end_time = start_time + customer.desired_errand.base_time
                    prev_location = customer.location

    def test_is_valid_assignment(self) -> None:
        for contractor in self.contractors:
            for customer in self.customers:
                start_time = datetime.combine(datetime.now().date(), WORK_START_TIME_OBJ)
                end_time = start_time + customer.desired_errand.base_time
                self.assertTrue(is_valid_assignment(contractor, customer, start_time, end_time),
                                f"Assignment should be valid for contractor {contractor.id} and customer {customer.id}")

                invalid_start = datetime.combine(datetime.now().date(), WORK_END_TIME_OBJ) + timedelta(hours=1)
                invalid_end = invalid_start + customer.desired_errand.base_time
                self.assertFalse(is_valid_assignment(contractor, customer, invalid_start, invalid_end),
                                 f"Assignment outside working hours should be invalid")

    def test_empty_customer_list(self) -> None:
        with self.assertRaises(InitialSchedulingError):
            initial_greedy_schedule([], self.contractors)

    def test_empty_contractor_list(self) -> None:
        with self.assertRaises(InitialSchedulingError):
            initial_greedy_schedule(self.customers, [])

    def test_no_feasible_schedule(self) -> None:
        working_hours = timedelta(hours=WORK_END_TIME_OBJ.hour - WORK_START_TIME_OBJ.hour,
                                  minutes=WORK_END_TIME_OBJ.minute - WORK_START_TIME_OBJ.minute)
        impossible_customers: List[Customer] = self._generate_customers(1)
        impossible_customers[0].desired_errand.base_time = working_hours + timedelta(minutes=1)
        
        with self.assertRaises(InitialSchedulingError):
            initial_greedy_schedule(impossible_customers, self.contractors)

    def test_respect_scheduling_days_limit(self) -> None:
        long_errand_customers: List[Customer] = self._generate_customers(10)
        for customer in long_errand_customers:
            customer.desired_errand.base_time = timedelta(hours=6)
        
        schedule: Schedule = initial_greedy_schedule(long_errand_customers, self.contractors)
        
        self.assertLessEqual(len(schedule.assignments), SCHEDULING_DAYS,
                             f"Schedule exceeds the maximum allowed days ({SCHEDULING_DAYS})")

    def test_logging_functionality(self) -> None:
        with self.capture_logging('algorithms.initial_greedy_scheduler') as log_capture:
            initial_greedy_schedule(self.customers, self.contractors)

        log_contents = log_capture.getvalue()
        self.assertIn("Starting initial greedy scheduling process", log_contents)
        self.assertIn("Initial greedy scheduling process completed", log_contents)
        self.assertIn("Total profit for initial greedy schedule", log_contents)

    def test_error_handling(self) -> None:
        with self.assertRaises(InitialSchedulingError):
            initial_greedy_schedule(None, self.contractors)
        
        with self.assertRaises(InitialSchedulingError):
            initial_greedy_schedule(self.customers, None)

        unavailable_contractors = [
            Contractor(0, (0, 0), DEFAULT_CONTRACTOR_RATE),
            Contractor(1, (GRID_SIZE-1, GRID_SIZE-1), DEFAULT_CONTRACTOR_RATE + 0.1)
        ]
        unavailable_master_calendar = MasterContractorCalendar()
        for contractor in unavailable_contractors:
            unavailable_master_calendar.add_contractor(contractor)
            for day in range(SCHEDULING_DAYS):
                date = datetime.now().date() + timedelta(days=day)
                start_time = datetime.combine(date, WORK_START_TIME_OBJ)
                end_time = datetime.combine(date, WORK_END_TIME_OBJ)
                errand_id = f"test_errand_{contractor.id}_{day}"
                unavailable_master_calendar.reserve_time_slot(contractor.id, errand_id, start_time, end_time)
        
        with self.assertRaises(InitialSchedulingError):
            initial_greedy_schedule(self.customers, unavailable_contractors)

    def test_back_to_back_assignments(self) -> None:
        close_customers: List[Customer] = self._generate_customers(2)
        for customer in close_customers:
            customer.desired_errand.base_time = timedelta(minutes=30)
            customer.location = (10, 10)  # Set close locations
        
        schedule: Schedule = initial_greedy_schedule(close_customers, [self.contractors[0]])
        
        assignments = list(schedule.assignments.values())[0]
        self.assertEqual(len(assignments), 2)
        _, contractor, start_time1 = assignments[0]
        customer2, _, start_time2 = assignments[1]
        total_time = calculate_total_time(contractor, customer2, customer2.desired_errand)
        expected_start_time2 = start_time1 + timedelta(minutes=30) + (total_time - customer2.desired_errand.base_time)
        self.assertEqual(start_time2, expected_start_time2)

    def test_assignments_spanning_multiple_days(self) -> None:
        long_errand_customers: List[Customer] = self._generate_customers(3)
        for customer in long_errand_customers:
            customer.desired_errand.base_time = timedelta(hours=10)
        
        schedule: Schedule = initial_greedy_schedule(long_errand_customers, self.contractors)
        
        self.assertGreater(len(schedule.assignments), 1)
        
        for day, assignments in schedule.assignments.items():
            for customer, contractor, start_time in assignments:
                end_time = start_time + customer.desired_errand.base_time
                self.assertLessEqual(end_time.time(), WORK_END_TIME_OBJ)

    def test_no_overlapping_assignments(self) -> None:
        schedule: Schedule = initial_greedy_schedule(self.customers, self.contractors)
        
        for day, assignments in schedule.assignments.items():
            contractor_assignments: Dict[int, List[Tuple[datetime, datetime]]] = {contractor.id: [] for contractor in self.contractors}
            for customer, contractor, start_time in assignments:
                end_time = start_time + customer.desired_errand.base_time
                contractor_assignments[contractor.id].append((start_time, end_time))
            
            for contractor_id, time_slots in contractor_assignments.items():
                sorted_slots = sorted(time_slots)
                for i in range(1, len(sorted_slots)):
                    self.assertLess(sorted_slots[i-1][1], sorted_slots[i][0],
                                    f"Overlapping assignments for contractor {contractor_id}")

    def test_customer_availability_respected(self) -> None:
        start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        limited_customer = Customer(
            3, (40, 40), 
            Errand(3, ERRAND_TYPES[0][0], timedelta(minutes=ERRAND_TYPES[0][1]), ERRAND_TYPES[0][2], ERRAND_TYPES[0][3]),
            {start_date: [(datetime.combine(start_date, WORK_START_TIME_OBJ), 
                           datetime.combine(start_date, WORK_START_TIME_OBJ) + timedelta(hours=2))]}  # Only available for 2 hours on the first day
        )
        
        customers_with_limited = self.customers + [limited_customer]
        schedule: Schedule = initial_greedy_schedule(customers_with_limited, self.contractors)
        
        for day, assignments in schedule.assignments.items():
            for customer, _, start_time in assignments:
                if customer.id == limited_customer.id:
                    self.assertEqual(day.date(), start_date.date())  # Should be scheduled on the first day
                    self.assertGreaterEqual(start_time.time(), WORK_START_TIME_OBJ)
                    self.assertLess(start_time.time(), (datetime.combine(start_date, WORK_START_TIME_OBJ) + timedelta(hours=2)).time())
                    return  # Test passes if we find the limited customer scheduled correctly
        
        self.fail("Limited availability customer was not scheduled")

    def test_respect_availability_slots(self) -> None:
        start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        contractor = self.contractors[0]
        
        # Create a complex availability pattern
        contractor.calendar.calendar[start_date] = [
            contractor.calendar.ContractorAvailabilitySlot(
                datetime.combine(start_date, datetime.min.time().replace(hour=9, minute=0)),
                datetime.combine(start_date, datetime.min.time().replace(hour=11, minute=0))
            ),
            contractor.calendar.ContractorAvailabilitySlot(
                datetime.combine(start_date, datetime.min.time().replace(hour=13, minute=0)),
                datetime.combine(start_date, datetime.min.time().replace(hour=17, minute=0))
            )
        ]

        schedule: Schedule = initial_greedy_schedule(self.customers, [contractor])

        for day, assignments in schedule.assignments.items():
            if day.date() == start_date.date():
                for customer, assigned_contractor, start_time in assignments:
                    end_time = start_time + customer.desired_errand.base_time
                    self.assertTrue(
                        (9 <= start_time.hour < 11) or (13 <= start_time.hour < 17),
                        f"Errand for customer {customer.id} is scheduled outside of available slots"
                    )
                    self.assertTrue(
                        (9 <= end_time.hour <= 11) or (13 <= end_time.hour <= 17),
                        f"Errand for customer {customer.id} ends outside of available slots"
                    )

if __name__ == '__main__':
    unittest.main()