import unittest
from datetime import datetime, timedelta
from models.master_contractor_calendar import MasterContractorCalendar
from models.contractor import Contractor
from models.contractor_calendar import ContractorCalendar, ContractorAvailabilitySlot
from constants import SCHEDULING_DAYS, WORK_START_TIME_OBJ, WORK_END_TIME_OBJ

class TestMasterContractorCalendar(unittest.TestCase):
    def setUp(self):
        self.master_calendar = MasterContractorCalendar()
        self.contractor1 = Contractor(1, (0, 0), 0.5)
        self.contractor2 = Contractor(2, (10, 10), 0.6)
        self.master_calendar.add_contractor(self.contractor1)
        self.master_calendar.add_contractor(self.contractor2)

    def test_add_contractor(self):
        self.assertIn(self.contractor1.id, self.master_calendar.contractor_calendars)
        self.assertIn(self.contractor2.id, self.master_calendar.contractor_calendars)
        self.assertIsInstance(self.master_calendar.contractor_calendars[self.contractor1.id], ContractorCalendar)

    def test_find_first_available_slot(self):
        start_datetime = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
        duration = timedelta(hours=1)
        contractor_id, slot = self.master_calendar.find_first_available_slot(start_datetime, duration)
        self.assertIsNotNone(contractor_id)
        self.assertIsNotNone(slot)
        self.assertGreaterEqual(slot['start'], start_datetime)
        self.assertEqual(slot['end'] - slot['start'], duration)

    def test_reserve_time_slot(self):
        start_time = datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)
        end_time = start_time + timedelta(hours=1)
        errand_id = "test_errand"
        self.assertTrue(self.master_calendar.reserve_time_slot(self.contractor1.id, errand_id, start_time, end_time))
        self.assertFalse(self.master_calendar.is_contractor_available(self.contractor1.id, start_time, end_time))

    def test_is_contractor_available(self):
        start_time = datetime.now().replace(hour=11, minute=0, second=0, microsecond=0)
        end_time = start_time + timedelta(hours=1)
        self.assertTrue(self.master_calendar.is_contractor_available(self.contractor1.id, start_time, end_time))
        self.master_calendar.reserve_time_slot(self.contractor1.id, "test_errand", start_time, end_time)
        self.assertFalse(self.master_calendar.is_contractor_available(self.contractor1.id, start_time, end_time))

    def test_get_contractor_next_available_slot(self):
        start_time = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
        duration = timedelta(hours=1)
        slot = self.master_calendar.get_contractor_next_available_slot(self.contractor1.id, start_time, duration)
        self.assertIsNotNone(slot)
        self.assertGreaterEqual(slot['start'], start_time)
        self.assertEqual(slot['end'] - slot['start'], duration)

    def test_get_contractor_errands(self):
        start_time = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
        end_time = start_time + timedelta(hours=1)
        errand_id = "test_errand"
        self.master_calendar.reserve_time_slot(self.contractor1.id, errand_id, start_time, end_time)
        errands = self.master_calendar.get_contractor_errands(self.contractor1.id, start_time)
        self.assertEqual(len(errands), 1)
        self.assertEqual(errands[0].errand_id, errand_id)
        self.assertEqual(errands[0].start_time, start_time)
        self.assertEqual(errands[0].end_time, end_time)

    def test_get_contractor_availability(self):
        date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        availability = self.master_calendar.get_contractor_availability(self.contractor1.id, date)
        self.assertIsInstance(availability, list)
        self.assertTrue(all(isinstance(slot, ContractorAvailabilitySlot) for slot in availability))
        
        # Check for specific time ranges
        self.assertTrue(any(slot.start_time.time() == WORK_START_TIME_OBJ for slot in availability))
        self.assertTrue(any(slot.end_time.time() == WORK_END_TIME_OBJ for slot in availability))

    def test_error_handling(self):
        with self.assertRaises(ValueError):
            self.master_calendar.reserve_time_slot("non_existent_id", "test_errand", datetime.now(), datetime.now() + timedelta(hours=1))
        with self.assertRaises(ValueError):
            self.master_calendar.is_contractor_available("non_existent_id", datetime.now(), datetime.now() + timedelta(hours=1))
        with self.assertRaises(ValueError):
            self.master_calendar.get_contractor_next_available_slot("non_existent_id", datetime.now(), timedelta(hours=1))
        with self.assertRaises(ValueError):
            self.master_calendar.get_contractor_errands("non_existent_id", datetime.now())
        with self.assertRaises(ValueError):
            self.master_calendar.get_contractor_availability("non_existent_id", datetime.now())

    def test_overlapping_time_slots(self):
        start_time1 = datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)
        end_time1 = start_time1 + timedelta(hours=2)
        start_time2 = start_time1 + timedelta(hours=1)
        end_time2 = start_time2 + timedelta(hours=2)

        self.assertTrue(self.master_calendar.reserve_time_slot(self.contractor1.id, "errand1", start_time1, end_time1))
        self.assertFalse(self.master_calendar.reserve_time_slot(self.contractor1.id, "errand2", start_time2, end_time2))

    def test_split_availability_slot(self):
        start_time = datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)
        end_time = start_time + timedelta(hours=1)

        # Reserve a time slot
        self.master_calendar.reserve_time_slot(self.contractor1.id, "test_errand", start_time, end_time)

        # Get the availability for the day
        date = start_time.replace(hour=0, minute=0, second=0, microsecond=0)
        availability = self.master_calendar.get_contractor_availability(self.contractor1.id, date)

        # Check if the availability slot was split
        self.assertTrue(any(slot.end_time == start_time for slot in availability))
        self.assertTrue(any(slot.start_time == end_time for slot in availability))

    def test_scheduling_days_limit(self):
        start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        last_valid_date = start_date + timedelta(days=SCHEDULING_DAYS - 1)
        beyond_limit_date = start_date + timedelta(days=SCHEDULING_DAYS)

        # Test scheduling within the limit
        self.assertTrue(self.master_calendar.is_contractor_available(
            self.contractor1.id,
            last_valid_date.replace(hour=WORK_START_TIME_OBJ.hour, minute=WORK_START_TIME_OBJ.minute),
            last_valid_date.replace(hour=WORK_START_TIME_OBJ.hour, minute=WORK_START_TIME_OBJ.minute) + timedelta(hours=1)
        ))

        # Test scheduling beyond the limit
        self.assertFalse(self.master_calendar.is_contractor_available(
            self.contractor1.id,
            beyond_limit_date.replace(hour=WORK_START_TIME_OBJ.hour, minute=WORK_START_TIME_OBJ.minute),
            beyond_limit_date.replace(hour=WORK_START_TIME_OBJ.hour, minute=WORK_START_TIME_OBJ.minute) + timedelta(hours=1)
        ))

    def test_datetime_consistency(self):
        start_time = datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)
        end_time = start_time + timedelta(hours=1)
        errand_id = "test_errand"

        # Reserve a time slot
        self.master_calendar.reserve_time_slot(self.contractor1.id, errand_id, start_time, end_time)

        # Check availability
        self.assertFalse(self.master_calendar.is_contractor_available(self.contractor1.id, start_time, end_time))

        # Get next available slot
        next_slot = self.master_calendar.get_contractor_next_available_slot(self.contractor1.id, start_time, timedelta(hours=1))
        self.assertGreaterEqual(next_slot['start'], end_time)

        # Get contractor errands
        errands = self.master_calendar.get_contractor_errands(self.contractor1.id, start_time)
        self.assertEqual(len(errands), 1)
        self.assertEqual(errands[0].start_time, start_time)
        self.assertEqual(errands[0].end_time, end_time)

if __name__ == '__main__':
    unittest.main()