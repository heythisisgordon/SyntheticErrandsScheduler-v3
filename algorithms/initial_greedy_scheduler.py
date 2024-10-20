"""
Initial Greedy Scheduler for the Synthetic Errands Scheduler.
Implements a simple greedy initial scheduling algorithm as a baseline for performance comparison.
"""

import logging
from typing import List, Tuple, Optional
from models.schedule import Schedule
from models.customer import Customer
from models.contractor import Contractor
from utils.scheduling_utils import SchedulingUtilities
from utils.travel_time import calculate_travel_time
import pandas as pd

logger: logging.Logger = logging.getLogger(__name__)

def initial_greedy_schedule(customers: List[Customer], contractors: List[Contractor]) -> Schedule:
    """Create an initial schedule using a simple greedy algorithm."""
    scheduler = GreedyScheduler(customers, contractors)
    return scheduler._generate_schedule()

class GreedyScheduler:
    def __init__(self, customers: List[Customer], contractors: List[Contractor]):
        self.customers = customers
        self.contractors = contractors
        self.schedule = Schedule(contractors, customers)
        self.unscheduled_customers: List[Customer] = list(customers)
        self.current_date = pd.Timestamp.now().floor('D')
        logger.info(f"GreedyScheduler initialized with current_date: {self.current_date}")

    def _generate_schedule(self) -> Schedule:
        """Generate the complete schedule."""
        start_date = pd.Timestamp.now().floor('D')
        
        while self.unscheduled_customers:
            scheduled_any = False
            for customer in self.unscheduled_customers[:]:
                if self._schedule_customer(customer, start_date):
                    scheduled_any = True
            
            if not scheduled_any:
                break  # Exit if no customers could be scheduled
        
        self._log_results()
        return self.schedule

    def _schedule_customer(self, customer: Customer, start_date: pd.Timestamp) -> bool:
        """Attempt to schedule a single customer across all available days."""
        valid_slot_info = self._find_earliest_valid_slot(customer, start_date)
        if valid_slot_info:
            selected_contractor, travel_start_time, task_end_time = valid_slot_info
            if self._attempt_scheduling(customer, selected_contractor, travel_start_time, task_end_time):
                self.unscheduled_customers.remove(customer)
                logger.info(f"Scheduled customer {customer.id} from {travel_start_time} to {task_end_time}")
                return True
        logger.warning(f"Failed to schedule customer {customer.id}")
        return False

    def _find_earliest_valid_slot(self, customer: Customer, start_date: pd.Timestamp) -> Optional[Tuple[Contractor, pd.Timestamp, pd.Timestamp]]:
        """Find the earliest valid slot among all contractors for a given customer."""
        earliest_valid_slot = None
        selected_contractor = None
        earliest_task_end_time = None

        for contractor in self.contractors:
            travel_duration, _ = calculate_travel_time(contractor.location, customer.location)
            total_duration = travel_duration + customer.desired_errand.base_time

            current_datetime = max(start_date, contractor.schedule.index.get_level_values('Date').min())
            logger.debug(f"Searching for slot from {current_datetime} for customer {customer.id}")

            next_available_time = SchedulingUtilities.calculate_next_available_time(contractor, customer, current_datetime)
            
            if next_available_time:
                travel_start_time = next_available_time
                task_end_time = travel_start_time + total_duration
# CHECK THIS LOGIC ****************************************************************************
                if earliest_valid_slot is None or travel_start_time < earliest_valid_slot:
                    earliest_valid_slot = travel_start_time
                    earliest_task_end_time = task_end_time
                    selected_contractor = contractor
                logger.debug(f"Found valid slot for customer {customer.id} with contractor {contractor.id}: {travel_start_time} to {task_end_time}")

        if earliest_valid_slot:
            logger.debug(f"Selected earliest slot for customer {customer.id}: {earliest_valid_slot} to {earliest_task_end_time} with contractor {selected_contractor.id}")
            return selected_contractor, earliest_valid_slot, earliest_task_end_time

        logger.warning(f"No valid slot found for customer {customer.id}")
        return None

    def _attempt_scheduling(self, customer: Customer, contractor: Contractor, travel_start_time: pd.Timestamp, task_end_time: pd.Timestamp) -> bool:
        """Attempt to schedule a customer with a contractor at a specific time."""
        if SchedulingUtilities.is_valid_assignment(contractor, customer, travel_start_time, task_end_time):
            if self.schedule.add_assignment(travel_start_time, customer, contractor):
                contractor.update_location(customer.location)
                return True
        return False

    def _log_results(self) -> None:
        """Log the results of the scheduling process."""
        total_profit = self.schedule.calculate_total_profit()
        scheduled_count = len(self.customers) - len(self.unscheduled_customers)
        logger.info(f"Initial greedy scheduling completed. Total profit: ${total_profit:.2f}")
        logger.info(f"Scheduled customers: {scheduled_count}, Unscheduled: {len(self.unscheduled_customers)}")
        if self.unscheduled_customers:
            logger.warning(f"Failed to schedule {len(self.unscheduled_customers)} customers")
