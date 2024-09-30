"""
Contractor model for the Synthetic Errands Scheduler

This module defines the Contractor class, which represents a contractor in the scheduling system.
It includes attributes for contractor identification, location, schedule, and rate.
"""

from typing import Dict, List, Tuple
from datetime import datetime, time

class Contractor:
    """
    Represents a contractor in the scheduling system.

    Attributes:
        id (int): Unique identifier for the contractor.
        location (Tuple[int, int]): The current (x, y) coordinates of the contractor's location.
        initial_location (Tuple[int, int]): The initial (x, y) coordinates of the contractor's location.
        schedule (Dict[datetime, List[Tuple[datetime, datetime]]]): A dictionary mapping dates to lists of time slots (start and end times).
        rate (float): The contractor's rate per minute.
    """

    def __init__(self, id: int, location: Tuple[int, int], rate: float):
        """
        Initialize a Contractor object.

        Args:
            id (int): Unique identifier for the contractor.
            location (Tuple[int, int]): The (x, y) coordinates of the contractor's initial location.
            rate (float): The contractor's rate per minute.
        """
        self.id: int = id
        self.location: Tuple[int, int] = location
        self.initial_location: Tuple[int, int] = location
        self.schedule: Dict[datetime, List[Tuple[datetime, datetime]]] = {}
        self.rate: float = rate

    def is_available(self, date: datetime, start_time: datetime, end_time: datetime) -> bool:
        """
        Check if the contractor is available for a given time slot on a specific date.

        Args:
            date (datetime): The date to check availability for.
            start_time (datetime): The start time of the time slot.
            end_time (datetime): The end time of the time slot.

        Returns:
            bool: True if the contractor is available, False otherwise.
        """
        if date not in self.schedule:
            return True
        
        for scheduled_start, scheduled_end in self.schedule[date]:
            if (start_time < scheduled_end and end_time > scheduled_start):
                return False
        
        return True

    def add_assignment(self, date: datetime, start_time: datetime, end_time: datetime) -> None:
        """
        Add an assignment to the contractor's schedule.

        Args:
            date (datetime): The date of the assignment.
            start_time (datetime): The start time of the assignment.
            end_time (datetime): The end time of the assignment.
        """
        if date not in self.schedule:
            self.schedule[date] = []
        
        self.schedule[date].append((start_time, end_time))
        self.schedule[date].sort(key=lambda x: x[0])  # Sort assignments by start time

    def __str__(self) -> str:
        """
        Return a string representation of the Contractor object.

        Returns:
            str: A string describing the Contractor object.
        """
        return f"Contractor(id={self.id}, location={self.location}, rate=${self.rate:.2f}/minute)"

    def __repr__(self) -> str:
        """
        Return a string representation of the Contractor object.

        Returns:
            str: A string describing the Contractor object.
        """
        return self.__str__()