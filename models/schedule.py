"""
Schedule class for managing assignments of errands to contractors.
"""

from typing import List, Dict, Tuple
import pandas as pd
from models.contractor import Contractor
from models.customer import Customer
from models.contractor_calendar import ContractorCalendar, ErrandAssignment
from utils.scheduling_utils import SchedulingUtilities
from utils.travel_time import calculate_travel_time
from constants import WORK_START_TIME_OBJ

class Schedule:
    def __init__(self, contractors: List[Contractor], customers: List[Customer]):
        self.contractors: List[Contractor] = contractors
        self.customers: List[Customer] = customers
        self.contractor_calendars: Dict[int, ContractorCalendar] = {
            contractor.id: ContractorCalendar(contractor.schedule) for contractor in contractors
        }
        self.assignments: Dict[str, ErrandAssignment] = {}

    def add_assignment(self, start_time: pd.Timestamp, customer: Customer, contractor: Contractor) -> bool:
        calendar = self.contractor_calendars[contractor.id]
        errand_id = f"errand_{customer.id}_{contractor.id}_{start_time.strftime('%Y%m%d%H%M')}"
        travel_duration, _ = calculate_travel_time(contractor.location, customer.location)
        task_duration = customer.desired_errand.base_time
        total_duration = travel_duration + task_duration

        travel_start_time = start_time
        travel_end_time = start_time + travel_duration
        task_start_time = travel_end_time
        task_end_time = task_start_time + task_duration

        if calendar.reserve_time_slot(errand_id, customer.desired_errand.type, travel_start_time, travel_end_time, 
                                      task_start_time, task_end_time):
            contractor.update_location(customer.location)
            self.assignments[errand_id] = ErrandAssignment(
                errand_id=errand_id,
                errand_type=customer.desired_errand.type,
                travel_start_time=travel_start_time,
                travel_end_time=travel_end_time,
                task_start_time=task_start_time,
                task_end_time=task_end_time,
                travel_duration=travel_duration,
                total_duration=total_duration
            )
            return True
        return False

    def get_assignments(self) -> List[Tuple[ErrandAssignment, Customer, Contractor]]:
        assignments = []
        for errand_id, errand in self.assignments.items():
            customer_id = int(errand_id.split('_')[1])
            contractor_id = int(errand_id.split('_')[2])
            customer = next(c for c in self.customers if c.id == customer_id)
            contractor = next(c for c in self.contractors if c.id == contractor_id)
            assignments.append((errand, customer, contractor))
        
        return sorted(assignments, key=lambda x: x[0].travel_start_time)

    def calculate_total_profit(self) -> float:
        total_profit = 0
        for errand, customer, contractor in self.get_assignments():
            if SchedulingUtilities.is_valid_assignment(contractor, customer, errand.travel_start_time, errand.task_end_time):
                total_profit += SchedulingUtilities.calculate_profit(customer, contractor, errand.travel_start_time, errand.task_end_time)
        return total_profit

    def get_errand_end_time(self, customer: Customer, contractor: Contractor, start_time: pd.Timestamp) -> pd.Timestamp:
        travel_duration, _ = calculate_travel_time(contractor.location, customer.location)
        total_time = travel_duration + customer.desired_errand.base_time
        return start_time + total_time

    def __str__(self) -> str:
        return f"Schedule with {len(self.contractors)} contractors and {len(self.customers)} customers"

    __repr__ = __str__
