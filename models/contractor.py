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
    
    def reset_location(self) -> None:
        """Reset the contractor's location to the initial location."""
        self.location = self.initial_location

    def update_location(self, new_location: Tuple[int, int]) -> None:
        """Update the contractor's current location."""
        self.location = new_location

    def __str__(self) -> str:
        """Return a string representation of the Contractor object."""
        return f"Contractor(id={self.id}, location={self.location}, rate=${self.rate:.2f}/minute)"

    __repr__ = __str__