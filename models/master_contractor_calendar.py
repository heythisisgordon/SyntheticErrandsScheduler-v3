import logging
from typing import Dict, Optional
from models.contractor_calendar import ContractorCalendar
from models.contractor import Contractor
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class MasterContractorCalendar:
    def __init__(self):
        self.contractor_calendars: Dict[str, ContractorCalendar] = {}

    def add_contractor(self, contractor: Contractor):
        """Add a contractor's calendar to the master calendar."""
        self.contractor_calendars[contractor.id] = contractor.calendar
        logger.info(f"Added contractor {contractor.id} to master calendar")

    def find_first_available_slot(self, start_datetime: datetime, duration: timedelta) -> tuple[Optional[str], Optional[Dict[str, datetime]]]:
        """Find the first available slot across all contractors."""
        logger.debug(f"Searching for first available slot from {start_datetime} with duration {duration}")
        earliest_slot = None
        earliest_contractor = None

        for contractor_id, calendar in self.contractor_calendars.items():
            slot = calendar.get_next_available_slot(start_datetime, duration)
            if slot:
                logger.debug(f"Found slot for contractor {contractor_id}: {slot}")
                if earliest_slot is None or slot['start'] < earliest_slot['start']:
                    earliest_slot = slot
                    earliest_contractor = contractor_id
            else:
                logger.debug(f"No available slot found for contractor {contractor_id}")

        if earliest_contractor and earliest_slot:
            logger.info(f"First available slot found: Contractor {earliest_contractor}, Slot: {earliest_slot}")
        else:
            logger.warning("No available slot found across all contractors")

        return earliest_contractor, earliest_slot

    def reserve_time_slot(self, contractor_id: str, errand_id: str, start_time: datetime, end_time: datetime) -> bool:
        """Reserve a time slot for a specific contractor."""
        if contractor_id not in self.contractor_calendars:
            logger.error(f"Contractor {contractor_id} not found in master calendar.")
            raise ValueError(f"Contractor {contractor_id} not found in master calendar.")

        result = self.contractor_calendars[contractor_id].reserve_time_slot(errand_id, start_time, end_time)
        if result:
            logger.info(f"Reserved time slot for contractor {contractor_id}: Errand {errand_id}, {start_time} - {end_time}")
        else:
            logger.warning(f"Failed to reserve time slot for contractor {contractor_id}: Errand {errand_id}, {start_time} - {end_time}")
        return result

    def is_contractor_available(self, contractor_id: str, start_time: datetime, end_time: datetime) -> bool:
        """Check if a specific contractor is available for a given time slot."""
        if contractor_id not in self.contractor_calendars:
            logger.error(f"Contractor {contractor_id} not found in master calendar.")
            raise ValueError(f"Contractor {contractor_id} not found in master calendar.")

        result = self.contractor_calendars[contractor_id].is_available(start_time, end_time)
        logger.debug(f"Contractor {contractor_id} availability check: {start_time} - {end_time}, Result: {result}")
        return result

    def get_contractor_next_available_slot(self, contractor_id: str, start_datetime: datetime, min_duration: timedelta) -> Optional[Dict[str, datetime]]:
        """Get the next available slot for a specific contractor."""
        if contractor_id not in self.contractor_calendars:
            logger.error(f"Contractor {contractor_id} not found in master calendar.")
            raise ValueError(f"Contractor {contractor_id} not found in master calendar.")

        slot = self.contractor_calendars[contractor_id].get_next_available_slot(start_datetime, min_duration)
        if slot:
            logger.debug(f"Next available slot for contractor {contractor_id}: {slot}")
        else:
            logger.debug(f"No available slot found for contractor {contractor_id} from {start_datetime} with duration {min_duration}")
        return slot

    def get_contractor_errands(self, contractor_id: str, date: datetime) -> list:
        """Get all errands for a specific contractor on a given date."""
        if contractor_id not in self.contractor_calendars:
            logger.error(f"Contractor {contractor_id} not found in master calendar.")
            raise ValueError(f"Contractor {contractor_id} not found in master calendar.")

        errands = self.contractor_calendars[contractor_id].errands.get(date, [])
        logger.debug(f"Errands for contractor {contractor_id} on {date}: {len(errands)} errands")
        return errands

    def get_contractor_availability(self, contractor_id: str, date: datetime) -> list:
        """Get all availability slots for a specific contractor on a given date."""
        if contractor_id not in self.contractor_calendars:
            logger.error(f"Contractor {contractor_id} not found in master calendar.")
            raise ValueError(f"Contractor {contractor_id} not found in master calendar.")

        availability = self.contractor_calendars[contractor_id].calendar.get(date, [])
        logger.debug(f"Availability for contractor {contractor_id} on {date}: {len(availability)} slots")
        return availability