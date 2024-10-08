import unittest
import datetime
from utils.time_utils import (
    convert_minutes_to_time,
    is_time_within_range,
    get_next_working_day,
    calculate_time_difference
)
from constants import WORK_START_TIME_OBJ, WORK_END_TIME_OBJ

class TestTimeUtils(unittest.TestCase):

    def test_convert_minutes_to_time(self):
        self.assertEqual(convert_minutes_to_time(0), datetime.time(0, 0))
        self.assertEqual(convert_minutes_to_time(60), datetime.time(1, 0))
        self.assertEqual(convert_minutes_to_time(1439), datetime.time(23, 59))
        with self.assertRaises(ValueError):
            convert_minutes_to_time(-1)
        with self.assertRaises(ValueError):
            convert_minutes_to_time(1440)

    def test_is_time_within_range(self):
        self.assertTrue(is_time_within_range(
            datetime.time(12, 0),
            datetime.time(9, 0),
            datetime.time(17, 0)
        ))
        self.assertFalse(is_time_within_range(
            datetime.time(8, 0),
            datetime.time(9, 0),
            datetime.time(17, 0)
        ))
        self.assertTrue(is_time_within_range(
            datetime.time(23, 0),
            datetime.time(22, 0),
            datetime.time(6, 0)
        ))
        self.assertTrue(is_time_within_range(
            datetime.time(1, 0),
            datetime.time(22, 0),
            datetime.time(6, 0)
        ))

    def test_get_next_working_day(self):
        friday = datetime.date(2023, 6, 2)
        saturday = datetime.date(2023, 6, 3)
        sunday = datetime.date(2023, 6, 4)
        monday = datetime.date(2023, 6, 5)
        
        self.assertEqual(get_next_working_day(friday), monday)
        self.assertEqual(get_next_working_day(saturday), monday)
        self.assertEqual(get_next_working_day(sunday), monday)
        self.assertEqual(get_next_working_day(monday), datetime.date(2023, 6, 6))

    def test_calculate_time_difference(self):
        # Test with datetime objects
        start_dt = datetime.datetime(2023, 6, 1, 9, 0)
        end_dt = datetime.datetime(2023, 6, 1, 17, 0)
        self.assertEqual(calculate_time_difference(start_dt, end_dt), datetime.timedelta(hours=8))

        # Test with time objects
        start_t = datetime.time(9, 0)
        end_t = datetime.time(17, 0)
        self.assertEqual(calculate_time_difference(start_t, end_t), datetime.timedelta(hours=8))

        # Test with time objects spanning midnight
        start_t = datetime.time(22, 0)
        end_t = datetime.time(2, 0)
        with self.assertRaises(ValueError):
            calculate_time_difference(start_t, end_t)

        # Test with mismatched types
        with self.assertRaises(TypeError):
            calculate_time_difference(start_dt, end_t)

    def test_work_time_constants(self):
        # Test that WORK_START_TIME_OBJ and WORK_END_TIME_OBJ are valid time objects
        self.assertIsInstance(WORK_START_TIME_OBJ, datetime.time)
        self.assertIsInstance(WORK_END_TIME_OBJ, datetime.time)

        # Test that WORK_START_TIME_OBJ is before WORK_END_TIME_OBJ
        self.assertLess(WORK_START_TIME_OBJ, WORK_END_TIME_OBJ)

        # Test is_time_within_range with WORK_START_TIME_OBJ and WORK_END_TIME_OBJ
        self.assertTrue(is_time_within_range(
            datetime.time(12, 0),
            WORK_START_TIME_OBJ,
            WORK_END_TIME_OBJ
        ))
        self.assertFalse(is_time_within_range(
            datetime.time(7, 0),  # Assuming work doesn't start this early
            WORK_START_TIME_OBJ,
            WORK_END_TIME_OBJ
        ))

        # Test calculate_time_difference with WORK_START_TIME_OBJ and WORK_END_TIME_OBJ
        work_duration = calculate_time_difference(WORK_START_TIME_OBJ, WORK_END_TIME_OBJ)
        self.assertGreater(work_duration, datetime.timedelta(hours=0))
        self.assertLess(work_duration, datetime.timedelta(hours=24))

if __name__ == '__main__':
    unittest.main()