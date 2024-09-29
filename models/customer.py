"""
Customer model for the Synthetic Errands Scheduler

This module defines the Customer class, which represents a customer in the scheduling system.
It includes attributes for customer identification, location, desired errand, and availability.
"""

from typing import Dict, List, Tuple
from datetime import datetime, time
from models.errand import Errand

class Customer:
    """
    Represents a customer in the scheduling system.

    Attributes:
        id (int): Unique identifier for the customer.
        location (Tuple[int, int]): The (x, y) coordinates of the customer's location.
        desired_errand (Errand): The errand requested by the customer.
        availability (Dict[datetime, List[Tuple[time, time]]]): A dictionary mapping dates to lists of available time slots.
    """

    def __init__(self, id: int, location: Tuple[int, int], desired_errand: Errand, availability: Dict[datetime, List[Tuple[time, time]]]):
        """
        Initialize a Customer object.

        Args:
            id (int): Unique identifier for the customer.
            location (Tuple[int, int]): The (x, y) coordinates of the customer's location.
            desired_errand (Errand): The errand requested by the customer.
            availability (Dict[datetime, List[Tuple[time, time]]]): A dictionary mapping dates to lists of available time slots.
        """
        self.id: int = id
        self.location: Tuple[int, int] = location
        self.desired_errand: Errand = desired_errand
        self.availability: Dict[datetime, List[Tuple[time, time]]] = availability

    def is_available(self, date: datetime, start_time: time, end_time: time) -> bool:
        """
        Check if the customer is available for a given time slot on a specific date.

        Args:
            date (datetime): The date to check availability for.
            start_time (time): The start time of the time slot.
            end_time (time): The end time of the time slot.

        Returns:
            bool: True if the customer is available, False otherwise.
        """
        if date not in self.availability:
            return False
        
        for avail_start, avail_end in self.availability[date]:
            if avail_start <= start_time and end_time <= avail_end:
                return True
        
        return False

    def __str__(self) -> str:
        """
        Return a string representation of the Customer object.

        Returns:
            str: A string describing the Customer object.
        """
        return f"Customer(id={self.id}, location={self.location}, errand={self.desired_errand})"

    def __repr__(self) -> str:
        """
        Return a string representation of the Customer object.

        Returns:
            str: A string describing the Customer object.
        """
        return self.__str__()