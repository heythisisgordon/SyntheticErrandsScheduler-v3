"""
Customer model for the Synthetic Errands Scheduler.
Defines the Customer class representing a customer in the scheduling system.
"""

from typing import Dict, List, Tuple
from datetime import datetime
from models.errand import Errand

class Customer:
    """Represents a customer in the scheduling system."""

    def __init__(self, id: int, location: Tuple[int, int], desired_errand: Errand, availability: Dict[datetime, List[Tuple[datetime, datetime]]]):
        self.id: int = id
        self.location: Tuple[int, int] = location
        self.desired_errand: Errand = desired_errand
        self.availability: Dict[datetime, List[Tuple[datetime, datetime]]] = availability

    def is_available(self, date: datetime, start_time: datetime, end_time: datetime) -> bool:
        """Check if the customer is available for a given time slot on a specific date."""
        if date not in self.availability:
            return False
        return any(start <= start_time and end_time <= end for start, end in self.availability[date])

    def get_availability_for_date(self, date: datetime) -> List[Tuple[datetime, datetime]]:
        """Get the customer's availability for a specific date."""
        return self.availability.get(date, [])

    def add_availability(self, date: datetime, start_time: datetime, end_time: datetime) -> None:
        """Add a new availability slot for the customer."""
        if date not in self.availability:
            self.availability[date] = []
        self.availability[date].append((start_time, end_time))
        self._sort_availability(date)

    def remove_availability(self, date: datetime, start_time: datetime, end_time: datetime) -> bool:
        """Remove an availability slot for the customer."""
        if date in self.availability:
            slot = (start_time, end_time)
            if slot in self.availability[date]:
                self.availability[date].remove(slot)
                return True
        return False

    def _sort_availability(self, date: datetime) -> None:
        """Sort availability slots for a given date."""
        if date in self.availability:
            self.availability[date].sort(key=lambda x: x[0])

    def __str__(self) -> str:
        """Return a string representation of the Customer object."""
        return f"Customer(id={self.id}, location={self.location}, errand={self.desired_errand})"

    __repr__ = __str__