"""
Schedule class for managing assignments of errands to contractors.
"""

from typing import List, Tuple
from datetime import datetime, timedelta
from models.contractor import Contractor
from models.customer import Customer
from models.errand import Errand
from utils.scheduling_utils import SchedulingUtilities

class Schedule:
    def __init__(self, contractors: List[Contractor], customers: List[Customer]):
        self.contractors: List[Contractor] = contractors
        self.customers: List[Customer] = customers
        self.assignments: List[Tuple[datetime, Customer, Contractor]] = []

    def add_assignment(self, start_time: datetime, customer: Customer, contractor: Contractor) -> None:
        """Add a new assignment to the schedule."""
        self.assignments.append((start_time, customer, contractor))

    def calculate_total_profit(self) -> float:
        """Calculate the total profit for all valid assignments in the schedule."""
        return sum(
            self.calculate_errand_profit(customer, contractor, start_time, i)
            for i, (start_time, customer, contractor) in enumerate(self.assignments)
            if SchedulingUtilities.is_valid_assignment(contractor, customer, start_time, self.get_errand_end_time(customer, contractor, start_time))
        )

    def calculate_errand_profit(self, customer: Customer, contractor: Contractor, start_time: datetime, index: int) -> float:
        """Calculate the profit for a single errand assignment."""
        errand: Errand = customer.desired_errand
        
        prev_location = self.assignments[index-1][1].location if index > 0 else contractor.location
        total_time = SchedulingUtilities.calculate_total_time(contractor, customer, errand)
        
        contractor_cost: float = total_time.total_seconds() / 60 * contractor.rate
        final_charge: float = errand.calculate_final_charge(start_time, datetime.now())

        return final_charge - contractor_cost

    def get_errand_end_time(self, customer: Customer, contractor: Contractor, start_time: datetime) -> datetime:
        """Calculate the end time of an errand."""
        total_time = SchedulingUtilities.calculate_total_time(contractor, customer, customer.desired_errand)
        return start_time + total_time

    def __str__(self) -> str:
        return f"Schedule with {len(self.contractors)} contractors and {len(self.customers)} customers"

    __repr__ = __str__
