from typing import Tuple, Optional, Dict, List
import pandas as pd
from constants import WORK_START_TIME_OBJ, WORK_END_TIME_OBJ, TIME_BLOCKS
from utils.scheduling_utils import SchedulingUtilities
import logging

logger = logging.getLogger(__name__)

class ErrandAssignment:
    def __init__(self, errand_id: str, errand_type: str, travel_start_time: pd.Timestamp, travel_end_time: pd.Timestamp, 
                 task_start_time: pd.Timestamp, task_end_time: pd.Timestamp, travel_duration: pd.Timedelta, total_duration: pd.Timedelta):
        self.errand_id = errand_id
        self.errand_type = errand_type
        self.travel_start_time = travel_start_time
        self.travel_end_time = travel_end_time
        self.task_start_time = task_start_time
        self.task_end_time = task_end_time
        self.travel_duration = travel_duration
        self.total_duration = total_duration

class ContractorCalendar:
    def __init__(self, schedule: pd.DataFrame):
        self.schedule = schedule

    def is_available(self, start_time: pd.Timestamp, end_time: pd.Timestamp) -> bool:
        return SchedulingUtilities.is_valid_assignment(self, None, start_time, end_time)

    def reserve_time_slot(self, errand_id: str, errand_type: str, travel_start_time: pd.Timestamp, travel_end_time: pd.Timestamp, 
                          task_start_time: pd.Timestamp, task_end_time: pd.Timestamp) -> bool:
        self.expand_schedule(task_end_time)
        if self.is_available(travel_start_time, task_end_time):
            mask = (self.schedule.index.get_level_values('Date') >= travel_start_time.floor('D')) & \
                   (self.schedule.index.get_level_values('Date') <= task_end_time.floor('D')) & \
                   (
                       ((self.schedule.index.get_level_values('Date') == travel_start_time.floor('D')) & (self.schedule.index.get_level_values('Time') >= travel_start_time.time())) |
                       ((self.schedule.index.get_level_values('Date') == task_end_time.floor('D')) & (self.schedule.index.get_level_values('Time') < task_end_time.time())) |
                       ((self.schedule.index.get_level_values('Date') > travel_start_time.floor('D')) & (self.schedule.index.get_level_values('Date') < task_end_time.floor('D')))
                   )
            self.schedule.loc[mask, 'Client_ID'] = errand_id
            logger.info(f"Reserved time slot for errand {errand_id}: {travel_start_time} - {task_end_time}")
            return True
        logger.warning(f"Failed to reserve time slot for errand {errand_id}: {travel_start_time} - {task_end_time}")
        return False

    def get_next_available_slot(self, start_datetime: pd.Timestamp, min_duration: pd.Timedelta) -> Optional[Dict[str, pd.Timestamp]]:
        logger.debug(f"Searching for next available slot from {start_datetime} with duration {min_duration}")
        
        end_datetime = self.schedule.index.get_level_values('Date').max()
        current_datetime = max(start_datetime, self.schedule.index.get_level_values('Date').min())
        
        while current_datetime < end_datetime:
            if self.is_available(current_datetime, current_datetime + min_duration):
                logger.debug(f"Found valid slot: {current_datetime} - {current_datetime + min_duration}")
                return {'start': current_datetime, 'end': current_datetime + min_duration}
            
            current_datetime += pd.Timedelta(minutes=TIME_BLOCKS)
        
        logger.debug("No available slot found within scheduling period")
        return None

    def expand_schedule(self, new_datetime: pd.Timestamp):
        if new_datetime > self.schedule.index.get_level_values('Date').max():
            new_end = pd.Timestamp.combine(new_datetime.date(), WORK_END_TIME_OBJ)
            new_range = pd.date_range(start=self.schedule.index.get_level_values('Date').max() + pd.Timedelta(days=1), 
                                      end=new_end, 
                                      freq=f'{TIME_BLOCKS}min')
            new_schedule = pd.DataFrame(index=pd.MultiIndex.from_product([new_range.date, new_range.time], names=['Date', 'Time']), columns=['Client_ID'])
            new_schedule['Client_ID'] = None
            self.schedule = pd.concat([self.schedule, new_schedule]).sort_index()

def is_overlapping(start1: pd.Timestamp, end1: pd.Timestamp, start2: pd.Timestamp, end2: pd.Timestamp) -> bool:
    return start1 < end2 and end1 > start2
