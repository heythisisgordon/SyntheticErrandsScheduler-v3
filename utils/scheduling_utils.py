"""
Scheduling utilities for the Synthetic Errands Scheduler.
Provides common utility functions for scheduling operations used across different algorithms.
"""

import logging
from typing import Optional, Tuple
from datetime import datetime, timedelta
from models.customer import Customer
from models.contractor import Contractor
from models.errand import Errand
from utils.errand_utils import calculate_total_errand_time
from constants import WORK_START_TIME_OBJ, WORK_END_TIME_OBJ
from utils.time_utils import is_time_within_range, calculate_time_difference

logger = logging.getLogger(__name__)

def calculate_total_time(contractor: Contractor, customer: Customer, errand: Errand) -> timedelta:
    """Calculate the total time for an errand, including travel time."""
    return calculate_total_errand_time(errand, contractor.location, customer.location)

def is_within_working_hours(start_time: datetime, total_time: timedelta) -> bool:
    """Check if the errand starts and ends within working hours."""
    end_time = (start_time + total_time).time()
    return is_time_within_range(start_time.time(), WORK_START_TIME_OBJ, WORK_END_TIME_OBJ) and end_time <= WORK_END_TIME_OBJ

def calculate_next_available_time(contractor: Contractor, customer: Customer, current_datetime: datetime) -> Optional[datetime]:
    """Calculate the next available time for a contractor, considering travel time and working hours."""
    total_time = calculate_total_time(contractor, customer, customer.desired_errand)
    next_slot = contractor.calendar.get_next_available_slot(current_datetime, total_time)
    
    if next_slot:
        start_time = next_slot['start']
        end_time = start_time + total_time
        if is_within_working_hours(start_time, total_time) and contractor.calendar.is_available(start_time, end_time):
            return start_time
        
        return calculate_next_available_time(contractor, customer, current_datetime + timedelta(days=1))

    return None

def calculate_profit(customer: Customer, contractor: Contractor, start_time: datetime, total_time: timedelta) -> float:
    """Calculate the profit for a specific errand assignment."""
    charge = customer.desired_errand.calculate_final_charge(start_time, datetime.now())
    cost = calculate_time_difference(start_time, start_time + total_time).total_seconds() / 60 * contractor.rate
    return charge - cost

def is_valid_assignment(contractor: Contractor, customer: Customer, start_time: datetime, end_time: datetime) -> bool:
    """Check if an assignment is valid based on contractor availability and working hours."""
    total_time = calculate_total_time(contractor, customer, customer.desired_errand)
    
    # Check if the available time slot is at least 50% of the required total time
    minimum_required_time = total_time / 2
    
    return all([
        end_time - start_time >= minimum_required_time,
        is_within_working_hours(start_time, min(total_time, end_time - start_time)),
        contractor.calendar.is_available(start_time, end_time),
        has_sufficient_travel_time(contractor, customer, start_time)
    ])

def has_sufficient_travel_time(contractor: Contractor, customer: Customer, start_time: datetime) -> bool:
    """Check if there's sufficient time for travel before the errand start time."""
    travel_time = calculate_total_errand_time(customer.desired_errand, contractor.location, customer.location) - customer.desired_errand.base_time
    work_start_datetime = datetime.combine(start_time.date(), WORK_START_TIME_OBJ)
    return start_time >= work_start_datetime + travel_time

def get_assignment_details(customer: Customer, contractor: Contractor, start_time: datetime) -> Tuple[datetime, timedelta, float]:
    """Get the details of an assignment including end time, total time, and profit."""
    total_time = calculate_total_time(contractor, customer, customer.desired_errand)
    end_time = start_time + total_time
    profit = calculate_profit(customer, contractor, start_time, total_time)
    return end_time, total_time, profit