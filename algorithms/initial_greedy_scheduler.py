"""
Initial Greedy Scheduler for the Synthetic Errands Scheduler.
Implements a simple greedy initial scheduling algorithm as a baseline for performance comparison.
"""

import logging
from typing import List, Tuple, Optional, Dict, Set
from models.schedule import Schedule
from models.customer import Customer
from models.contractor import Contractor
from models.contractor_calendar import ContractorCalendar
from datetime import datetime, timedelta
from constants import SCHEDULING_DAYS, WORK_START_TIME_OBJ
from utils.scheduling_utils import SchedulingUtilities

logger: logging.Logger = logging.getLogger(__name__)

class InitialSchedulingError(Exception):
    """Custom exception for errors during initial scheduling."""
    pass

def initial_greedy_schedule(customers: List[Customer], contractors: List[Contractor]) -> Schedule:
    """Create an initial schedule using a simple greedy algorithm."""
    scheduler = GreedyScheduler(customers, contractors)
    return scheduler.generate_schedule()

class GreedyScheduler:
    def __init__(self, customers: List[Customer], contractors: List[Contractor]):
        self.customers = customers
        self.contractors = contractors
        self.contractor_calendars = {contractor.id: contractor.calendar for contractor in contractors}
        self.schedule = Schedule(contractors, customers)
        self.unscheduled_customers: Set[Customer] = set(customers)
        self.current_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    def generate_schedule(self) -> Schedule:
        """Generate the complete schedule."""
        for day in range(SCHEDULING_DAYS):
            self.reset_contractor_locations()
            self.schedule_day(day)
            self.current_date += timedelta(days=1)
        
        self.schedule.assignments.sort(key=lambda x: x[0])  # Sort assignments by start time
        self.log_results()
        return self.schedule

    def reset_contractor_locations(self) -> None:
        """Reset all contractors to their initial locations."""
        for contractor in self.contractors:
            contractor.reset_location()

    def schedule_day(self, day: int) -> None:
        """Schedule all customers for a single day."""
        for customer in list(self.unscheduled_customers):  # Create a copy of the set to iterate over
            self.schedule_customer(customer)

    def schedule_customer(self, customer: Customer) -> None:
        """Attempt to schedule a single customer."""
        valid_slot_info = self.find_earliest_valid_slot(customer)
        if valid_slot_info:
            selected_contractor, start_time, end_time = valid_slot_info
            if self.attempt_scheduling(customer, selected_contractor, start_time, end_time):
                self.unscheduled_customers.remove(customer)
                return

    def find_earliest_valid_slot(self, customer: Customer) -> Optional[Tuple[Contractor, datetime, datetime]]:
        """Find the earliest valid slot among all contractors for a given customer."""
        earliest_valid_slot = None
        selected_contractor = None
        for contractor in self.contractors:
            total_time = SchedulingUtilities.calculate_total_time(contractor, customer, customer.desired_errand)
            potential_slot = self.contractor_calendars[contractor.id].get_next_available_slot(self.current_date, total_time)
            if potential_slot:
                start_time = potential_slot['start']
                end_time = start_time + total_time
                if SchedulingUtilities.is_valid_assignment(contractor, customer, start_time, end_time):
                    if earliest_valid_slot is None or start_time < earliest_valid_slot['start']:
                        earliest_valid_slot = potential_slot
                        selected_contractor = contractor
        
        return (selected_contractor, earliest_valid_slot['start'], earliest_valid_slot['end']) if selected_contractor and earliest_valid_slot else None

    def attempt_scheduling(self, customer: Customer, contractor: Contractor, start_time: datetime, end_time: datetime) -> bool:
        """Attempt to schedule a customer with a contractor at a specific time."""
        total_time = SchedulingUtilities.calculate_total_time(contractor, customer, customer.desired_errand)
        actual_end_time = start_time + total_time
        
        if SchedulingUtilities.is_valid_assignment(contractor, customer, start_time, actual_end_time):
            errand_id = f"errand_{customer.id}_{contractor.id}_{start_time.strftime('%Y%m%d%H%M')}"
            if self.contractor_calendars[contractor.id].reserve_time_slot(errand_id, start_time, actual_end_time):
                self.schedule.add_assignment(start_time, customer, contractor)
                contractor.update_location(customer.location)
                return True
        return False

    def log_results(self) -> None:
        """Log the results of the scheduling process."""
        total_profit = self.schedule.calculate_total_profit()
        scheduled_count = len(self.customers) - len(self.unscheduled_customers)
        logger.info(f"Initial greedy scheduling completed. Total profit: ${total_profit:.2f}")
        logger.info(f"Scheduled customers: {scheduled_count}, Unscheduled: {len(self.unscheduled_customers)}")
        if self.unscheduled_customers:
            logger.warning(f"Failed to schedule {len(self.unscheduled_customers)} customers")
