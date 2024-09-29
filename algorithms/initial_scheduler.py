"""
Initial Greedy Scheduler for the Synthetic Errands Scheduler

This module implements a greedy initial scheduling algorithm. It schedules errands in the order they are received
and assigns them to the first available time slot. This serves as a starting point for the optimizer and as a
baseline for performance comparison.

Note: This algorithm should not be changed to optimize the initial solution, as it's meant to be a simple
greedy approach.
"""

import logging
from typing import List, Tuple, Dict, Optional
from models.schedule import Schedule
from models.customer import Customer
from models.contractor import Contractor
from utils.errand_utils import get_errand_time, calculate_errand_end_time
from utils.travel_time import calculate_travel_time
from datetime import datetime, timedelta, time
from constants import SCHEDULING_DAYS, WORK_START_TIME, WORK_END_TIME

logger: logging.Logger = logging.getLogger(__name__)

class InitialSchedulingError(Exception):
    """Custom exception for errors during initial scheduling."""
    pass

# Type aliases for improved readability
Assignment = Tuple[Customer, Contractor, datetime]
DailyAssignments = List[Assignment]
ScheduleAssignments = Dict[datetime, DailyAssignments]

# Convert WORK_START_TIME and WORK_END_TIME to datetime.time objects
WORK_START_TIME_OBJ = time(hour=WORK_START_TIME // 60, minute=WORK_START_TIME % 60)
WORK_END_TIME_OBJ = time(hour=WORK_END_TIME // 60, minute=WORK_END_TIME % 60)

def initial_schedule(customers: List[Customer], contractors: List[Contractor]) -> Schedule:
    """
    Create an initial schedule using a greedy algorithm.

    Args:
        customers (List[Customer]): List of Customer objects.
        contractors (List[Contractor]): List of Contractor objects.

    Returns:
        Schedule: The initial schedule.

    Raises:
        InitialSchedulingError: If there's an error during the initial scheduling process.
    """
    try:
        if not customers or not contractors:
            raise InitialSchedulingError("No customers or contractors provided for scheduling.")

        schedule = Schedule(contractors, customers)
        today = datetime.now().date()

        logger.info("Starting initial scheduling process...")

        for day in range(SCHEDULING_DAYS):
            current_date = today + timedelta(days=day)
            logger.info(f"Scheduling for day {day} ({current_date}):")
            
            # Reset contractor availability at the start of each day
            for contractor in contractors:
                contractor.available_time = datetime.combine(current_date, WORK_START_TIME_OBJ)
                contractor.current_location = contractor.location

            for customer in customers:
                logger.debug(f"Attempting to schedule customer {customer.id} for errand type {customer.desired_errand.type}")
                if customer.id not in [assignment[0].id for assignments in schedule.assignments.values() for assignment in assignments]:
                    # Find the first available contractor and time slot
                    assigned_contractor: Optional[Contractor] = None
                    start_time: Optional[datetime] = None

                    for contractor in contractors:
                        travel_time, _ = calculate_travel_time(contractor.current_location, customer.location)
                        errand_time = get_errand_time(customer.desired_errand, contractor.current_location, customer.location)
                        total_time = travel_time + errand_time

                        potential_start_time = contractor.available_time + travel_time
                        potential_end_time = potential_start_time + errand_time

                        if potential_end_time.time() <= WORK_END_TIME_OBJ:
                            assigned_contractor = contractor
                            start_time = potential_start_time
                            break

                    if assigned_contractor and start_time is not None:
                        schedule.assignments.setdefault(current_date, []).append((customer, assigned_contractor, start_time))
                        
                        # Calculate and log profit
                        contractor_cost = total_time.total_seconds() / 60 * Schedule.contractor_cost_per_minute
                        errand_charge = customer.desired_errand.calculate_final_charge(start_time, datetime.now())
                        profit = errand_charge - contractor_cost
                        
                        logger.info(f"Scheduled customer {customer.id} with contractor {assigned_contractor.id} at start time {start_time.time()}")
                        logger.debug(f"Travel time: {travel_time}")
                        logger.debug(f"Errand time: {errand_time}")
                        logger.debug(f"Errand charge: ${errand_charge:.2f}")
                        logger.debug(f"Contractor cost: ${contractor_cost:.2f}")
                        logger.debug(f"Profit: ${profit:.2f}")
                        
                        assigned_contractor.available_time = calculate_errand_end_time(start_time, errand_time)
                        assigned_contractor.current_location = customer.location
                        logger.debug(f"Contractor {assigned_contractor.id} new available time: {assigned_contractor.available_time.time()}")
                    else:
                        logger.warning(f"Could not schedule customer {customer.id} on day {day}")

        logger.info("Initial scheduling process completed.")
        total_profit = schedule.calculate_total_profit()
        logger.info(f"Total profit for initial schedule: ${total_profit:.2f}")

        if not schedule.assignments:
            raise InitialSchedulingError("Failed to create any assignments in the initial schedule.")

        return schedule

    except Exception as e:
        logger.error(f"Error during initial scheduling: {str(e)}")
        raise InitialSchedulingError(f"Failed to create initial schedule: {str(e)}")