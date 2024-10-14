from datetime import datetime, timedelta
from typing import List, Tuple, Optional
from constants import SCHEDULING_DAYS, WORK_START_TIME_OBJ, WORK_END_TIME_OBJ
from utils.time_utils import is_time_within_range, get_next_working_day
import logging

logger = logging.getLogger(__name__)

class ContractorAvailabilitySlot:
    def __init__(self, start_time: datetime, end_time: datetime):
        self.start_time = start_time
        self.end_time = end_time
        self.available = True

class ErrandAssignment:
    def __init__(self, errand_id: str, errand_type: str, travel_start_time: datetime, travel_end_time: datetime, 
                 task_start_time: datetime, task_end_time: datetime, travel_duration: timedelta, total_duration: timedelta):
        self.errand_id = errand_id
        self.errand_type = errand_type
        self.travel_start_time = travel_start_time
        self.travel_end_time = travel_end_time
        self.task_start_time = task_start_time
        self.task_end_time = task_end_time
        self.travel_duration = travel_duration
        self.total_duration = total_duration

class ContractorCalendar:
    def __init__(self):
        self.calendar: List[Tuple[datetime, List[ContractorAvailabilitySlot]]] = []
        self.errands: List[Tuple[datetime, List[ErrandAssignment]]] = []
        self.start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        self._initialize_calendar()

    def _initialize_calendar(self):
        for day in range(SCHEDULING_DAYS):
            current_date = self.start_date + timedelta(days=day)
            work_start = current_date.replace(hour=WORK_START_TIME_OBJ.hour, minute=WORK_START_TIME_OBJ.minute)
            work_end = current_date.replace(hour=WORK_END_TIME_OBJ.hour, minute=WORK_END_TIME_OBJ.minute)
            self.calendar.append((current_date, [ContractorAvailabilitySlot(work_start, work_end)]))
            self.errands.append((current_date, []))
        logger.debug(f"Calendar initialized for {SCHEDULING_DAYS} days starting from {self.start_date}")

    def is_available(self, start_time: datetime, end_time: datetime) -> bool:
        date_key = start_time.replace(hour=0, minute=0, second=0, microsecond=0)
        
        calendar_entry = next((entry for entry in self.calendar if entry[0] == date_key), None)
        if not calendar_entry:
            logger.debug(f"Date {date_key} is outside the initialized range")
            return False
        
        if not is_time_within_range(start_time.time(), WORK_START_TIME_OBJ, WORK_END_TIME_OBJ) or \
           not is_time_within_range(end_time.time(), WORK_START_TIME_OBJ, WORK_END_TIME_OBJ):
            logger.debug(f"Time slot {start_time} - {end_time} is outside working hours")
            return False
        
        for slot in calendar_entry[1]:
            if slot.available and slot.start_time <= start_time and slot.end_time >= end_time:
                logger.debug(f"Available slot found: {slot.start_time} - {slot.end_time}")
                return True
        logger.debug(f"No available slot found for {start_time} - {end_time}")
        return False

    def reserve_time_slot(self, errand_id: str, errand_type: str, travel_start_time: datetime, travel_end_time: datetime, 
                          task_start_time: datetime, task_end_time: datetime) -> bool:
        if self.is_available(travel_start_time, task_end_time):
            date_key = travel_start_time.replace(hour=0, minute=0, second=0, microsecond=0)
            travel_duration = travel_end_time - travel_start_time
            total_duration = task_end_time - travel_start_time
            new_errand = ErrandAssignment(errand_id, errand_type, travel_start_time, travel_end_time, 
                                          task_start_time, task_end_time, travel_duration, total_duration)
            errand_entry = next(entry for entry in self.errands if entry[0] == date_key)
            errand_entry[1].append(new_errand)
            self._update_availability(date_key, travel_start_time, task_end_time)
            logger.info(f"Reserved time slot for errand {errand_id}: {travel_start_time} - {task_end_time}")
            return True
        logger.warning(f"Failed to reserve time slot for errand {errand_id}: {travel_start_time} - {task_end_time}")
        return False

    def _update_availability(self, date_key: datetime, start_time: datetime, end_time: datetime):
        calendar_entry = next(entry for entry in self.calendar if entry[0] == date_key)
        updated_slots = []
        for slot in calendar_entry[1]:
            if not slot.available:
                updated_slots.append(slot)
                continue

            if start_time >= slot.end_time or end_time <= slot.start_time:
                # No overlap
                updated_slots.append(slot)
            elif start_time <= slot.start_time and end_time >= slot.end_time:
                # Errand fully covers the slot
                continue
            else:
                # Partial overlap
                if slot.start_time < start_time:
                    updated_slots.append(ContractorAvailabilitySlot(slot.start_time, start_time))
                if end_time < slot.end_time:
                    updated_slots.append(ContractorAvailabilitySlot(end_time, slot.end_time))

        # Update the calendar entry with the new list of slots
        calendar_index = next(i for i, entry in enumerate(self.calendar) if entry[0] == date_key)
        self.calendar[calendar_index] = (date_key, updated_slots)
        logger.debug(f"Updated availability for {date_key}: {len(updated_slots)} slots")

    def get_next_available_slot(self, start_datetime: datetime, min_duration: timedelta) -> Optional[dict]:
        current_date = start_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
        logger.debug(f"Searching for next available slot from {start_datetime} with duration {min_duration}")
        
        for calendar_entry in self.calendar:
            if calendar_entry[0] >= current_date:
                logger.debug(f"Checking date: {calendar_entry[0]}")
                for slot in calendar_entry[1]:
                    if slot.available:
                        start = max(slot.start_time, start_datetime)
                        if slot.end_time - start >= min_duration:
                            end = start + min_duration
                            if self.is_available(start, end):
                                logger.debug(f"Found valid slot: {start} - {end}")
                                return {'start': start, 'end': end}
                        else:
                            logger.debug(f"Slot {slot.start_time} - {slot.end_time} is too short for duration {min_duration}")
                    else:
                        logger.debug(f"Slot {slot.start_time} - {slot.end_time} is not available")
                
                logger.debug(f"No available slot found for {calendar_entry[0]}, moving to next day")
                current_date = get_next_working_day(calendar_entry[0])
                start_datetime = current_date.replace(hour=WORK_START_TIME_OBJ.hour, minute=WORK_START_TIME_OBJ.minute)

        logger.debug("No available slot found within scheduling period")
        return None

def is_overlapping(start1: datetime, end1: datetime, start2: datetime, end2: datetime) -> bool:
    return start1 < end2 and end1 > start2
