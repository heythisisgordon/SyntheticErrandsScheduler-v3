"""
Contractor model for the Synthetic Errands Scheduler

This module defines the Contractor class, which represents a contractor in the scheduling system.
It includes attributes for contractor identification, location, schedule, rate, and calendar.
"""

from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
from .contractor_calendar import ContractorCalendar

class Contractor:
    """
    Represents a contractor in the scheduling system.

    Attributes:
        id (int): Unique identifier for the contractor.
        location (Tuple[int, int]): The current (x, y) coordinates of the contractor's location.
        initial_location (Tuple[int, int]): The initial (x, y) coordinates of the contractor's location.
        schedule (Dict[datetime, List[Tuple[datetime, datetime]]]): A dictionary mapping dates to lists of time slots (start and end times).
        rate (float): The contractor's rate per minute.
        calendar (ContractorCalendar): The contractor's calendar for managing availability and assignments.
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
        self.calendar: ContractorCalendar = ContractorCalendar()

    def is_available(self, start_time: datetime, end_time: datetime) -> bool:
        """
        Check if the contractor is available for a given time slot.

        Args:
            start_time (datetime): The start time of the time slot.
            end_time (datetime): The end time of the time slot.

        Returns:
            bool: True if the contractor is available, False otherwise.
        """
        return self.calendar.is_available(start_time, end_time)

    def add_assignment(self, start_time: datetime, end_time: datetime) -> bool:
        """
        Add an assignment to the contractor's schedule and calendar.

        Args:
            start_time (datetime): The start time of the assignment.
            end_time (datetime): The end time of the assignment.

        Returns:
            bool: True if the assignment was successfully added, False otherwise.
        """
        if self.calendar.reserve_time_slot(start_time, end_time):
            date = start_time.date()
            if date not in self.schedule:
                self.schedule[date] = []
            self.schedule[date].append((start_time, end_time))
            self.schedule[date].sort(key=lambda x: x[0])  # Sort assignments by start time
            return True
        return False

    def get_next_available_slot(self, start_datetime: datetime, min_duration: timedelta) -> Optional[Dict[str, datetime]]:
        """
        Get the next available time slot for the contractor starting from a given datetime.

        Args:
            start_datetime (datetime): The datetime to start checking for availability.
            min_duration (timedelta): The minimum duration required for the time slot.

        Returns:
            Optional[Dict[str, datetime]]: A dictionary with 'start' and 'end' keys representing the next available time slot,
                                           or None if no suitable slot is available.
        """
        return self.calendar.get_next_available_slot(start_datetime, min_duration)

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