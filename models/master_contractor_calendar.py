"""
MasterContractorCalendar class for managing multiple contractor calendars.
"""

import logging
from typing import Dict, Optional, Tuple, List
from models.contractor_calendar import ContractorCalendar
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class MasterContractorCalendar:
    def __init__(self):
        self.contractor_calendars: Dict[str, ContractorCalendar] = {}

    def add_contractor_calendar(self, contractor_id: str, calendar: ContractorCalendar) -> None:
        """Add a contractor's calendar to the master calendar."""
        self.contractor_calendars[contractor_id] = calendar

    def is_contractor_available(self, contractor_id: str, start_time: datetime, end_time: datetime) -> bool:
        """Check if a specific contractor is available for a given time slot."""
        self._validate_contractor(contractor_id)
        return self.contractor_calendars[contractor_id].is_available(start_time, end_time)

    def get_contractor_next_available_slot(self, contractor_id: str, start_datetime: datetime, min_duration: timedelta) -> Optional[Dict[str, datetime]]:
        """Get the next available slot for a specific contractor."""
        self._validate_contractor(contractor_id)
        return self.contractor_calendars[contractor_id].get_next_available_slot(start_datetime, min_duration)

    def reserve_time_slot(self, contractor_id: str, errand_id: str, start_time: datetime, end_time: datetime) -> bool:
        """Reserve a time slot for a specific contractor."""
        self._validate_contractor(contractor_id)
        result = self.contractor_calendars[contractor_id].reserve_time_slot(errand_id, start_time, end_time)
        if not result:
            logger.warning(f"Failed to reserve time slot for contractor {contractor_id}: Errand {errand_id}, {start_time} - {end_time}")
        return result

    def find_first_available_slot(self, start_datetime: datetime, duration: timedelta) -> Tuple[Optional[str], Optional[Dict[str, datetime]]]:
        """Find the first available slot across all contractors."""
        earliest_slot = None
        earliest_contractor = None

        for contractor_id, calendar in self.contractor_calendars.items():
            slot = calendar.get_next_available_slot(start_datetime, duration)
            if slot and (earliest_slot is None or slot['start'] < earliest_slot['start']):
                earliest_slot = slot
                earliest_contractor = contractor_id

        if not earliest_contractor:
            logger.warning("No available slot found across all contractors")

        return earliest_contractor, earliest_slot

    def get_contractor_errands(self, contractor_id: str, date: datetime) -> List[Dict[str, datetime]]:
        """Get all errands for a specific contractor on a given date."""
        self._validate_contractor(contractor_id)
        return self.contractor_calendars[contractor_id].errands.get(date, [])

    def get_contractor_availability(self, contractor_id: str, date: datetime) -> List[Tuple[datetime, datetime]]:
        """Get all availability slots for a specific contractor on a given date."""
        self._validate_contractor(contractor_id)
        return self.contractor_calendars[contractor_id].calendar.get(date, [])

    def _validate_contractor(self, contractor_id: str) -> None:
        """Validate that the contractor exists in the master calendar."""
        if contractor_id not in self.contractor_calendars:
            raise ValueError(f"Contractor {contractor_id} not found in master calendar.")

    def get_all_contractors_availability(self, date: datetime) -> Dict[str, List[Tuple[datetime, datetime]]]:
        """Get availability for all contractors on a given date."""
        return {
            contractor_id: self.get_contractor_availability(contractor_id, date)
            for contractor_id in self.contractor_calendars
        }

    def get_all_contractors_errands(self, date: datetime) -> Dict[str, List[Dict[str, datetime]]]:
        """Get errands for all contractors on a given date."""
        return {
            contractor_id: self.get_contractor_errands(contractor_id, date)
            for contractor_id in self.contractor_calendars
        }