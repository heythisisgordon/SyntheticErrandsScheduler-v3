"""
Scheduling Utilities for the Synthetic Errands Scheduler

This module provides common utility functions for scheduling operations,
used across different scheduling algorithms.
"""

import logging
from typing import Tuple, Optional
from datetime import datetime, timedelta, time
from models.customer import Customer
from models.contractor import Contractor
from models.errand import Errand
from models.contractor_calendar import ContractorCalendar
from utils.travel_time import calculate_travel_time
from utils.errand_utils import get_errand_time
from constants import WORK_START_TIME_OBJ, WORK_END_TIME_OBJ
from utils.time_utils import is_time_within_range, calculate_time_difference

logger = logging.getLogger(__name__)

def calculate_total_time(contractor: Contractor, customer: Customer, errand: Errand) -> timedelta:
    """Calculate the total time for an errand, including travel time."""
    travel_time, _ = calculate_travel_time(contractor.location, customer.location)
    errand_time = get_errand_time(errand, contractor.location, customer.location)
    total_time = travel_time + errand_time
    logger.debug(f"Total time calculation: Travel time: {travel_time}, Errand time: {errand_time}, Total: {total_time}")
    return total_time

def is_within_working_hours(start_time: datetime, total_time: timedelta) -> bool:
    """Check if the errand starts within working hours."""
    end_time = (start_time + total_time).time()
    result = is_time_within_range(start_time.time(), WORK_START_TIME_OBJ, WORK_END_TIME_OBJ)
    logger.debug(f"Working hours check: Start: {start_time.time()}, End: {end_time}, Result: {result}")
    return result

def calculate_next_available_time(contractor: Contractor, customer: Customer, current_datetime: datetime) -> Optional[datetime]:
    """Calculate the next available time for a contractor, considering travel time and working hours."""
    travel_time, _ = calculate_travel_time(contractor.location, customer.location)
    errand_time = get_errand_time(customer.desired_errand, contractor.location, customer.location)
    total_time = travel_time + errand_time

    next_slot = contractor.calendar.get_next_available_slot(current_datetime, total_time)
    if next_slot:
        start_time = next_slot['start']
        end_time = start_time + total_time

        # Check if the errand starts within working hours
        if is_within_working_hours(start_time, total_time):
            # Double-check availability using ContractorCalendar
            if contractor.calendar.is_available(start_time, end_time):
                logger.debug(f"Next available time found: {start_time}")
                return start_time

        # If not within working hours or not available, try the next day
        next_day = current_datetime + timedelta(days=1)
        logger.debug(f"No suitable time found, trying next day: {next_day}")
        return calculate_next_available_time(contractor, customer, next_day)

    logger.debug(f"No available slot found for contractor {contractor.id}")
    return None

def calculate_profit(customer: Customer, contractor: Contractor, start_time: datetime, total_time: timedelta) -> float:
    """Calculate the profit for a specific errand assignment."""
    charge = customer.desired_errand.calculate_final_charge(start_time, datetime.now())
    cost = calculate_time_difference(start_time, start_time + total_time).total_seconds() / 60 * contractor.rate
    profit = charge - cost
    logger.debug(f"Profit calculation: Charge: ${charge:.2f}, Cost: ${cost:.2f}, Profit: ${profit:.2f}")
    return profit

def find_next_available_slot(calendar: ContractorCalendar, start_datetime: datetime, duration: timedelta) -> Optional[datetime]:
    """
    Find the next available time slot in the contractor's calendar.

    Args:
        calendar (ContractorCalendar): The contractor's calendar.
        start_datetime (datetime): The datetime to start searching from.
        duration (timedelta): The duration of the required time slot.

    Returns:
        Optional[datetime]: The start time of the next available slot, or None if no slot is found.
    """
    end_date = start_datetime + timedelta(days=14)  # Look up to two weeks ahead
    current_datetime = start_datetime

    while current_datetime < end_date:
        next_slot = calendar.get_next_available_slot(current_datetime, duration)
        if next_slot:
            logger.debug(f"Next available slot found: {next_slot['start']}")
            return next_slot['start']
        current_datetime += timedelta(days=1)
    
    logger.debug(f"No available slot found within {(end_date - start_datetime).days} days")
    return None

def is_valid_assignment(contractor: Contractor, customer: Customer, start_time: datetime, end_time: datetime) -> bool:
    """
    Check if an assignment is valid based on contractor availability and working hours.

    Args:
        contractor (Contractor): The contractor to be assigned.
        customer (Customer): The customer with the errand.
        start_time (datetime): The proposed start time of the assignment.
        end_time (datetime): The proposed end time of the assignment.

    Returns:
        bool: True if the assignment is valid, False otherwise.
    """
    logger.debug(f"Checking assignment validity for Contractor {contractor.id} and Customer {customer.id}")
    logger.debug(f"Errand type: {customer.desired_errand.type}, Start time: {start_time}, End time: {end_time}")

    total_time = calculate_total_time(contractor, customer, customer.desired_errand)
    
    if end_time - start_time < total_time:
        logger.debug(f"Invalid assignment: Scheduled time ({end_time - start_time}) is less than required time ({total_time})")
        return False
    
    if not is_within_working_hours(start_time, total_time):
        logger.debug(f"Invalid assignment: Start time not within working hours")
        return False
    
    if not contractor.calendar.is_available(start_time, end_time):
        logger.debug(f"Invalid assignment: Contractor {contractor.id} is not available")
        return False
    
    travel_time, _ = calculate_travel_time(contractor.location, customer.location)
    work_start_datetime = datetime.combine(start_time.date(), WORK_START_TIME_OBJ)
    if start_time < work_start_datetime + travel_time:
        logger.debug(f"Invalid assignment: Not enough time for travel before work start")
        return False
    
    logger.debug(f"Valid assignment found for Contractor {contractor.id} and Customer {customer.id}")
    return True

def calculate_assignment_profit(customer: Customer, contractor: Contractor, start_time: datetime, end_time: datetime) -> float:
    """
    Calculate the profit for a specific assignment.

    Args:
        customer (Customer): The customer with the errand.
        contractor (Contractor): The contractor assigned to the errand.
        start_time (datetime): The start time of the assignment.
        end_time (datetime): The end time of the assignment.

    Returns:
        float: The calculated profit for the assignment.
    """
    total_time = end_time - start_time
    charge = customer.desired_errand.calculate_final_charge(start_time, datetime.now())
    cost = total_time.total_seconds() / 60 * contractor.rate
    profit = charge - cost
    logger.debug(f"Assignment profit: Charge: ${charge:.2f}, Cost: ${cost:.2f}, Profit: ${profit:.2f}")
    return profit