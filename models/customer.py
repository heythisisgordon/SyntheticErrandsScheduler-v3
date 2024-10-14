"""
Customer model for the Synthetic Errands Scheduler.
Defines the Customer class representing a customer in the scheduling system.
"""

from typing import Dict, List, Tuple
from datetime import datetime
from models.errand import Errand

class Customer:

    def __init__(self, id: int, location: Tuple[int, int], desired_errand: Errand, availability: Dict[datetime, List[Tuple[datetime, datetime]]]):
        self.id: int = id
        self.location: Tuple[int, int] = location
        self.desired_errand: Errand = desired_errand
        self.availability: Dict[datetime, List[Tuple[datetime, datetime]]] = availability

    def __str__(self) -> str:
        """Return a string representation of the Customer object."""
        return f"Customer(id={self.id}, location={self.location}, errand={self.desired_errand})"

    __repr__ = __str__