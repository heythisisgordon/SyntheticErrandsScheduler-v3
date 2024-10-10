"""
Initial Greedy Scheduler for the Synthetic Errands Scheduler.
Implements a simple greedy initial scheduling algorithm as a baseline for performance comparison.
"""

import logging
from typing import List, Tuple, Optional, Set, Dict, Any
from tkinter import messagebox
from models.schedule import Schedule
from models.customer import Customer
from models.contractor import Contractor
from models.contractor_calendar import ContractorCalendar
from datetime import datetime, timedelta
from constants import SCHEDULING_DAYS, WORK_START_TIME_OBJ
from utils.scheduling_utils import calculate_total_time, is_valid_assignment, calculate_profit

logger: logging.Logger = logging.getLogger(__name__)

class InitialSchedulingError(Exception):
    """Custom exception for errors during initial scheduling."""
    pass

def initial_greedy_schedule(customers: List[Customer], contractors: List[Contractor], contractor_calendars: Dict[str, ContractorCalendar]) -> Schedule:
    """Create an initial schedule using a simple greedy algorithm."""
    scheduler = StepThroughGreedyScheduler(customers, contractors, contractor_calendars)
    while scheduler.step():
        pass
    return scheduler.schedule

class StepThroughGreedyScheduler:
    def __init__(self, customers: List[Customer], contractors: List[Contractor], contractor_calendars: Dict[str, ContractorCalendar]):
        self.customers = customers
        self.contractors = contractors
        self.contractor_calendars = contractor_calendars
        self.schedule = Schedule(contractors, customers)
        self.unscheduled_customers: Set[Customer] = set()
        self.current_date = datetime.now().replace(hour=WORK_START_TIME_OBJ.hour, minute=WORK_START_TIME_OBJ.minute, second=0, microsecond=0)
        self.current_day = 0
        self.current_customer_index = 0
        self.scheduled_customer_ids = set()

    def step(self) -> Optional[Dict[str, Any]]:
        if self.current_day >= SCHEDULING_DAYS:
            self.log_results()
            return None

        if self.current_customer_index == 0:
            self.reset_contractor_locations()

        if self.current_customer_index >= len(self.customers):
            self.current_day += 1
            self.current_customer_index = 0
            self.current_date += timedelta(days=1)
            return self.step()

        customer = self.customers[self.current_customer_index]
        self.current_customer_index += 1

        if customer.id not in self.scheduled_customer_ids:
            result = self.schedule_customer(customer)
            return {
                'step_name': 'Schedule Customer',
                'variables': {
                    'current_day': self.current_day,
                    'current_date': self.current_date,
                    'customer_id': customer.id,
                    'scheduled': result['scheduled'],
                    'contractor_id': result.get('contractor_id'),
                    'start_time': result.get('start_time'),
                    'end_time': result.get('end_time'),
                    'profit': result.get('profit')
                }
            }
        return self.step()

    def reset_contractor_locations(self) -> None:
        """Reset all contractors to their initial locations."""
        for contractor in self.contractors:
            contractor.reset_location()

    def schedule_customer(self, customer: Customer) -> Dict[str, Any]:
        """Attempt to schedule a single customer."""
        for _ in range(SCHEDULING_DAYS):
            valid_slot_info = self.find_earliest_valid_slot(customer)
            if valid_slot_info:
                selected_contractor, start_time, end_time = valid_slot_info
                if self.attempt_scheduling(customer, selected_contractor, start_time, end_time):
                    return {
                        'scheduled': True,
                        'contractor_id': selected_contractor.id,
                        'start_time': start_time,
                        'end_time': end_time,
                        'profit': calculate_profit(customer, selected_contractor, start_time, end_time - start_time)
                    }
            self.current_date += timedelta(days=1)

        logger.warning(f"Failed to schedule customer {customer.id} after {SCHEDULING_DAYS} attempts")
        self.unscheduled_customers.add(customer)
        return {'scheduled': False}

    def find_earliest_valid_slot(self, customer: Customer) -> Optional[Tuple[Contractor, datetime, datetime]]:
        """Find the earliest valid slot among all contractors for a given customer."""
        earliest_valid_slot = None
        selected_contractor = None
        for contractor in self.contractors:
            total_time = calculate_total_time(contractor, customer, customer.desired_errand)
            potential_slot = self.contractor_calendars[contractor.id].get_next_available_slot(self.current_date, total_time)
            if potential_slot:
                start_time = potential_slot['start']
                end_time = start_time + total_time
                if is_valid_assignment(contractor, customer, start_time, end_time):
                    if earliest_valid_slot is None or start_time < earliest_valid_slot['start']:
                        earliest_valid_slot = potential_slot
                        selected_contractor = contractor
        
        if selected_contractor and earliest_valid_slot:
            logger.debug(f"Earliest valid slot found for customer {customer.id}: Contractor {selected_contractor.id}, {earliest_valid_slot['start']} - {earliest_valid_slot['end']}")
        else:
            logger.debug(f"No valid slot found for customer {customer.id}")
        
        return (selected_contractor, earliest_valid_slot['start'], earliest_valid_slot['end']) if selected_contractor and earliest_valid_slot else None

    def attempt_scheduling(self, customer: Customer, contractor: Contractor, start_time: datetime, end_time: datetime) -> bool:
        """Attempt to schedule a customer with a contractor at a specific time."""
        total_time = calculate_total_time(contractor, customer, customer.desired_errand)
        actual_end_time = start_time + total_time
        
        logger.debug(f"Attempting to schedule customer {customer.id} with contractor {contractor.id} from {start_time} to {actual_end_time}")
        
        if is_valid_assignment(contractor, customer, start_time, actual_end_time):
            errand_id = f"errand_{customer.id}_{contractor.id}_{start_time.strftime('%Y%m%d%H%M')}"
            if self.contractor_calendars[contractor.id].reserve_time_slot(errand_id, start_time, actual_end_time):
                self.schedule.add_assignment(start_time, customer, contractor)
                profit = calculate_profit(customer, contractor, start_time, total_time)
                logger.info(f"Scheduled customer {customer.id} with contractor {contractor.id} at {start_time.time()}, profit: ${profit:.2f}")
                contractor.update_location(customer.location)
                self.scheduled_customer_ids.add(customer.id)
                return True
        else:
            logger.debug(f"Invalid slot for customer {customer.id} with contractor {contractor.id} from {start_time} to {actual_end_time}")
        return False

    def log_results(self) -> None:
        """Log the results of the scheduling process."""
        total_profit = self.schedule.calculate_total_profit()
        scheduled_count = len(self.customers) - len(self.unscheduled_customers)
        logger.info(f"Initial greedy scheduling completed. Total profit: ${total_profit:.2f}")
        logger.info(f"Scheduled customers: {scheduled_count}, Unscheduled: {len(self.unscheduled_customers)}")
        if self.unscheduled_customers:
            logger.warning(f"Failed to schedule {len(self.unscheduled_customers)} customers: {[c.id for c in self.unscheduled_customers]}")
