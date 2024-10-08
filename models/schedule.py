from typing import List, Dict, Tuple, Any
from utils.travel_time import calculate_travel_time
from utils.errand_utils import get_errand_time, calculate_errand_end_time
from datetime import datetime, timedelta
from models.contractor import Contractor
from models.customer import Customer
from models.errand import Errand

class Schedule:
    def __init__(self, contractors: List[Contractor], customers: List[Customer]):
        self.contractors: List[Contractor] = contractors
        self.customers: List[Customer] = customers
        self.assignments: Dict[datetime, List[Tuple[Customer, Contractor, datetime]]] = {}

    def calculate_total_profit(self) -> float:
        total_profit: float = 0

        for day, assignments in self.assignments.items():
            for i, (customer, contractor, start_time) in enumerate(assignments):
                if self.is_valid_assignment(customer, contractor, start_time):
                    errand_profit: float = self.calculate_errand_profit(customer, contractor, start_time, i, assignments)
                    total_profit += errand_profit

        return total_profit

    def calculate_errand_profit(self, customer: Customer, contractor: Contractor, start_time: datetime, index: int, assignments: List[Tuple[Customer, Contractor, datetime]]) -> float:
        errand: Errand = customer.desired_errand
        
        # Calculate travel time
        if index == 0:
            travel_time, _ = calculate_travel_time(contractor.location, customer.location)
        else:
            prev_customer: Customer = assignments[index-1][0]
            travel_time, _ = calculate_travel_time(prev_customer.location, customer.location)

        # Calculate total errand time
        errand_duration: timedelta = get_errand_time(errand, contractor.location, customer.location)

        # Calculate contractor cost using the contractor's individual rate
        contractor_cost: float = (travel_time + errand_duration).total_seconds() / 60 * contractor.rate

        # Calculate errand charge with incentives and disincentives
        final_charge: float = errand.calculate_final_charge(start_time, datetime.now())

        # Calculate profit
        profit: float = final_charge - contractor_cost

        return profit

    def get_errand_end_time(self, customer: Customer, contractor: Contractor, start_time: datetime) -> datetime:
        errand: Errand = customer.desired_errand
        errand_duration: timedelta = get_errand_time(errand, contractor.location, customer.location)
        return calculate_errand_end_time(start_time, errand_duration)

    def is_valid_assignment(self, customer: Customer, contractor: Contractor, start_time: datetime) -> bool:
        end_time = self.get_errand_end_time(customer, contractor, start_time)
        return contractor.calendar.is_available(start_time, end_time)

    def add_assignment(self, start_time: datetime, customer: Customer, contractor: Contractor) -> None:
        if start_time not in self.assignments:
            self.assignments[start_time] = []
        self.assignments[start_time].append((customer, contractor, start_time))

    def __str__(self) -> str:
        return f"Schedule with {len(self.contractors)} contractors and {len(self.customers)} customers"

    def __repr__(self) -> str:
        return self.__str__()