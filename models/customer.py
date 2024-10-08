"""
Customer model for the Synthetic Errands Scheduler

This module defines the Customer class, which represents a customer in the scheduling system.
It includes attributes for customer identification, location, desired errand, and availability.
"""

from typing import Dict, List, Tuple
from datetime import datetime
from models.errand import Errand

class Customer:
    """
    Represents a customer in the scheduling system.

    Attributes:
        id (int): Unique identifier for the customer.
        location (Tuple[int, int]): The (x, y) coordinates of the customer's location.
        desired_errand (Errand): The errand requested by the customer.
        availability (Dict[datetime, List[Tuple[datetime, datetime]]]): A dictionary mapping dates to lists of available time slots.
    """

    def __init__(self, id: int, location: Tuple[int, int], desired_errand: Errand, availability: Dict[datetime, List[Tuple[datetime, datetime]]]):
        """
        Initialize a Customer object.

        Args:
            id (int): Unique identifier for the customer.
            location (Tuple[int, int]): The (x, y) coordinates of the customer's location.
            desired_errand (Errand): The errand requested by the customer.
            availability (Dict[datetime, List[Tuple[datetime, datetime]]]): A dictionary mapping dates to lists of available time slots.
        """
        self.id: int = id
        self.location: Tuple[int, int] = location
        self.desired_errand: Errand = desired_errand
        self.availability: Dict[datetime, List[Tuple[datetime, datetime]]] = availability

    def is_available(self, start_time: datetime, end_time: datetime) -> bool:
        # Always return True, indicating the customer is always available
        return True

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