"""
Initial Greedy Scheduler for the Synthetic Errands Scheduler

This module implements a simple greedy initial scheduling algorithm.
It serves as a starting point for the optimizer and as a baseline for performance comparison.

IMPORTANT: This file should not be modified to include any optimization techniques.
It must remain a simple greedy algorithm for baseline comparison.
"""

import logging
from typing import List, Tuple, Dict
from models.schedule import Schedule
from models.customer import Customer
from models.contractor import Contractor
from models.master_contractor_calendar import MasterContractorCalendar
from datetime import datetime, timedelta
from constants import SCHEDULING_DAYS, WORK_START_TIME_OBJ, WORK_END_TIME_OBJ
from utils.scheduling_utils import (
    calculate_total_time,
    is_valid_assignment,
    calculate_assignment_profit
)

logger: logging.Logger = logging.getLogger(__name__)

class InitialSchedulingError(Exception):
    """Custom exception for errors during initial scheduling."""
    pass

# Type aliases for improved readability
Assignment = Tuple[Customer, Contractor, datetime]
DailyAssignments = List[Assignment]
ScheduleAssignments = Dict[datetime, DailyAssignments]

def initial_greedy_schedule(customers: List[Customer], contractors: List[Contractor]) -> Schedule:
    """Create an initial schedule using a simple greedy algorithm."""
    try:
        if not customers or not contractors:
            raise InitialSchedulingError("No customers or contractors provided for scheduling.")

        schedule = Schedule(contractors, customers)
        today = datetime.now().replace(hour=WORK_START_TIME_OBJ.hour, minute=WORK_START_TIME_OBJ.minute, second=0, microsecond=0)

        logger.info("Starting initial greedy scheduling process...")
        logger.info(f"Number of customers: {len(customers)}")
        logger.info(f"Number of contractors: {len(contractors)}")

        master_calendar = MasterContractorCalendar()
        for contractor in contractors:
            master_calendar.add_contractor(contractor)
            logger.debug(f"Added contractor {contractor.id} to master calendar")

        unscheduled_customers = []

        for day in range(SCHEDULING_DAYS):
            current_date = today + timedelta(days=day)
            logger.info(f"Scheduling for day {day} ({current_date}):")
            
            for contractor in contractors:
                contractor.location = contractor.initial_location
                logger.debug(f"Contractor {contractor.id} initial location: {contractor.location}")

            for customer in customers:
                logger.info(f"Attempting to schedule customer {customer.id} for errand type {customer.desired_errand.type}")
                if customer.id not in [assignment[0].id for assignments in schedule.assignments.values() for assignment in assignments]:
                    scheduled = False
                    attempts = 0
                    while not scheduled and attempts < SCHEDULING_DAYS:
                        earliest_slot = None
                        selected_contractor = None

                        for contractor in contractors:
                            total_time = calculate_total_time(contractor, customer, customer.desired_errand)
                            logger.debug(f"Total time for errand with contractor {contractor.id}: {total_time}")
                            slot = master_calendar.get_contractor_next_available_slot(contractor.id, current_date, total_time)
                            
                            if slot:
                                logger.debug(f"Available slot found for contractor {contractor.id}: Start time: {slot['start']}, End time: {slot['end']}")
                                if earliest_slot is None or slot['start'] < earliest_slot['start']:
                                    earliest_slot = slot
                                    selected_contractor = contractor
                            else:
                                logger.debug(f"No available slot found for contractor {contractor.id}")
                            
                            # Log the next available window start time for the contractor
                            next_available = contractor.calendar.get_next_available_slot(current_date, timedelta(minutes=1))
                            if next_available:
                                logger.debug(f"Contractor {contractor.id} next available window starts at: {next_available['start']}")
                            else:
                                logger.debug(f"Contractor {contractor.id} has no available windows in the future")

                        if selected_contractor is None or earliest_slot is None:
                            logger.warning(f"No available time slot for any contractor on {current_date}")
                            current_date += timedelta(days=1)
                            attempts += 1
                            continue

                        potential_start_time = earliest_slot['start']
                        potential_end_time = earliest_slot['end']

                        logger.debug(f"Potential start time: {potential_start_time}, Potential end time: {potential_end_time}")

                        if is_valid_assignment(selected_contractor, customer, potential_start_time, potential_end_time):
                            logger.debug(f"Valid assignment found for customer {customer.id} with contractor {selected_contractor.id}")
                            errand_id = f"errand_{customer.id}_{selected_contractor.id}_{potential_start_time.strftime('%Y%m%d%H%M')}"
                            if master_calendar.reserve_time_slot(selected_contractor.id, errand_id, potential_start_time, potential_end_time):
                                schedule.add_assignment(potential_start_time, customer, selected_contractor)
                                profit = calculate_assignment_profit(customer, selected_contractor, potential_start_time, potential_end_time)
                                logger.info(f"Scheduled customer {customer.id} with contractor {selected_contractor.id} (rate: ${selected_contractor.rate:.2f}/min) at start time {potential_start_time.time()}, profit: ${profit:.2f}")
                                selected_contractor.location = customer.location
                                scheduled = True
                            else:
                                logger.warning(f"Failed to reserve time slot for contractor {selected_contractor.id} on {current_date}")
                        else:
                            logger.warning(f"Invalid assignment for contractor {selected_contractor.id} on {current_date}")

                        if not scheduled:
                            current_date += timedelta(days=1)
                            attempts += 1
                            logger.debug(f"Attempt {attempts} for customer {customer.id}, moving to date {current_date}")
                            if current_date > today + timedelta(days=SCHEDULING_DAYS - 1):
                                logger.warning(f"Could not schedule customer {customer.id} within the scheduling period")
                                break

                    if not scheduled:
                        logger.warning(f"Failed to schedule customer {customer.id} after {attempts} attempts")
                        unscheduled_customers.append(customer)

        logger.info("Initial greedy scheduling process completed.")
        total_profit = schedule.calculate_total_profit()
        logger.info(f"Total profit for initial greedy schedule: ${total_profit:.2f}")
        logger.info(f"Total scheduled customers: {len(customers) - len(unscheduled_customers)}")
        logger.info(f"Total unscheduled customers: {len(unscheduled_customers)}")

        if not schedule.assignments:
            raise InitialSchedulingError("Failed to create any assignments in the initial greedy schedule.")

        if unscheduled_customers:
            logger.warning(f"Failed to schedule {len(unscheduled_customers)} customers: {[c.id for c in unscheduled_customers]}")

        return schedule

    except Exception as e:
        logger.error(f"Error during initial greedy scheduling: {str(e)}")
        raise InitialSchedulingError(f"Failed to create initial greedy schedule: {str(e)}")