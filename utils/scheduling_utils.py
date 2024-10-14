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
from utils.travel_time import calculate_travel_time
from constants import WORK_START_TIME_OBJ, WORK_END_TIME_OBJ
from utils.time_utils import is_time_within_range, calculate_time_difference

logger = logging.getLogger(__name__)

class SchedulingUtilities:
    @staticmethod
    def is_within_working_hours(start_time: datetime, end_time: datetime) -> bool:
        """Check if the errand starts and ends within working hours."""
        return (is_time_within_range(start_time.time(), WORK_START_TIME_OBJ, WORK_END_TIME_OBJ) and
                is_time_within_range(end_time.time(), WORK_START_TIME_OBJ, WORK_END_TIME_OBJ))

    @staticmethod
    def calculate_next_available_time(contractor: Contractor, customer: Customer, current_datetime: datetime) -> Optional[datetime]:
        """Calculate the next available time for a contractor, considering travel time and working hours."""
        travel_duration, _ = calculate_travel_time(contractor.location, customer.location)
        total_time = travel_duration + customer.desired_errand.base_time
        next_available_slot = contractor.calendar.get_next_available_slot(current_datetime, total_time)
        
        if next_available_slot:
            potential_start_time = next_available_slot['start']
            potential_end_time = potential_start_time + total_time
            if SchedulingUtilities.is_within_working_hours(potential_start_time, potential_end_time) and contractor.calendar.is_available(potential_start_time, potential_end_time):
                return potential_start_time
            
            return SchedulingUtilities.calculate_next_available_time(contractor, customer, current_datetime + timedelta(days=1))

        return None

    @staticmethod
    def calculate_profit(customer: Customer, contractor: Contractor, travel_start_time: datetime, task_end_time: datetime) -> float:
        """Calculate the profit for a specific errand assignment."""
        charge = customer.desired_errand.calculate_final_charge(travel_start_time, datetime.now())
        total_time = task_end_time - travel_start_time
        cost = total_time.total_seconds() / 60 * contractor.rate
        return charge - cost

    @staticmethod
    def is_valid_assignment(contractor: Contractor, customer: Customer, travel_start_time: datetime, task_end_time: datetime) -> bool:
        """Check if an assignment is valid based on contractor availability and working hours."""
        return all([
            SchedulingUtilities.is_within_working_hours(travel_start_time, task_end_time),
            contractor.calendar.is_available(travel_start_time, task_end_time)
        ])

    @staticmethod
    def has_sufficient_travel_time(contractor: Contractor, customer: Customer, travel_start_time: datetime, task_end_time: datetime) -> bool:
        """
        Check if the errand base time + travel time fits within the time slot being evaluated.
        Returns True if there is sufficient time, False otherwise.
        """
        travel_duration, _ = calculate_travel_time(contractor.location, customer.location)
        total_time = travel_duration + customer.desired_errand.base_time
        return task_end_time - travel_start_time >= total_time

    @staticmethod
    def get_assignment_details(customer: Customer, contractor: Contractor, travel_start_time: datetime) -> Tuple[datetime, datetime, timedelta, float]:
        """Get the details of an assignment including travel end time, task end time, total time, and profit."""
        travel_duration, _ = calculate_travel_time(contractor.location, customer.location)
        task_duration = customer.desired_errand.base_time
        total_duration = travel_duration + task_duration
        travel_end_time = travel_start_time + travel_duration
        task_end_time = travel_end_time + task_duration
        profit = SchedulingUtilities.calculate_profit(customer, contractor, travel_start_time, task_end_time)
        return travel_end_time, task_end_time, total_duration, profit
