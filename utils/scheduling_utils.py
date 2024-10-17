"""
Scheduling utilities for the Synthetic Errands Scheduler.
Provides common utility functions for scheduling operations used across different algorithms.
"""

import logging
from typing import Optional, Tuple
import pandas as pd
from models.customer import Customer
from models.contractor import Contractor
from models.errand import Errand
from utils.travel_time import calculate_travel_time
from constants import WORK_START_TIME_OBJ, WORK_END_TIME_OBJ, TIME_BLOCKS
from utils.time_utils import is_time_within_range, calculate_time_difference

logger = logging.getLogger(__name__)

class SchedulingUtilities:
    @staticmethod
    def is_within_working_hours(start_time: pd.Timestamp, end_time: pd.Timestamp) -> bool:
        """Check if the errand starts and ends within working hours."""
        return (is_time_within_range(start_time, WORK_START_TIME_OBJ, WORK_END_TIME_OBJ) and
                is_time_within_range(end_time, WORK_START_TIME_OBJ, WORK_END_TIME_OBJ))

    @staticmethod
    def calculate_next_available_time(contractor: Contractor, customer: Customer, current_datetime: pd.Timestamp) -> Optional[pd.Timestamp]:
        """Calculate the next available time for a contractor, considering travel time and working hours."""
        travel_duration, _ = calculate_travel_time(contractor.location, customer.location)
        total_time = travel_duration + customer.desired_errand.base_time
        total_blocks = int(total_time.total_seconds() / (TIME_BLOCKS * 60))

        schedule = contractor.schedule
        current_datetime = max(current_datetime, schedule.index.get_level_values('Date').min())

        # Ensure we start from the work start time
        if current_datetime.time() < WORK_START_TIME_OBJ.time():
            current_datetime = pd.Timestamp.combine(current_datetime.date(), WORK_START_TIME_OBJ.time())

        while current_datetime <= schedule.index.get_level_values('Date').max():
            mask = (schedule.index.get_level_values('Date') == current_datetime.floor('D')) & \
                   (schedule.index.get_level_values('Time') >= current_datetime.time())
            available_slots = schedule[mask]

            if len(available_slots) >= total_blocks and available_slots['Client_ID'].isnull().all():
                potential_end_time = current_datetime + total_time

                if SchedulingUtilities.is_within_working_hours(current_datetime, potential_end_time):
                    return current_datetime

            current_datetime += pd.Timedelta(minutes=TIME_BLOCKS)

            # If we've passed the end of the working day, move to the start of the next day
            if current_datetime.time() > WORK_END_TIME_OBJ.time():
                current_datetime = pd.Timestamp.combine(current_datetime.date() + pd.Timedelta(days=1), WORK_START_TIME_OBJ.time())

        return None

    @staticmethod
    def calculate_profit(customer: Customer, contractor: Contractor, travel_start_time: pd.Timestamp, task_end_time: pd.Timestamp) -> float:
        """Calculate the profit for a specific errand assignment."""
        charge = customer.desired_errand.calculate_final_charge(travel_start_time, pd.Timestamp.now())
        total_time = task_end_time - travel_start_time
        cost = total_time.total_seconds() / 60 * contractor.rate
        return charge - cost

    @staticmethod
    def is_valid_assignment(contractor: Contractor, customer: Customer, travel_start_time: pd.Timestamp, task_end_time: pd.Timestamp) -> bool:
        """Check if an assignment is valid based on contractor availability and working hours."""
        if not SchedulingUtilities.is_within_working_hours(travel_start_time, task_end_time):
            return False

        schedule = contractor.schedule
        mask = (schedule.index.get_level_values('Date') >= travel_start_time.floor('D')) & \
               (schedule.index.get_level_values('Date') <= task_end_time.floor('D')) & \
               (
                   ((schedule.index.get_level_values('Date') == travel_start_time.floor('D')) & (schedule.index.get_level_values('Time') >= travel_start_time.time())) |
                   ((schedule.index.get_level_values('Date') == task_end_time.floor('D')) & (schedule.index.get_level_values('Time') < task_end_time.time())) |
                   ((schedule.index.get_level_values('Date') > travel_start_time.floor('D')) & (schedule.index.get_level_values('Date') < task_end_time.floor('D')))
               )
        return schedule.loc[mask, 'Client_ID'].isnull().all()

    @staticmethod
    def has_sufficient_travel_time(contractor: Contractor, customer: Customer, travel_start_time: pd.Timestamp, task_end_time: pd.Timestamp) -> bool:
        """
        Check if the errand base time + travel time fits within the time slot being evaluated.
        Returns True if there is sufficient time, False otherwise.
        """
        travel_duration, _ = calculate_travel_time(contractor.location, customer.location)
        total_time = travel_duration + customer.desired_errand.base_time
        return task_end_time - travel_start_time >= total_time

    @staticmethod
    def get_assignment_details(customer: Customer, contractor: Contractor, travel_start_time: pd.Timestamp) -> Tuple[pd.Timestamp, pd.Timestamp, pd.Timedelta, float]:
        """Get the details of an assignment including travel end time, task end time, total time, and profit."""
        travel_duration, _ = calculate_travel_time(contractor.location, customer.location)
        task_duration = customer.desired_errand.base_time
        total_duration = travel_duration + task_duration
        travel_end_time = travel_start_time + travel_duration
        task_end_time = travel_end_time + task_duration
        profit = SchedulingUtilities.calculate_profit(customer, contractor, travel_start_time, task_end_time)
        return travel_end_time, task_end_time, total_duration, profit
