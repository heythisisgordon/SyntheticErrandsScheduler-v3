import unittest
from typing import Dict, List
from models.customer import Customer
from models.contractor import Contractor
from models.errand import Errand
from models.schedule import Schedule
from utils.travel_time import calculate_travel_time
from utils.errand_utils import get_errand_time
from datetime import datetime, timedelta, date
from constants import (
    ERRAND_RATES, MAX_INCENTIVE_MULTIPLIER, WORK_START_TIME, WORK_END_TIME,
    SCHEDULING_DAYS, DEFAULT_NUM_CUSTOMERS, DEFAULT_NUM_CONTRACTORS, ErrandType
)

class TestModels(unittest.TestCase):
    def setUp(self) -> None:
        self.errand: Errand = Errand(0, ErrandType.GROCERY_SHOPPING, timedelta(minutes=60), 1.5, None)
        self.customer: Customer = Customer(0, (10, 10), self.errand, {0: list(range(WORK_START_TIME, WORK_END_TIME, 30))})
        self.contractor: Contractor = Contractor(0, (0, 0))
        self.schedule: Schedule = Schedule([self.contractor], [self.customer])

    def test_errand(self) -> None:
        self.assertEqual(self.errand.id, 0)
        self.assertEqual(self.errand.type, ErrandType.GROCERY_SHOPPING)
        self.assertEqual(self.errand.base_time, timedelta(minutes=60))
        expected_charge: float = 60 * ERRAND_RATES.get(ErrandType.GROCERY_SHOPPING, 1)
        self.assertAlmostEqual(self.errand.charge, expected_charge, places=2)

    def test_errand_incentive_cap(self) -> None:
        # Test with an incentive that would exceed MAX_INCENTIVE_MULTIPLIER
        high_incentive_errand: Errand = Errand(1, ErrandType.GROCERY_SHOPPING, timedelta(minutes=60), MAX_INCENTIVE_MULTIPLIER + 0.5, None)
        base_charge: float = high_incentive_errand.charge
        incentive_charge: float = high_incentive_errand.apply_incentive(datetime.now(), datetime.now())
        self.assertAlmostEqual(incentive_charge, base_charge * MAX_INCENTIVE_MULTIPLIER, places=2)

        # Test with an incentive that is exactly MAX_INCENTIVE_MULTIPLIER
        exact_incentive_errand: Errand = Errand(2, ErrandType.GROCERY_SHOPPING, timedelta(minutes=60), MAX_INCENTIVE_MULTIPLIER, None)
        base_charge = exact_incentive_errand.charge
        incentive_charge = exact_incentive_errand.apply_incentive(datetime.now(), datetime.now())
        self.assertAlmostEqual(incentive_charge, base_charge * MAX_INCENTIVE_MULTIPLIER, places=2)

        # Test with an incentive that is less than MAX_INCENTIVE_MULTIPLIER
        low_incentive_errand: Errand = Errand(3, ErrandType.GROCERY_SHOPPING, timedelta(minutes=60), MAX_INCENTIVE_MULTIPLIER - 0.3, None)
        base_charge = low_incentive_errand.charge
        incentive_charge = low_incentive_errand.apply_incentive(datetime.now(), datetime.now())
        self.assertAlmostEqual(incentive_charge, base_charge * (MAX_INCENTIVE_MULTIPLIER - 0.3), places=2)

    def test_errand_apply_incentive_with_datetime(self) -> None:
        now = datetime.now()
        incentive_charge = self.errand.apply_incentive(now, now)
        self.assertAlmostEqual(incentive_charge, self.errand.charge * 1.5, places=2)

        tomorrow = now + timedelta(days=1)
        no_incentive_charge = self.errand.apply_incentive(tomorrow, now)
        self.assertAlmostEqual(no_incentive_charge, self.errand.charge, places=2)

    def test_errand_apply_incentive_with_date(self) -> None:
        today = date.today()
        incentive_charge = self.errand.apply_incentive(today, today)
        self.assertAlmostEqual(incentive_charge, self.errand.charge * 1.5, places=2)

        tomorrow = today + timedelta(days=1)
        no_incentive_charge = self.errand.apply_incentive(tomorrow, today)
        self.assertAlmostEqual(no_incentive_charge, self.errand.charge, places=2)

    def test_errand_apply_disincentive(self) -> None:
        errand_with_disincentive = Errand(4, ErrandType.GROCERY_SHOPPING, timedelta(minutes=60), 1.5, {'type': 'percentage', 'value': 10})
        
        # Test with datetime
        now = datetime.now()
        late_date = now + timedelta(days=SCHEDULING_DAYS + 2)
        disincentive_charge = errand_with_disincentive.apply_disincentive(late_date, now)
        expected_charge = errand_with_disincentive.charge * (1 - 0.2)  # 20% reduction for 2 days late
        self.assertAlmostEqual(disincentive_charge, expected_charge, places=2)

        # Test with date
        today = date.today()
        late_date = today + timedelta(days=SCHEDULING_DAYS + 2)
        disincentive_charge = errand_with_disincentive.apply_disincentive(late_date, today)
        self.assertAlmostEqual(disincentive_charge, expected_charge, places=2)

    def test_errand_calculate_final_charge(self) -> None:
        errand_with_disincentive = Errand(5, ErrandType.GROCERY_SHOPPING, timedelta(minutes=60), 1.5, {'type': 'percentage', 'value': 10})
        
        # Test with datetime
        now = datetime.now()
        same_day_charge = errand_with_disincentive.calculate_final_charge(now, now)
        self.assertAlmostEqual(same_day_charge, errand_with_disincentive.charge * 1.5, places=2)

        late_date = now + timedelta(days=SCHEDULING_DAYS + 2)
        late_charge = errand_with_disincentive.calculate_final_charge(late_date, now)
        expected_charge = errand_with_disincentive.charge * (1 - 0.2)  # 20% reduction for 2 days late
        self.assertAlmostEqual(late_charge, expected_charge, places=2)

        # Test with date
        today = date.today()
        same_day_charge = errand_with_disincentive.calculate_final_charge(today, today)
        self.assertAlmostEqual(same_day_charge, errand_with_disincentive.charge * 1.5, places=2)

        late_date = today + timedelta(days=SCHEDULING_DAYS + 2)
        late_charge = errand_with_disincentive.calculate_final_charge(late_date, today)
        self.assertAlmostEqual(late_charge, expected_charge, places=2)

    def test_customer(self) -> None:
        self.assertEqual(self.customer.id, 0)
        self.assertEqual(self.customer.location, (10, 10))
        self.assertEqual(self.customer.desired_errand, self.errand)
        self.assertIn(0, self.customer.availability)
        expected_slots: int = (WORK_END_TIME - WORK_START_TIME) // 30
        self.assertEqual(len(self.customer.availability[0]), expected_slots)

    def test_contractor(self) -> None:
        self.assertEqual(self.contractor.id, 0)
        self.assertEqual(self.contractor.location, (0, 0))
        self.assertEqual(self.contractor.schedule, {})

    def test_schedule(self) -> None:
        self.assertEqual(len(self.schedule.contractors), 1)
        self.assertEqual(len(self.schedule.customers), 1)
        self.assertEqual(self.schedule.assignments, {})

    def test_schedule_assignment(self) -> None:
        start_time = datetime.combine(datetime.now().date(), datetime.min.time().replace(hour=WORK_START_TIME // 60, minute=WORK_START_TIME % 60))
        self.schedule.assignments = {datetime.now().date(): [(self.customer, self.contractor, start_time)]}
        self.assertIn(datetime.now().date(), self.schedule.assignments)
        self.assertEqual(len(self.schedule.assignments[datetime.now().date()]), 1)
        customer, contractor, assigned_start_time = self.schedule.assignments[datetime.now().date()][0]
        self.assertEqual(customer, self.customer)
        self.assertEqual(contractor, self.contractor)
        self.assertEqual(assigned_start_time, start_time)

    def test_schedule_profit_calculation(self) -> None:
        start_time = datetime.combine(datetime.now().date(), datetime.min.time().replace(hour=WORK_START_TIME // 60, minute=WORK_START_TIME % 60))
        self.schedule.assignments = {datetime.now().date(): [(self.customer, self.contractor, start_time)]}
        profit: float = self.schedule.calculate_total_profit()
        
        # Calculate travel time
        travel_time, _ = calculate_travel_time(self.contractor.location, self.customer.location)
        
        # Calculate errand time
        errand_time: timedelta = get_errand_time(self.errand, self.contractor.location, self.customer.location)
        
        # Calculate contractor cost
        contractor_cost: float = (travel_time + errand_time).total_seconds() / 60 * Schedule.contractor_cost_per_minute
        
        # Calculate final charge
        final_charge: float = self.errand.calculate_final_charge(start_time, datetime.now())
        
        # Calculate expected profit
        expected_profit: float = final_charge - contractor_cost
        
        self.assertAlmostEqual(profit, expected_profit, places=2)

if __name__ == '__main__':
    unittest.main()