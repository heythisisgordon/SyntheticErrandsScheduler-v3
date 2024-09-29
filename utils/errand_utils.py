"""
Utility functions for handling errands in the Synthetic Errands Scheduler.

This module provides functions for calculating errand times, taking into account
travel time and any additional time required for specific errand types.
"""

from datetime import datetime, timedelta
from utils.travel_time import calculate_travel_time
from constants import DELIVERY_ADDITIONAL_TIME, ErrandType
from models.errand import Errand
from typing import Tuple
from functools import lru_cache

@lru_cache(maxsize=1000)
def calculate_errand_time(errand_id: int, errand_type: ErrandType, base_time: timedelta, start_location: Tuple[int, int], end_location: Tuple[int, int]) -> timedelta:
    """
    Calculate the total time required for an errand, including travel time.

    Args:
        errand_id (int): The ID of the errand (used for caching).
        errand_type (ErrandType): The type of the errand.
        base_time (timedelta): The base time required for the errand.
        start_location (Tuple[int, int]): The starting location (x, y).
        end_location (Tuple[int, int]): The ending location (x, y).

    Returns:
        timedelta: The total time required for the errand.
    """
    travel_time, _ = calculate_travel_time(start_location, end_location)
    
    if errand_type == ErrandType.DELIVERY:
        return travel_time + base_time + timedelta(minutes=DELIVERY_ADDITIONAL_TIME)
    elif errand_type == ErrandType.OUTING:
        return base_time  # No travel time for Outing
    else:
        return travel_time + base_time  # Default case for all other errand types

def get_errand_time(errand: Errand, start_location: Tuple[int, int], end_location: Tuple[int, int]) -> timedelta:
    """
    Wrapper function to call the cached calculate_errand_time function.

    Args:
        errand (Errand): The errand to calculate time for.
        start_location (Tuple[int, int]): The starting location (x, y).
        end_location (Tuple[int, int]): The ending location (x, y).

    Returns:
        timedelta: The total time required for the errand.
    """
    return calculate_errand_time(errand.id, errand.type, errand.base_time, start_location, end_location)

def calculate_errand_end_time(start_time: datetime, errand_duration: timedelta) -> datetime:
    """
    Calculate the end time of an errand given its start time and duration.

    Args:
        start_time (datetime): The start time of the errand.
        errand_duration (timedelta): The duration of the errand.

    Returns:
        datetime: The end time of the errand.
    """
    return start_time + errand_duration

# Clear the cache when the module is reloaded (useful for testing and development)
calculate_errand_time.cache_clear()