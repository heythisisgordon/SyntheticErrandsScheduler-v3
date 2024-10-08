"""
Initial Greedy Scheduler for the Synthetic Errands Scheduler.
Implements a simple greedy initial scheduling algorithm as a baseline for performance comparison.
"""

import logging
from typing import List, Tuple, Optional, Set
from models.schedule import Schedule
from models.customer import Customer
from models.contractor import Contractor
from models.master_contractor_calendar import MasterContractorCalendar
from datetime import datetime, timedelta
from constants import SCHEDULING_DAYS, WORK_START_TIME_OBJ
from utils.scheduling_utils import calculate_total_time, is_valid_assignment, calculate_assignment_profit

logger: logging.Logger = logging.getLogger(__name__)

class InitialSchedulingError(Exception):
    """Custom exception for errors during initial scheduling."""
    pass

def create_initial_schedule(customers: List[Customer], contractors: List[Contractor]) -> Schedule:
    """Create an initial schedule using a simple greedy algorithm."""
    if not customers or not contractors:
        raise InitialSchedulingError("No customers or contractors provided for scheduling.")

    schedule = Schedule(contractors, customers)
    master_calendar = create_master_calendar(contractors)
    unscheduled_customers: Set[Customer] = set()

    logger.info(f"Starting initial greedy scheduling for {len(customers)} customers and {len(contractors)} contractors...")

    today = datetime.now().replace(hour=WORK_START_TIME_OBJ.hour, minute=WORK_START_TIME_OBJ.minute, second=0, microsecond=0)
    for day in range(SCHEDULING_DAYS):
        current_date = today + timedelta(days=day)
        reset_contractor_locations(contractors)
        schedule_day(schedule, customers, contractors, master_calendar, current_date, unscheduled_customers)

    log_results(schedule, customers, unscheduled_customers)

    if not schedule.assignments:
        raise InitialSchedulingError("Failed to create any assignments in the initial greedy schedule.")

    return schedule

def create_master_calendar(contractors: List[Contractor]) -> MasterContractorCalendar:
    """Create and populate a master calendar with all contractors."""
    master_calendar = MasterContractorCalendar()
    for contractor in contractors:
        master_calendar.add_contractor(contractor)
    return master_calendar

def reset_contractor_locations(contractors: List[Contractor]) -> None:
    """Reset all contractors to their initial locations."""
    for contractor in contractors:
        contractor.reset_location()

def schedule_day(schedule: Schedule, customers: List[Customer], contractors: List[Contractor], 
                 master_calendar: MasterContractorCalendar, current_date: datetime, 
                 unscheduled_customers: Set[Customer]) -> None:
    """Schedule customers for a specific day."""
    scheduled_customer_ids = get_scheduled_customer_ids(schedule)
    for customer in customers:
        if customer.id not in scheduled_customer_ids:
            schedule_customer(schedule, customer, contractors, master_calendar, current_date, unscheduled_customers)

def get_scheduled_customer_ids(schedule: Schedule) -> Set[int]:
    """Get the set of customer IDs that have already been scheduled."""
    return {assignment[0].id for assignments in schedule.assignments.values() for assignment in assignments}

def schedule_customer(schedule: Schedule, customer: Customer, contractors: List[Contractor], 
                      master_calendar: MasterContractorCalendar, current_date: datetime, 
                      unscheduled_customers: Set[Customer]) -> None:
    """Attempt to schedule a single customer."""
    for _ in range(SCHEDULING_DAYS):
        slot_info = find_earliest_slot(customer, contractors, master_calendar, current_date)
        if slot_info:
            selected_contractor, start_time, end_time = slot_info
            if attempt_scheduling(schedule, customer, selected_contractor, master_calendar, start_time, end_time):
                return
        current_date += timedelta(days=1)

    logger.warning(f"Failed to schedule customer {customer.id} after {SCHEDULING_DAYS} attempts")
    unscheduled_customers.add(customer)

def find_earliest_slot(customer: Customer, contractors: List[Contractor], 
                       master_calendar: MasterContractorCalendar, 
                       current_date: datetime) -> Optional[Tuple[Contractor, datetime, datetime]]:
    """Find the earliest available slot among all contractors for a given customer."""
    earliest_slot = None
    selected_contractor = None
    for contractor in contractors:
        total_time = calculate_total_time(contractor, customer, customer.desired_errand)
        slot = master_calendar.get_contractor_next_available_slot(contractor.id, current_date, total_time)
        if slot and (earliest_slot is None or slot['start'] < earliest_slot['start']):
            earliest_slot = slot
            selected_contractor = contractor
    
    return (selected_contractor, earliest_slot['start'], earliest_slot['end']) if selected_contractor and earliest_slot else None

def attempt_scheduling(schedule: Schedule, customer: Customer, contractor: Contractor, 
                       master_calendar: MasterContractorCalendar, start_time: datetime, 
                       end_time: datetime) -> bool:
    """Attempt to schedule a customer with a contractor at a specific time."""
    if is_valid_assignment(contractor, customer, start_time, end_time):
        errand_id = f"errand_{customer.id}_{contractor.id}_{start_time.strftime('%Y%m%d%H%M')}"
        if master_calendar.reserve_time_slot(contractor.id, errand_id, start_time, end_time):
            schedule.add_assignment(start_time, customer, contractor)
            profit = calculate_assignment_profit(customer, contractor, start_time, end_time)
            logger.info(f"Scheduled customer {customer.id} with contractor {contractor.id} at {start_time.time()}, profit: ${profit:.2f}")
            contractor.update_location(customer.location)
            return True
    return False

def log_results(schedule: Schedule, customers: List[Customer], unscheduled_customers: Set[Customer]) -> None:
    """Log the results of the scheduling process."""
    total_profit = schedule.calculate_total_profit()
    scheduled_count = len(customers) - len(unscheduled_customers)
    logger.info(f"Initial greedy scheduling completed. Total profit: ${total_profit:.2f}")
    logger.info(f"Scheduled customers: {scheduled_count}, Unscheduled: {len(unscheduled_customers)}")
    if unscheduled_customers:
        logger.warning(f"Failed to schedule {len(unscheduled_customers)} customers: {[c.id for c in unscheduled_customers]}")