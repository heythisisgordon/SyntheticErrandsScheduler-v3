"""
Contractor model for the Synthetic Errands Scheduler.
Defines the Contractor class representing a contractor in the scheduling system.
"""

from typing import Tuple, Optional, Dict, List
import pandas as pd
from constants import WORK_START_TIME_OBJ, WORK_END_TIME_OBJ, TIME_BLOCKS

class Contractor:
    """Represents a contractor in the scheduling system."""

    def __init__(self, id: int, location: Tuple[int, int], rate: float):
        self.id: int = id
        self.location: Tuple[int, int] = location
        self.initial_location: Tuple[int, int] = location  # Starting location for each day
        self.rate: float = rate
        self.schedule = None  # Initialize as None
    
    def initialize_schedule(self, schedule_manager):
        """Initialize the schedule using ScheduleManager"""
        if self.schedule is None or self.schedule.empty:
            self.schedule = schedule_manager._generate_empty_schedule()

    def update_location(self, new_location: Tuple[int, int]) -> None:
        """Update the contractor's current location."""
        self.location = new_location

    def __str__(self) -> str:
        """Return a string representation of the Contractor object."""
        return f"Contractor(id={self.id}, location={self.location}, rate=${self.rate:.2f}/minute)"

    __repr__ = __str__
