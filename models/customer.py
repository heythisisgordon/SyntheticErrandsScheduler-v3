"""
Customer model for the Synthetic Errands Scheduler.
Defines the Customer class representing a customer in the scheduling system.
"""

from typing import List, Tuple
import pandas as pd
from models.errand import Errand

class Customer:

    def __init__(self, id: int, location: Tuple[int, int], desired_errand: Errand, availability: List[Tuple[pd.Timestamp, List[Tuple[pd.Timestamp, pd.Timestamp]]]]):
        self.id: int = id
        self.location: Tuple[int, int] = location
        self.desired_errand: Errand = desired_errand
        self.availability: List[Tuple[pd.Timestamp, List[Tuple[pd.Timestamp, pd.Timestamp]]]] = availability

    def __str__(self) -> str:
        """Return a string representation of the Customer object."""
        return f"Customer(id={self.id}, location={self.location}, errand={self.desired_errand})"

    __repr__ = __str__
