"""
Schedule class for managing assignments of errands to contractors.
"""

from typing import List, Dict, Tuple
from datetime import datetime, timedelta
from models.contractor import Contractor
from models.customer import Customer
from models.errand import Errand
from utils.scheduling_utils import SchedulingUtilities

class Schedule:
    def __init__(self, contractors: List[Contractor], customers: List[Customer]):
        self.contractors: List[Contractor] = contractors
        self.customers: List[Customer] = customers
        self.assignments: Dict[datetime, List[Tuple[Customer, Contractor, datetime]]] = {}

    def add_assignment(self, start_time: datetime, customer: Customer, contractor: Contractor) -> None:
        """Add a new assignment to the schedule."""
        if start_time not in self.assignments:
            self.assignments[start_time] = []
        self.assignments[start_time].append((customer, contractor, start_time))

    def calculate_total_profit(self) -> float:
        """Calculate the total profit for all valid assignments in the schedule."""
        return sum(
            self.calculate_errand_profit(customer, contractor, start_time, i, assignments)
            for day, assignments in self.assignments.items()
            for i, (customer, contractor, start_time) in enumerate(assignments)
            if SchedulingUtilities.is_valid_assignment(contractor, customer, start_time, self.get_errand_end_time(customer, contractor, start_time))
        )

    def calculate_errand_profit(self, customer: Customer, contractor: Contractor, start_time: datetime, 
                                index: int, assignments: List[Tuple[Customer, Contractor, datetime]]) -> float:
        """Calculate the profit for a single errand assignment."""
        errand: Errand = customer.desired_errand
        
        # Calculate travel time from previous location or contractor's initial location
        prev_location = assignments[index-1][0].location if index > 0 else contractor.location
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
