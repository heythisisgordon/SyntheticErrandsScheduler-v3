"""
Errand model for the Synthetic Errands Scheduler

This module defines the Errand class, which represents an errand in the scheduling system.
It includes methods for calculating charges, applying incentives and disincentives.
"""

from datetime import datetime, timedelta, date
from constants import MAX_INCENTIVE_MULTIPLIER, ERRAND_RATES, SCHEDULING_DAYS, ErrandType
from typing import Dict, Union

class Errand:
    """
    Represents an errand in the scheduling system.

    Attributes:
        id (int): Unique identifier for the errand.
        type (ErrandType): Type of the errand.
        base_time (timedelta): Base time required to complete the errand.
        incentive (float): Incentive multiplier for same-day service.
        disincentive (Dict[str, Union[str, int, float]] or None): Disincentive rules for late completion.
        charge (float): Base charge for the errand.
    """

    def __init__(self, id: int, type: ErrandType, base_time: timedelta, incentive: float, disincentive: Union[Dict[str, Union[str, int, float]], None]):
        self.id: int = id
        self.type: ErrandType = type
        self.base_time: timedelta = base_time
        self.incentive: float = incentive
        self.disincentive: Union[Dict[str, Union[str, int, float]], None] = disincentive
        self.charge: float = self.calculate_base_charge()

    def calculate_base_charge(self) -> float:
        """
        Calculate the base charge for the errand.

        Returns:
            float: The base charge for the errand.
        """
        return self.base_time.total_seconds() / 60 * ERRAND_RATES.get(self.type, 1)  # Default to $1 per minute if type not found

    def apply_incentive(self, scheduled_date: Union[datetime, date], request_date: Union[datetime, date]) -> float:
        """
        Apply the incentive for same-day service.

        Args:
            scheduled_date (Union[datetime, date]): The date or datetime the errand is scheduled for.
            request_date (Union[datetime, date]): The date or datetime the errand was requested.

        Returns:
            float: The charge after applying the incentive.
        """
        scheduled_date_only = scheduled_date.date() if isinstance(scheduled_date, datetime) else scheduled_date
        request_date_only = request_date.date() if isinstance(request_date, datetime) else request_date

        if scheduled_date_only == request_date_only:
            incentive_charge = self.charge * self.incentive
            return min(incentive_charge, self.charge * MAX_INCENTIVE_MULTIPLIER)
        return self.charge

    def apply_disincentive(self, scheduled_date: Union[datetime, date], request_date: Union[datetime, date]) -> float:
        """
        Apply the disincentive for late completion.

        Args:
            scheduled_date (Union[datetime, date]): The date or datetime the errand is scheduled for.
            request_date (Union[datetime, date]): The date or datetime the errand was requested.

        Returns:
            float: The charge after applying the disincentive.
        """
        if self.disincentive is None:
            return self.charge

        scheduled_date_only = scheduled_date.date() if isinstance(scheduled_date, datetime) else scheduled_date
        request_date_only = request_date.date() if isinstance(request_date, datetime) else request_date

        days_difference = (scheduled_date_only - request_date_only).days

        # Apply gradual disincentive within SLA window
        if days_difference <= SCHEDULING_DAYS:
            gradual_disincentive = 1 - (days_difference / SCHEDULING_DAYS) * 0.1  # 10% max reduction within SLA
            return self.charge * gradual_disincentive

        # Apply original disincentive for days beyond SLA window
        days_past = days_difference - SCHEDULING_DAYS
        if self.disincentive['type'] == 'percentage':
            reduction = min(self.disincentive['value'] * days_past / 100, 1)  # Cap at 100% reduction
            return max(0, self.charge * (1 - reduction))
        elif self.disincentive['type'] == 'fixed':
            return max(0, self.charge - (self.disincentive['value'] * days_past))
        return self.charge

    def calculate_final_charge(self, scheduled_date: Union[datetime, date], request_date: Union[datetime, date]) -> float:
        """
        Calculate the final charge for the errand, considering incentives and disincentives.

        Args:
            scheduled_date (Union[datetime, date]): The date or datetime the errand is scheduled for.
            request_date (Union[datetime, date]): The date or datetime the errand was requested.

        Returns:
            float: The final charge for the errand.
        """
        incentive_charge = self.apply_incentive(scheduled_date, request_date)
        final_charge = self.apply_disincentive(scheduled_date, request_date)
        return max(incentive_charge, final_charge)

    def __str__(self) -> str:
        return f"Errand(id={self.id}, type={self.type.name}, base_time={self.base_time}, charge=${self.charge:.2f})"

    def __repr__(self) -> str:
        return self.__str__()