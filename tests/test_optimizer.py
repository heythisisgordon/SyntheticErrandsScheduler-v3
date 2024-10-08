import unittest
from typing import List, Dict, Tuple, Optional
from datetime import datetime, timedelta
from models.customer import Customer
from models.contractor import Contractor
from models.errand import Errand
from models.schedule import Schedule
from algorithms.CP_SAT_optimizer import optimize_schedule, is_valid_schedule
from algorithms.vehicle_routing_optimizer import optimize_schedule_vrp
from utils.city_map import GRID_SIZE
from constants import SCHEDULING_DAYS, ERRAND_TYPES, ErrandType, WORK_START_TIME_OBJ, WORK_END_TIME_OBJ

class TestOptimizer(unittest.TestCase):
    def setUp(self) -> None:
        # Create a sample problem for testing
        self.customers: List[Customer] = [
            Customer(i, ((i+1)*10, (i+1)*10), Errand(i, ERRAND_TYPES[i][0], timedelta(minutes=ERRAND_TYPES[i][1]), ERRAND_TYPES[i][2], ERRAND_TYPES[i][3]), 
                     {(datetime.now().date() + timedelta(days=day)): 
                      [(datetime.combine(datetime.now().date() + timedelta(days=day), WORK_START_TIME_OBJ) + timedelta(minutes=30*i), 
                        datetime.combine(datetime.now().date() + timedelta(days=day), WORK_START_TIME_OBJ) + timedelta(minutes=30*(i+1))) 
                       for i in range(int((WORK_END_TIME_OBJ.hour * 60 + WORK_END_TIME_OBJ.minute - WORK_START_TIME_OBJ.hour * 60 - WORK_START_TIME_OBJ.minute) / 30))] 
                      for day in range(SCHEDULING_DAYS)})
            for i in range(len(ERRAND_TYPES))
        ]
        self.contractors: List[Contractor] = [
            Contractor(0, (0, 0), 0.5),
            Contractor(1, (GRID_SIZE-1, GRID_SIZE-1), 0.6)
        ]
        self.schedule: Schedule = Schedule(self.contractors, self.customers)
        
        # Create a simple initial schedule
        start_date = datetime.now().date()
        self.schedule.assignments: Dict[datetime, List[Tuple[Customer, Contractor, datetime]]] = {
            datetime.combine(start_date, WORK_START_TIME_OBJ): [
                (self.customers[0], self.contractors[0], datetime.combine(start_date, WORK_START_TIME_OBJ)),
                (self.customers[1], self.contractors[0], datetime.combine(start_date, WORK_START_TIME_OBJ) + timedelta(minutes=120)),
                (self.customers[2], self.contractors[1], datetime.combine(start_date, WORK_START_TIME_OBJ))
            ],
            datetime.combine(start_date + timedelta(days=1), WORK_START_TIME_OBJ): [
                (self.customers[3], self.contractors[0], datetime.combine(start_date + timedelta(days=1), WORK_START_TIME_OBJ)),
                (self.customers[4], self.contractors[1], datetime.combine(start_date + timedelta(days=1), WORK_START_TIME_OBJ))
            ],
            datetime.combine(start_date + timedelta(days=2), WORK_START_TIME_OBJ): [
                (self.customers[5], self.contractors[0], datetime.combine(start_date + timedelta(days=2), WORK_START_TIME_OBJ))
            ]
        }

        # Reserve time slots in contractor calendars
        for day, assignments in self.schedule.assignments.items():
            for customer, contractor, start_time in assignments:
                end_time = start_time + customer.desired_errand.base_time
                errand_id = f"errand_{customer.id}_{contractor.id}_{start_time.strftime('%Y%m%d%H%M')}"
                contractor.calendar.reserve_time_slot(errand_id, start_time, end_time)

    def test_is_valid_schedule(self) -> None:
        self.assertTrue(is_valid_schedule(self.schedule))

        # Test invalid schedule (errand ends after working hours)
        invalid_schedule: Schedule = Schedule(self.contractors, self.customers)
        start_date = datetime.now().date()
        invalid_schedule.assignments = {
            datetime.combine(start_date, WORK_END_TIME_OBJ) - timedelta(minutes=20): [
                (self.customers[0], self.contractors[0], datetime.combine(start_date, WORK_END_TIME_OBJ) - timedelta(minutes=20))  # Starts 20 minutes before end of day
            ]
        }
        self.assertFalse(is_valid_schedule(invalid_schedule))

    def test_optimize_schedule_cp_sat(self) -> None:
        initial_schedule, optimized_schedule = optimize_schedule(self.schedule)
        initial_profit: float = initial_schedule.calculate_total_profit()
        optimized_profit: float = optimized_schedule.calculate_total_profit()

        self.assertGreaterEqual(optimized_profit, initial_profit)
        self.assertTrue(is_valid_schedule(optimized_schedule))
        self.assertTrue(self._check_calendar_validity(optimized_schedule))

    def test_optimize_schedule_vrp(self) -> None:
        initial_schedule, optimized_schedule = optimize_schedule_vrp(self.schedule)
        initial_profit: float = initial_schedule.calculate_total_profit()
        optimized_profit: float = optimized_schedule.calculate_total_profit()

        self.assertGreaterEqual(optimized_profit, initial_profit)
        self.assertTrue(is_valid_schedule(optimized_schedule))
        self.assertTrue(self._check_calendar_validity(optimized_schedule))

    def test_optimize_schedule_respects_constraints(self) -> None:
        _, optimized_schedule = optimize_schedule(self.schedule)

        # Check if all customers are scheduled
        scheduled_customers: set = set()
        for day_assignments in optimized_schedule.assignments.values():
            for customer, _, _ in day_assignments:
                scheduled_customers.add(customer.id)
        self.assertEqual(len(scheduled_customers), len(self.customers))

        # Check if working hours are respected
        for day_assignments in optimized_schedule.assignments.values():
            for _, _, start_time in day_assignments:
                self.assertGreaterEqual(start_time.time(), WORK_START_TIME_OBJ)
                self.assertLess(start_time.time(), WORK_END_TIME_OBJ)

    def test_optimize_schedule_handles_errand_types(self) -> None:
        _, optimized_schedule = optimize_schedule(self.schedule)

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
            datetime.combine(start_date + timedelta(days=day), WORK_START_TIME_OBJ): [
                (customer, self.contractors[0], datetime.combine(start_date + timedelta(days=day), WORK_START_TIME_OBJ) + timedelta(minutes=60 * i))
                for i, customer in enumerate(self.customers)
            ]
            for day in range(3)
        }

        initial_schedule, optimized_schedule = optimize_schedule(inefficient_schedule)
        initial_profit: float = initial_schedule.calculate_total_profit()
        optimized_profit: float = optimized_schedule.calculate_total_profit()

        self.assertGreater(optimized_profit, initial_profit)

    def test_compare_cp_sat_and_vrp(self) -> None:
        _, cp_sat_schedule = optimize_schedule(self.schedule)
        _, vrp_schedule = optimize_schedule_vrp(self.schedule)

        cp_sat_profit = cp_sat_schedule.calculate_total_profit()
        vrp_profit = vrp_schedule.calculate_total_profit()

        # Both should produce valid schedules
        self.assertTrue(is_valid_schedule(cp_sat_schedule))
        self.assertTrue(is_valid_schedule(vrp_schedule))
        self.assertTrue(self._check_calendar_validity(cp_sat_schedule))
        self.assertTrue(self._check_calendar_validity(vrp_schedule))

        # Log the profits for comparison
        print(f"CP-SAT profit: ${cp_sat_profit:.2f}")
        print(f"VRP profit: ${vrp_profit:.2f}")

        # We don't assert which one is better, as it may vary depending on the problem instance
        # Instead, we ensure both produce valid schedules and log the results for manual review

    def test_optimize_schedule_respects_contractor_calendar(self) -> None:
        # Add a pre-existing appointment to a contractor's calendar
        start_date = datetime.now().date()
        appointment_start = datetime.combine(start_date, datetime.min.time().replace(hour=10, minute=0))
        appointment_end = appointment_start + timedelta(hours=1)
        self.contractors[0].calendar.reserve_time_slot("pre_existing_appointment", appointment_start, appointment_end)

        _, optimized_schedule = optimize_schedule(self.schedule)

        # Check if the optimized schedule respects the pre-existing appointment
        for day, assignments in optimized_schedule.assignments.items():
            for customer, contractor, start_time in assignments:
                if contractor.id == 0 and day.date() == start_date:
                    end_time = start_time + customer.desired_errand.base_time
                    self.assertFalse(
                        (start_time < appointment_end and end_time > appointment_start),
                        f"Errand for customer {customer.id} conflicts with pre-existing appointment"
                    )

    def test_optimize_with_multiple_contractors_appointments(self) -> None:
        start_date = datetime.now().date()
        
        # Add pre-existing appointments to both contractors
        self.contractors[0].calendar.reserve_time_slot(
            "pre_existing_appointment_1",
            datetime.combine(start_date, datetime.min.time().replace(hour=9, minute=0)),
            datetime.combine(start_date, datetime.min.time().replace(hour=11, minute=0))
        )
        self.contractors[1].calendar.reserve_time_slot(
            "pre_existing_appointment_2",
            datetime.combine(start_date, datetime.min.time().replace(hour=13, minute=0)),
            datetime.combine(start_date, datetime.min.time().replace(hour=15, minute=0))
        )

        _, optimized_schedule = optimize_schedule(self.schedule)
        self.assertTrue(self._check_calendar_validity(optimized_schedule))

        # Check if the optimized schedule respects both pre-existing appointments
        for day, assignments in optimized_schedule.assignments.items():
            for customer, contractor, start_time in assignments:
                end_time = start_time + customer.desired_errand.base_time
                self.assertTrue(contractor.calendar.is_available(start_time, end_time),
                                f"Errand for customer {customer.id} conflicts with contractor {contractor.id}'s pre-existing appointment")

    def test_optimize_across_multiple_days(self) -> None:
        start_date = datetime.now().date()
        
        # Add pre-existing appointments for multiple days
        for i in range(3):
            day = start_date + timedelta(days=i)
            self.contractors[0].calendar.reserve_time_slot(
                f"pre_existing_appointment_day_{i}",
                datetime.combine(day, datetime.min.time().replace(hour=9, minute=0)),
                datetime.combine(day, datetime.min.time().replace(hour=11, minute=0))
            )

        _, optimized_schedule = optimize_schedule(self.schedule)
        self.assertTrue(self._check_calendar_validity(optimized_schedule))

        # Check if the optimized schedule respects appointments across multiple days
        for day, assignments in optimized_schedule.assignments.items():
            for customer, contractor, start_time in assignments:
                end_time = start_time + customer.desired_errand.base_time
                self.assertTrue(contractor.calendar.is_available(start_time, end_time),
                                f"Errand for customer {customer.id} conflicts with contractor {contractor.id}'s pre-existing appointment on {day}")

    def test_optimize_with_conflicting_appointments(self) -> None:
        start_date = datetime.now().date()
        
        # Add conflicting appointments for all contractors
        for i, contractor in enumerate(self.contractors):
            contractor.calendar.reserve_time_slot(
                f"conflicting_appointment_{i}",
                datetime.combine(start_date, datetime.min.time().replace(hour=9, minute=0)),
                datetime.combine(start_date, datetime.min.time().replace(hour=17, minute=0))
            )

        _, optimized_schedule = optimize_schedule(self.schedule)
        self.assertTrue(self._check_calendar_validity(optimized_schedule))

        # Check if the optimized schedule handles conflicting appointments
        self.assertGreater(len(optimized_schedule.assignments), 1, "Schedule should span multiple days due to conflicting appointments")
        
        for day, assignments in optimized_schedule.assignments.items():
            for customer, contractor, start_time in assignments:
                end_time = start_time + customer.desired_errand.base_time
                self.assertTrue(contractor.calendar.is_available(start_time, end_time),
                                f"Errand for customer {customer.id} conflicts with contractor {contractor.id}'s appointment on {day}")

    def test_cp_sat_and_vrp_respect_calendars(self) -> None:
        start_date = datetime.now().date()
        
        # Add pre-existing appointments
        self.contractors[0].calendar.reserve_time_slot(
            "pre_existing_appointment_1",
            datetime.combine(start_date, datetime.min.time().replace(hour=9, minute=0)),
            datetime.combine(start_date, datetime.min.time().replace(hour=11, minute=0))
        )
        self.contractors[1].calendar.reserve_time_slot(
            "pre_existing_appointment_2",
            datetime.combine(start_date, datetime.min.time().replace(hour=13, minute=0)),
            datetime.combine(start_date, datetime.min.time().replace(hour=15, minute=0))
        )

        _, cp_sat_schedule = optimize_schedule(self.schedule)
        _, vrp_schedule = optimize_schedule_vrp(self.schedule)

        self.assertTrue(self._check_calendar_validity(cp_sat_schedule), "CP-SAT optimizer does not respect contractor calendars")
        self.assertTrue(self._check_calendar_validity(vrp_schedule), "VRP optimizer does not respect contractor calendars")

    def test_optimize_respects_availability_slots(self) -> None:
        start_date = datetime.now().date()
        
        # Create a complex availability pattern
        self.contractors[0].calendar.calendar[start_date] = [
            self.contractors[0].calendar.ContractorAvailabilitySlot(
                datetime.combine(start_date, datetime.min.time().replace(hour=9, minute=0)),
                datetime.combine(start_date, datetime.min.time().replace(hour=11, minute=0))
            ),
            self.contractors[0].calendar.ContractorAvailabilitySlot(
                datetime.combine(start_date, datetime.min.time().replace(hour=13, minute=0)),
                datetime.combine(start_date, datetime.min.time().replace(hour=17, minute=0))
            )
        ]

        _, optimized_schedule = optimize_schedule(self.schedule)
        self.assertTrue(self._check_calendar_validity(optimized_schedule))

        # Check if the optimized schedule respects the complex availability pattern
        for day, assignments in optimized_schedule.assignments.items():
            if day.date() == start_date:
                for customer, contractor, start_time in assignments:
                    if contractor.id == 0:
                        end_time = start_time + customer.desired_errand.base_time
                        self.assertTrue(
                            (9 <= start_time.hour < 11) or (13 <= start_time.hour < 17),
                            f"Errand for customer {customer.id} is scheduled outside of available slots"
                        )
                        self.assertTrue(
                            (9 <= end_time.hour <= 11) or (13 <= end_time.hour <= 17),
                            f"Errand for customer {customer.id} ends outside of available slots"
                        )

    def _check_calendar_validity(self, schedule: Schedule) -> bool:
        for day, assignments in schedule.assignments.items():
            for customer, contractor, start_time in assignments:
                end_time = start_time + customer.desired_errand.base_time
                if not contractor.calendar.is_available(start_time, end_time):
                    return False
        return True

if __name__ == '__main__':
    unittest.main()