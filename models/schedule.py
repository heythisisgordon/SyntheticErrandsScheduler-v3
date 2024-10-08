"""
Schedule class for managing assignments of errands to contractors.
"""

from typing import List, Dict, Tuple
from datetime import datetime, timedelta
from models.contractor import Contractor
from models.customer import Customer
from models.errand import Errand
from utils.travel_time import calculate_travel_time
from utils.errand_utils import get_errand_time, calculate_errand_end_time

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
            if self.is_valid_assignment(customer, contractor, start_time)
        )

    def calculate_errand_profit(self, customer: Customer, contractor: Contractor, start_time: datetime, 
                                index: int, assignments: List[Tuple[Customer, Contractor, datetime]]) -> float:
        """Calculate the profit for a single errand assignment."""
        errand: Errand = customer.desired_errand
        
        # Calculate travel time from previous location or contractor's initial location
        prev_location = assignments[index-1][0].location if index > 0 else contractor.location
        travel_time, _ = calculate_travel_time(prev_location, customer.location)

        errand_duration: timedelta = get_errand_time(errand, contractor.location, customer.location)
        contractor_cost: float = (travel_time + errand_duration).total_seconds() / 60 * contractor.rate
        final_charge: float = errand.calculate_final_charge(start_time, datetime.now())

        return final_charge - contractor_cost

    def get_errand_end_time(self, customer: Customer, contractor: Contractor, start_time: datetime) -> datetime:
        """Calculate the end time of an errand."""
        errand_duration: timedelta = get_errand_time(customer.desired_errand, contractor.location, customer.location)
        return calculate_errand_end_time(start_time, errand_duration)

    def is_valid_assignment(self, customer: Customer, contractor: Contractor, start_time: datetime) -> bool:
        """Check if an assignment is valid based on contractor availability."""
        end_time = self.get_errand_end_time(customer, contractor, start_time)
        return contractor.calendar.is_available(start_time, end_time)

    def get_assignments_for_day(self, day: datetime) -> List[Tuple[Customer, Contractor, datetime]]:
        """Get all assignments for a specific day."""
        return self.assignments.get(day, [])

    def get_all_assignments(self) -> List[Tuple[Customer, Contractor, datetime]]:
        """Get all assignments across all days."""
        return [assignment for day_assignments in self.assignments.values() for assignment in day_assignments]

    def get_contractor_assignments(self, contractor: Contractor) -> List[Tuple[Customer, datetime]]:
        """Get all assignments for a specific contractor."""
        return [(customer, start_time) for assignments in self.assignments.values() 
                for customer, assigned_contractor, start_time in assignments 
                if assigned_contractor == contractor]

    def __str__(self) -> str:
        return f"Schedule with {len(self.contractors)} contractors and {len(self.customers)} customers"

    __repr__ = __str__