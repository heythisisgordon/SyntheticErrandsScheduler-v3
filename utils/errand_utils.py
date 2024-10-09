"""
Utility functions for handling errands in the Synthetic Errands Scheduler.

This module provides functions for calculating errand times, taking into account
travel time and any additional time required for specific errand types.
"""

from datetime import timedelta
from utils.travel_time import calculate_travel_time
from constants import DELIVERY_ADDITIONAL_TIME, ErrandType
from models.errand import Errand
from models.customer import Customer
from models.contractor import Contractor
from typing import Tuple, Union

def calculate_total_errand_time(errand: Union[Errand, Customer], start_location: Tuple[int, int], end_location: Tuple[int, int]) -> timedelta:
    """
    Calculate the total time required for an errand, including travel time.

    This function can be used with either an Errand object or a Customer object (which has a desired_errand).

    Args:
        errand (Union[Errand, Customer]): The errand or customer to calculate time for.
        start_location (Tuple[int, int]): The starting location (x, y).
        end_location (Tuple[int, int]): The ending location (x, y).

    Returns:
        timedelta: The total time required for the errand, including travel time.
    """
    if isinstance(errand, Customer):
        errand = errand.desired_errand

    travel_time, _ = calculate_travel_time(start_location, end_location)
    
    if errand.type == ErrandType.DELIVERY:
        return travel_time + errand.base_time + timedelta(minutes=DELIVERY_ADDITIONAL_TIME)
    elif errand.type == ErrandType.OUTING:
        return errand.base_time  # No travel time for Outing
    else:
        return travel_time + errand.base_time  # Default case for all other errand types