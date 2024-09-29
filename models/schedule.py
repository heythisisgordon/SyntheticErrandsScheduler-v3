from typing import List, Dict, Tuple, Any
from utils.travel_time import calculate_travel_time
from utils.errand_utils import get_errand_time, calculate_errand_end_time
from datetime import datetime, timedelta
from models.contractor import Contractor
from models.customer import Customer
from models.errand import Errand

class Schedule:
    contractor_cost_per_minute: float = 0.5  # $0.5 per minute of contractor time

    def __init__(self, contractors: List[Contractor], customers: List[Customer]):
        self.contractors: List[Contractor] = contractors
        self.customers: List[Customer] = customers
        self.assignments: Dict[datetime, List[Tuple[Customer, Contractor, datetime]]] = {}  # dictionary of day: list of (customer, contractor, start_time) tuples
    
    def calculate_total_profit(self) -> float:
        total_profit: float = 0

        for day, assignments in self.assignments.items():
            for i, (customer, contractor, start_time) in enumerate(assignments):
                errand_profit: float = self.calculate_errand_profit(customer, contractor, start_time, day, i, assignments)
                total_profit += errand_profit

        return total_profit

    def calculate_errand_profit(self, customer: Customer, contractor: Contractor, start_time: datetime, current_date: datetime, index: int, assignments: List[Tuple[Customer, Contractor, datetime]]) -> float:
        errand: Errand = customer.desired_errand
        
        # Calculate travel time
        if index == 0:
            travel_time, _ = calculate_travel_time(contractor.location, customer.location)
        else:
            prev_customer: Customer = assignments[index-1][0]
            travel_time, _ = calculate_travel_time(prev_customer.location, customer.location)

        # Calculate total errand time
        errand_duration: timedelta = get_errand_time(errand, contractor.location, customer.location)

        # Calculate contractor cost
        contractor_cost: float = (travel_time + errand_duration).total_seconds() / 60 * self.contractor_cost_per_minute

        # Calculate errand charge with incentives and disincentives
        final_charge: float = errand.calculate_final_charge(current_date, datetime.now())

        # Calculate profit
        profit: float = final_charge - contractor_cost

        return profit

    def get_errand_end_time(self, customer: Customer, contractor: Contractor, start_time: datetime) -> datetime:
        errand: Errand = customer.desired_errand
        errand_duration: timedelta = get_errand_time(errand, contractor.location, customer.location)
        return calculate_errand_end_time(start_time, errand_duration)

    def __str__(self) -> str:
        return f"Schedule with {len(self.contractors)} contractors and {len(self.customers)} customers"

    def __repr__(self) -> str:
        return self.__str__()