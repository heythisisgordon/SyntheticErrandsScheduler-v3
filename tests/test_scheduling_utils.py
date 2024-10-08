import unittest
from datetime import datetime, timedelta, date
from models.contractor import Contractor
from models.customer import Customer
from models.errand import Errand
from models.contractor_calendar import ContractorCalendar, ContractorAvailabilitySlot
from utils.scheduling_utils import (
    find_next_available_slot,
    is_valid_assignment,
    calculate_assignment_profit,
    calculate_next_available_time,
    split_availability_slot
)
from constants import ErrandType, WORK_START_TIME_OBJ, WORK_END_TIME_OBJ, SCHEDULING_DAYS

class TestSchedulingUtils(unittest.TestCase):
    def setUp(self):
        self.contractor = Contractor(1, (0, 0), 10.0)
        self.customer = Customer(1, (10, 10), Errand(1, ErrandType.SHOPPING, timedelta(minutes=60), 1.0, None))
        self.start_datetime = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
        
        # Set up customer availability
        self.customer.availability = {
            self.start_datetime.date(): [
                (self.start_datetime.replace(hour=9), self.start_datetime.replace(hour=17))
            ]
        }

    def test_contractor_calendar_initialization(self):
        calendar = ContractorCalendar()
        start_date = date.today()
        
        # Check that all days within SCHEDULING_DAYS are initialized
        for day in range(SCHEDULING_DAYS):
            current_date = start_date + timedelta(days=day)
            self.assertIn(current_date, calendar.calendar)
            self.assertEqual(len(calendar.calendar[current_date]), 1)
            self.assertIsInstance(calendar.calendar[current_date][0], ContractorAvailabilitySlot)
            self.assertEqual(calendar.calendar[current_date][0].start_time.time(), WORK_START_TIME_OBJ)
            self.assertEqual(calendar.calendar[current_date][0].end_time.time(), WORK_END_TIME_OBJ)

        # Check that a date beyond SCHEDULING_DAYS is not in the calendar
        beyond_date = start_date + timedelta(days=SCHEDULING_DAYS)
        self.assertNotIn(beyond_date, calendar.calendar)

    def test_find_next_available_slot(self):
        calendar = ContractorCalendar()
        duration = timedelta(hours=2)

        # Test with an empty calendar
        next_slot = find_next_available_slot(calendar, self.start_datetime, duration)
        self.assertIsNotNone(next_slot)
        self.assertEqual(next_slot.time(), WORK_START_TIME_OBJ)

        # Test with a busy slot
        busy_start = self.start_datetime.replace(hour=10, minute=0)
        busy_end = busy_start + timedelta(hours=1)
        calendar.reserve_time_slot("test_errand", busy_start, busy_end)

        next_slot = find_next_available_slot(calendar, self.start_datetime, duration)
        self.assertIsNotNone(next_slot)
        self.assertTrue(next_slot >= busy_end)

    def test_is_valid_assignment(self):
        start_time = self.start_datetime.replace(hour=10, minute=0)
        end_time = start_time + timedelta(hours=2)

        # Test valid assignment
        self.assertTrue(is_valid_assignment(self.contractor, self.customer, start_time, end_time))

        # Test invalid assignment (outside working hours)
        invalid_start = self.start_datetime.replace(hour=WORK_END_TIME_OBJ.hour + 1, minute=0)
        invalid_end = invalid_start + timedelta(hours=2)
        self.assertFalse(is_valid_assignment(self.contractor, self.customer, invalid_start, invalid_end))

        # Test invalid assignment (contractor not available)
        self.contractor.calendar.reserve_time_slot("test_errand", start_time, end_time)
        self.assertFalse(is_valid_assignment(self.contractor, self.customer, start_time, end_time))

        # Test invalid assignment (customer not available)
        self.customer.availability[self.start_datetime.date()] = [
            (self.start_datetime.replace(hour=13), self.start_datetime.replace(hour=17))
        ]
        self.assertFalse(is_valid_assignment(self.contractor, self.customer, start_time, end_time))

        # Test invalid assignment (not enough time for travel)
        early_start = self.start_datetime.replace(hour=WORK_START_TIME_OBJ.hour, minute=0)
        self.assertFalse(is_valid_assignment(self.contractor, self.customer, early_start, early_start + timedelta(hours=1)))

    def test_calculate_assignment_profit(self):
        start_time = self.start_datetime.replace(hour=10, minute=0)
        end_time = start_time + timedelta(hours=2)

        profit = calculate_assignment_profit(self.customer, self.contractor, start_time, end_time)
        self.assertIsInstance(profit, float)
        self.assertGreater(profit, 0)  # Assuming the profit should be positive

        # Test with different contractor rates
        self.contractor.rate = 20.0
        higher_rate_profit = calculate_assignment_profit(self.customer, self.contractor, start_time, end_time)
        self.assertLess(higher_rate_profit, profit)  # Higher rate should result in lower profit

    def test_calculate_next_available_time(self):
        # Test with an empty calendar
        next_time = calculate_next_available_time(self.contractor, self.customer, self.start_datetime)
        self.assertIsNotNone(next_time)
        self.assertEqual(next_time.time(), WORK_START_TIME_OBJ)

        # Test with a busy slot
        busy_start = self.start_datetime.replace(hour=10, minute=0)
        busy_end = busy_start + timedelta(hours=1)
        self.contractor.calendar.reserve_time_slot("test_errand", busy_start, busy_end)

        next_time = calculate_next_available_time(self.contractor, self.customer, self.start_datetime)
        self.assertIsNotNone(next_time)
        self.assertTrue(next_time >= busy_end)

        # Test with no available slot on the current day
        self.contractor.calendar.reserve_time_slot(
            "test_errand",
            self.start_datetime.replace(hour=WORK_START_TIME_OBJ.hour, minute=WORK_START_TIME_OBJ.minute),
            self.start_datetime.replace(hour=WORK_END_TIME_OBJ.hour, minute=WORK_END_TIME_OBJ.minute)
        )
        next_time = calculate_next_available_time(self.contractor, self.customer, self.start_datetime)
        self.assertIsNotNone(next_time)
        self.assertEqual(next_time.date(), self.start_datetime.date() + timedelta(days=1))

    def test_contractor_calendar_scheduling_days_limit(self):
        calendar = ContractorCalendar()
        start_date = datetime.now().date()
        last_valid_date = start_date + timedelta(days=SCHEDULING_DAYS - 1)
        beyond_limit_date = start_date + timedelta(days=SCHEDULING_DAYS)

        # Test scheduling within the limit
        self.assertTrue(calendar.is_available(
            datetime.combine(last_valid_date, WORK_START_TIME_OBJ),
            datetime.combine(last_valid_date, WORK_START_TIME_OBJ) + timedelta(hours=1)
        ))

        # Test scheduling beyond the limit
        self.assertFalse(calendar.is_available(
            datetime.combine(beyond_limit_date, WORK_START_TIME_OBJ),
            datetime.combine(beyond_limit_date, WORK_START_TIME_OBJ) + timedelta(hours=1)
        ))

    def test_split_availability_slot(self):
        start_time = self.start_datetime.replace(hour=9, minute=0)
        end_time = self.start_datetime.replace(hour=17, minute=0)
        slot = ContractorAvailabilitySlot(start_time, end_time)

        # Test splitting in the middle
        errand_start = self.start_datetime.replace(hour=12, minute=0)
        errand_end = self.start_datetime.replace(hour=13, minute=0)
        new_slots = split_availability_slot(slot, errand_start, errand_end)
        self.assertEqual(len(new_slots), 2)
        self.assertEqual(new_slots[0].start_time, start_time)
        self.assertEqual(new_slots[0].end_time, errand_start)
        self.assertEqual(new_slots[1].start_time, errand_end)
        self.assertEqual(new_slots[1].end_time, end_time)

        # Test splitting at the start
        errand_start = start_time
        errand_end = self.start_datetime.replace(hour=10, minute=0)
        new_slots = split_availability_slot(slot, errand_start, errand_end)
        self.assertEqual(len(new_slots), 1)
        self.assertEqual(new_slots[0].start_time, errand_end)
        self.assertEqual(new_slots[0].end_time, end_time)

        # Test splitting at the end
        errand_start = self.start_datetime.replace(hour=16, minute=0)
        errand_end = end_time
        new_slots = split_availability_slot(slot, errand_start, errand_end)
        self.assertEqual(len(new_slots), 1)
        self.assertEqual(new_slots[0].start_time, start_time)
        self.assertEqual(new_slots[0].end_time, errand_start)

        # Test errand covering the entire slot
        new_slots = split_availability_slot(slot, start_time, end_time)
        self.assertEqual(len(new_slots), 0)

if __name__ == '__main__':
    unittest.main()