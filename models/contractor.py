"""
Contractor model for the Synthetic Errands Scheduler.
Defines the Contractor class representing a contractor in the scheduling system.
"""

from typing import Tuple, Optional, Dict, List
from datetime import datetime, timedelta
from .contractor_calendar import ContractorCalendar

class Contractor:
    """Represents a contractor in the scheduling system."""

    def __init__(self, id: int, location: Tuple[int, int], rate: float):
        self.id: int = id
        self.location: Tuple[int, int] = location
        self.initial_location: Tuple[int, int] = location  # Starting location for each day
        self.rate: float = rate
        self.calendar: ContractorCalendar = ContractorCalendar()

    def is_available(self, start_time: datetime, end_time: datetime) -> bool:
        """Check if the contractor is available for a given time slot."""
        return self.calendar.is_available(start_time, end_time)

    def reserve_time_slot(self, start_time: datetime, end_time: datetime) -> bool:
        """Reserve a time slot in the contractor's calendar."""
        return self.calendar.reserve_time_slot(start_time, end_time)

    def remove_time_slot(self, start_time: datetime, end_time: datetime) -> bool:
        """Remove a reserved time slot from the contractor's calendar."""
        return self.calendar.remove_time_slot(start_time, end_time)

    def get_next_available_slot(self, start_datetime: datetime, min_duration: timedelta) -> Optional[Dict[str, datetime]]:
        """
        Get the next available time slot for the contractor.
        Returns a dict with 'start' and 'end' datetime keys, or None if no slot is available.
        """
        return self.calendar.get_next_available_slot(start_datetime, min_duration)

    def reset_location(self) -> None:
        """Reset the contractor's location to the initial location."""
        self.location = self.initial_location

    def update_location(self, new_location: Tuple[int, int]) -> None:
        """Update the contractor's current location."""
        self.location = new_location

    def get_availability_for_date(self, date: datetime) -> List[Tuple[datetime, datetime]]:
        """Get the contractor's availability for a specific date."""
        return self.calendar.get_availability_for_date(date)

    def get_reserved_slots_for_date(self, date: datetime) -> List[Tuple[datetime, datetime]]:
        """Get the contractor's reserved time slots for a specific date."""
        return self.calendar.get_reserved_slots_for_date(date)

    def __str__(self) -> str:
        """Return a string representation of the Contractor object."""
        return f"Contractor(id={self.id}, location={self.location}, rate=${self.rate:.2f}/minute)"

    __repr__ = __str__