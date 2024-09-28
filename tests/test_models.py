import unittest
from models.customer import Customer
from models.contractor import Contractor
from models.errand import Errand
from models.schedule import Schedule
from utils.travel_time import calculate_travel_time
from utils.errand_utils import calculate_errand_time
from datetime import datetime, timedelta
from constants import (
    ERRAND_RATES, MAX_INCENTIVE_MULTIPLIER, WORK_START_TIME, WORK_END_TIME,
    SCHEDULING_DAYS, DEFAULT_NUM_CUSTOMERS, DEFAULT_NUM_CONTRACTORS
)

class TestModels(unittest.TestCase):
    def setUp(self):
        self.errand = Errand(0, "Grocery Shopping", 60, 1.5, None)
        self.customer = Customer(0, (10, 10), self.errand, {0: list(range(WORK_START_TIME, WORK_END_TIME, 30))})
        self.contractor = Contractor(0, (0, 0))
        self.schedule = Schedule([self.contractor], [self.customer])

    def test_errand(self):
        self.assertEqual(self.errand.id, 0)
        self.assertEqual(self.errand.type, "Grocery Shopping")
        self.assertEqual(self.errand.base_time, 60)
        expected_charge = 60 * ERRAND_RATES.get("Grocery Shopping", 1)
        self.assertAlmostEqual(self.errand.charge, expected_charge, places=2)

    def test_errand_incentive_cap(self):
        # Test with an incentive that would exceed MAX_INCENTIVE_MULTIPLIER
        high_incentive_errand = Errand(1, "Grocery Shopping", 60, MAX_INCENTIVE_MULTIPLIER + 0.5, None)
        base_charge = high_incentive_errand.charge
        incentive_charge = high_incentive_errand.apply_incentive(datetime.now().date(), datetime.now())
        self.assertAlmostEqual(incentive_charge, base_charge * MAX_INCENTIVE_MULTIPLIER, places=2)

        # Test with an incentive that is exactly MAX_INCENTIVE_MULTIPLIER
        exact_incentive_errand = Errand(2, "Grocery Shopping", 60, MAX_INCENTIVE_MULTIPLIER, None)
        base_charge = exact_incentive_errand.charge
        incentive_charge = exact_incentive_errand.apply_incentive(datetime.now().date(), datetime.now())
        self.assertAlmostEqual(incentive_charge, base_charge * MAX_INCENTIVE_MULTIPLIER, places=2)

        # Test with an incentive that is less than MAX_INCENTIVE_MULTIPLIER
        low_incentive_errand = Errand(3, "Grocery Shopping", 60, MAX_INCENTIVE_MULTIPLIER - 0.3, None)
        base_charge = low_incentive_errand.charge
        incentive_charge = low_incentive_errand.apply_incentive(datetime.now().date(), datetime.now())
        self.assertAlmostEqual(incentive_charge, base_charge * (MAX_INCENTIVE_MULTIPLIER - 0.3), places=2)

    def test_customer(self):
        self.assertEqual(self.customer.id, 0)
        self.assertEqual(self.customer.location, (10, 10))
        self.assertEqual(self.customer.desired_errand, self.errand)
        self.assertIn(0, self.customer.availability)
        expected_slots = (WORK_END_TIME - WORK_START_TIME) // 30
        self.assertEqual(len(self.customer.availability[0]), expected_slots)

    def test_contractor(self):
        self.assertEqual(self.contractor.id, 0)
        self.assertEqual(self.contractor.location, (0, 0))
        self.assertEqual(self.contractor.schedule, {})

    def test_schedule(self):
        self.assertEqual(len(self.schedule.contractors), 1)
        self.assertEqual(len(self.schedule.customers), 1)
        self.assertEqual(self.schedule.assignments, {})

    def test_schedule_assignment(self):
        self.schedule.assignments = {0: [(self.customer, self.contractor, WORK_START_TIME)]}
        self.assertIn(0, self.schedule.assignments)
        self.assertEqual(len(self.schedule.assignments[0]), 1)
        customer, contractor, start_time = self.schedule.assignments[0][0]
        self.assertEqual(customer, self.customer)
        self.assertEqual(contractor, self.contractor)
        self.assertEqual(start_time, WORK_START_TIME)

    def test_schedule_profit_calculation(self):
        self.schedule.assignments = {0: [(self.customer, self.contractor, WORK_START_TIME)]}
        profit = self.schedule.calculate_total_profit()
        
        # Calculate travel time
        travel_time, _ = calculate_travel_time(self.contractor.location, self.customer.location)
        
        # Calculate errand time
        errand_time = calculate_errand_time(self.errand, self.contractor.location, self.customer.location)
        
        # Calculate contractor cost
        contractor_cost = (travel_time + errand_time) * Schedule.contractor_cost_per_minute
        
        # Calculate final charge
        final_charge = self.errand.calculate_final_charge(datetime.now().date(), datetime.now())
        
        # Calculate expected profit
        expected_profit = final_charge - contractor_cost
        
        self.assertAlmostEqual(profit, expected_profit, places=2)

if __name__ == '__main__':
    unittest.main()