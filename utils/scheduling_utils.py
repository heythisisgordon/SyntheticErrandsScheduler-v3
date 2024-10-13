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

class SchedulingUtilities:
    @staticmethod
    def calculate_total_time(contractor: Contractor, customer: Customer, errand: Errand) -> timedelta:
        """Calculate the total time for an errand, including travel time."""
        return calculate_total_errand_time(errand, contractor.location, customer.location)

    @staticmethod
    def is_within_working_hours(start_time: datetime, total_time: timedelta) -> bool:
        """Check if the errand starts and ends within working hours."""
        end_time = (start_time + total_time).time()
        return is_time_within_range(start_time.time(), WORK_START_TIME_OBJ, WORK_END_TIME_OBJ) and end_time <= WORK_END_TIME_OBJ

    @staticmethod
    def calculate_next_available_time(contractor: Contractor, customer: Customer, current_datetime: datetime) -> Optional[datetime]:
        """Calculate the next available time for a contractor, considering travel time and working hours."""
        total_time = SchedulingUtilities.calculate_total_time(contractor, customer, customer.desired_errand)
        next_available_slot = contractor.calendar.get_next_available_slot(current_datetime, total_time)
        
        if next_available_slot:
            potential_start_time = next_available_slot['start']
            potential_end_time = potential_start_time + total_time
            if SchedulingUtilities.is_within_working_hours(potential_start_time, total_time) and contractor.calendar.is_available(potential_start_time, potential_end_time):
                return potential_start_time
            
            return SchedulingUtilities.calculate_next_available_time(contractor, customer, current_datetime + timedelta(days=1))

        return None

    @staticmethod
    def calculate_profit(customer: Customer, contractor: Contractor, start_time: datetime, total_time: timedelta) -> float:
        """Calculate the profit for a specific errand assignment."""
        charge = customer.desired_errand.calculate_final_charge(start_time, datetime.now())
        cost = calculate_time_difference(start_time, start_time + total_time).total_seconds() / 60 * contractor.rate
        return charge - cost

    @staticmethod
    def is_valid_assignment(contractor: Contractor, customer: Customer, start_time: datetime, end_time: datetime) -> bool:
        """Check if an assignment is valid based on contractor availability and working hours."""
        total_time = SchedulingUtilities.calculate_total_time(contractor, customer, customer.desired_errand)
        
        return all([
            SchedulingUtilities.is_within_working_hours(start_time, total_time),
            contractor.calendar.is_available(start_time, start_time + total_time),
            SchedulingUtilities.has_sufficient_travel_time(contractor, customer, start_time, end_time)
        ])

    @staticmethod
    def has_sufficient_travel_time(contractor: Contractor, customer: Customer, start_time: datetime, end_time: datetime) -> bool:
        """
        Check if the errand base time + travel time fits within the time slot being evaluated.
        Returns True if there is sufficient time, False otherwise.
        """
        total_time = SchedulingUtilities.calculate_total_time(contractor, customer, customer.desired_errand)
        errand_end_time = start_time + total_time
        
        # Check if the errand (including travel time) fits within the evaluated time slot
        if errand_end_time <= end_time:
            return True
        else:
            return False

    @staticmethod
    def get_assignment_details(customer: Customer, contractor: Contractor, start_time: datetime) -> Tuple[datetime, timedelta, float]:
        """Get the details of an assignment including end time, total time, and profit."""
        total_time = SchedulingUtilities.calculate_total_time(contractor, customer, customer.desired_errand)
        end_time = start_time + total_time
        profit = SchedulingUtilities.calculate_profit(customer, contractor, start_time, total_time)
        return end_time, total_time, profit
