from datetime import datetime, timedelta
from typing import List, Dict, Optional
from constants import SCHEDULING_DAYS, WORK_START_TIME_OBJ, WORK_END_TIME_OBJ
from utils.time_utils import is_time_within_range, get_next_working_day
import logging

logger = logging.getLogger(__name__)

class ContractorAvailabilitySlot:
    def __init__(self, start_time: datetime, end_time: datetime):
        self.start_time = start_time
        self.end_time = end_time
        self.available = True

class ErrandSlot:
    def __init__(self, errand_id: str, start_time: datetime, end_time: datetime):
        self.errand_id = errand_id
        self.start_time = start_time
        self.end_time = end_time

class ContractorCalendar:
    def __init__(self):
        self.calendar: Dict[datetime, List[ContractorAvailabilitySlot]] = {}
        self.errands: Dict[datetime, List[ErrandSlot]] = {}
        self.start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        self._initialize_calendar()

    def _initialize_calendar(self):
        for day in range(SCHEDULING_DAYS):
            current_date = self.start_date + timedelta(days=day)
            work_start = current_date.replace(hour=WORK_START_TIME_OBJ.hour, minute=WORK_START_TIME_OBJ.minute)
            work_end = current_date.replace(hour=WORK_END_TIME_OBJ.hour, minute=WORK_END_TIME_OBJ.minute)
            self.calendar[current_date] = [ContractorAvailabilitySlot(work_start, work_end)]
            self.errands[current_date] = []
        logger.debug(f"Calendar initialized for {SCHEDULING_DAYS} days starting from {self.start_date}")

    def is_available(self, start_time: datetime, end_time: datetime) -> bool:
        date_key = start_time.replace(hour=0, minute=0, second=0, microsecond=0)
        
        if date_key not in self.calendar:
            logger.debug(f"Date {date_key} is outside the initialized range")
            return False
        
        if not is_time_within_range(start_time.time(), WORK_START_TIME_OBJ, WORK_END_TIME_OBJ) or \
           not is_time_within_range(end_time.time(), WORK_START_TIME_OBJ, WORK_END_TIME_OBJ):
            logger.debug(f"Time slot {start_time} - {end_time} is outside working hours")
            return False
        
        for slot in self.calendar[date_key]:
            if slot.available and slot.start_time <= start_time and slot.end_time >= end_time:
                logger.debug(f"Available slot found: {slot.start_time} - {slot.end_time}")
                return True
        logger.debug(f"No available slot found for {start_time} - {end_time}")
        return False

    def reserve_time_slot(self, errand_id: str, start_time: datetime, end_time: datetime) -> bool:
        if self.is_available(start_time, end_time):
            date_key = start_time.replace(hour=0, minute=0, second=0, microsecond=0)
            new_errand = ErrandSlot(errand_id, start_time, end_time)
            self.errands[date_key].append(new_errand)
            self._update_availability(date_key, start_time, end_time)
            logger.info(f"Reserved time slot for errand {errand_id}: {start_time} - {end_time}")
            return True
        logger.warning(f"Failed to reserve time slot for errand {errand_id}: {start_time} - {end_time}")
        return False

    def _update_availability(self, date_key: datetime, start_time: datetime, end_time: datetime):
        updated_slots = []
        for slot in self.calendar[date_key]:
            if slot.start_time < start_time and slot.end_time > end_time:
                # Split the slot
                updated_slots.append(ContractorAvailabilitySlot(slot.start_time, start_time))
                updated_slots.append(ContractorAvailabilitySlot(end_time, slot.end_time))
                logger.debug(f"Split slot: {slot.start_time} - {slot.end_time} into {slot.start_time} - {start_time} and {end_time} - {slot.end_time}")
            elif slot.start_time >= start_time and slot.end_time <= end_time:
                # Slot is fully covered by the new errand
                logger.debug(f"Removed slot: {slot.start_time} - {slot.end_time}")
                continue
            elif slot.start_time < start_time and slot.end_time > start_time:
                # Partial overlap at the start
                updated_slots.append(ContractorAvailabilitySlot(slot.start_time, start_time))
                logger.debug(f"Updated slot: {slot.start_time} - {slot.end_time} to {slot.start_time} - {start_time}")
            elif slot.start_time < end_time and slot.end_time > end_time:
                # Partial overlap at the end
                updated_slots.append(ContractorAvailabilitySlot(end_time, slot.end_time))
                logger.debug(f"Updated slot: {slot.start_time} - {slot.end_time} to {end_time} - {slot.end_time}")
            else:
                # No overlap
                updated_slots.append(slot)
        self.calendar[date_key] = updated_slots
        logger.debug(f"Updated availability for {date_key}: {len(updated_slots)} slots")

    def get_next_available_slot(self, start_datetime: datetime, min_duration: timedelta) -> Optional[Dict[str, datetime]]:
        current_date = start_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
        logger.debug(f"Searching for next available slot from {start_datetime} with duration {min_duration}")
        
        while current_date in self.calendar:
            logger.debug(f"Checking date: {current_date}")
            for slot in self.calendar[current_date]:
                if slot.available:
                    start = max(slot.start_time, start_datetime)
                    if slot.end_time - start >= min_duration:
                        logger.debug(f"Found slot: {start} - {start + min_duration}")
                        return {'start': start, 'end': start + min_duration}
            
            logger.debug(f"No available slot found for {current_date}, moving to next day")
            current_date = get_next_working_day(current_date)
            start_datetime = current_date.replace(hour=WORK_START_TIME_OBJ.hour, minute=WORK_START_TIME_OBJ.minute)

        logger.debug("No available slot found within scheduling period")
        return None

def is_overlapping(start1: datetime, end1: datetime, start2: datetime, end2: datetime) -> bool:
    return start1 < end2 and end1 > start2

def split_availability_slot(slot: ContractorAvailabilitySlot, errand_start: datetime, errand_end: datetime) -> List[ContractorAvailabilitySlot]:
    new_slots = []
    if slot.start_time < errand_start:  # Slot before the errand
        new_slots.append(ContractorAvailabilitySlot(slot.start_time, errand_start))
    if errand_end < slot.end_time:  # Slot after the errand
        new_slots.append(ContractorAvailabilitySlot(errand_end, slot.end_time))
    return new_slots