import unittest
from models.customer import Customer
from models.contractor import Contractor
from models.errand import Errand
from models.schedule import Schedule
from utils.travel_time import calculate_travel_time
from utils.errand_utils import calculate_errand_time
from datetime import datetime, timedelta

class TestModels(unittest.TestCase):
    def setUp(self):
        self.errand = Errand(0, "Grocery Shopping", 60, 1.5, None)
        self.customer = Customer(0, (10, 10), self.errand, {0: list(range(480, 1020, 30))})
        self.contractor = Contractor(0, (0, 0))
        self.schedule = Schedule([self.contractor], [self.customer])

    def test_errand(self):
        self.assertEqual(self.errand.id, 0)
        self.assertEqual(self.errand.type, "Grocery Shopping")
        self.assertEqual(self.errand.base_time, 60)
        self.assertAlmostEqual(self.errand.charge, 90, places=2)  # 60 * 1.5 = 90

    def test_customer(self):
        self.assertEqual(self.customer.id, 0)
        self.assertEqual(self.customer.location, (10, 10))
        self.assertEqual(self.customer.desired_errand, self.errand)
        self.assertIn(0, self.customer.availability)
        self.assertEqual(len(self.customer.availability[0]), 18)  # 18 30-minute slots from 8am to 5pm

    def test_contractor(self):
        self.assertEqual(self.contractor.id, 0)
        self.assertEqual(self.contractor.location, (0, 0))
        self.assertEqual(self.contractor.schedule, {})

    def test_schedule(self):
        self.assertEqual(len(self.schedule.contractors), 1)
        self.assertEqual(len(self.schedule.customers), 1)
        self.assertEqual(self.schedule.assignments, {})

    def test_schedule_assignment(self):
        self.schedule.assignments = {0: [(self.customer, self.contractor, 480)]}
        self.assertIn(0, self.schedule.assignments)
        self.assertEqual(len(self.schedule.assignments[0]), 1)
        customer, contractor, start_time = self.schedule.assignments[0][0]
        self.assertEqual(customer, self.customer)
        self.assertEqual(contractor, self.contractor)
        self.assertEqual(start_time, 480)

    def test_schedule_profit_calculation(self):
        self.schedule.assignments = {0: [(self.customer, self.contractor, 480)]}
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