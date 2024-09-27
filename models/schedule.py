from utils.travel_time import calculate_travel_time
from utils.errand_utils import calculate_errand_time
from datetime import datetime, timedelta

class Schedule:
    contractor_cost_per_minute = 0.5  # $0.5 per minute of contractor time

    def __init__(self, contractors, customers):
        self.contractors = contractors
        self.customers = customers
        self.assignments = {}  # dictionary of day: list of (customer, contractor, start_time) tuples
    
    def calculate_total_profit(self):
        total_profit = 0
        today = datetime.now().date()

        for day, assignments in self.assignments.items():
            current_date = today + timedelta(days=day)
            for i, (customer, contractor, start_time) in enumerate(assignments):
                errand_profit = self.calculate_errand_profit(customer, contractor, start_time, current_date, i, assignments)
                total_profit += errand_profit

        return total_profit

    def calculate_errand_profit(self, customer, contractor, start_time, current_date, index, assignments):
        errand = customer.desired_errand
        
        # Calculate travel time
        if index == 0:
            travel_time, _ = calculate_travel_time(contractor.location, customer.location)
        else:
            prev_customer = assignments[index-1][0]
            travel_time, _ = calculate_travel_time(prev_customer.location, customer.location)

        # Calculate total errand time
        errand_time = calculate_errand_time(errand, contractor.location, customer.location)

        # Calculate contractor cost
        contractor_cost = (travel_time + errand_time) * self.contractor_cost_per_minute

        # Calculate errand charge with incentives and disincentives
        base_charge = errand.calculate_base_charge()
        final_charge = errand.calculate_final_charge(current_date, datetime.now())

        # Calculate profit
        profit = final_charge - contractor_cost

        return profit

    def __str__(self):
        return f"Schedule with {len(self.contractors)} contractors and {len(self.customers)} customers"

    def __repr__(self):
        return self.__str__()