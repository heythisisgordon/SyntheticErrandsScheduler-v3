from typing import List, Tuple
from models.customer import Customer
from models.contractor import Contractor
from models.schedule import Schedule
from algorithms.initial_greedy_scheduler import initial_greedy_schedule, InitialSchedulingError
import logging
import pandas as pd
from constants import SCHEDULING_DAYS, WORK_START_TIME_OBJ, WORK_END_TIME_OBJ, TIME_BLOCKS

logger = logging.getLogger(__name__)

class ScheduleManager:
    @staticmethod
    def generate_greedy_schedule(customers: List[Customer], contractors: List[Contractor]) -> Tuple[Schedule, str]:
        try:
            # Initialize contractor schedules using the new method
            for contractor in contractors:
                contractor.initialize_schedule(ScheduleManager)
            
            schedule = initial_greedy_schedule(customers, contractors)
            
            total_assignments = len(schedule.get_assignments())
            logger.info(f"Total assignments made: {total_assignments}")
            logger.info(f"Total customers: {len(customers)}")
            logger.info(f"Unscheduled customers: {len(customers) - total_assignments}")
            
            if total_assignments == 0:
                return schedule, "No assignments were made in the greedy solution"
            elif total_assignments < len(customers):
                return schedule, f"Only {total_assignments} out of {len(customers)} customers were scheduled"
            
            return schedule, ""
            
        except (InitialSchedulingError, ValueError) as e:
            logger.error(f"Failed to generate greedy solution: {str(e)}")
            return None, str(e)

    @staticmethod
    def calculate_total_profit(schedule: Schedule) -> float:
        return schedule.calculate_total_profit()

    @staticmethod
    def generate_empty_schedule() -> pd.DataFrame:
        start_date = pd.Timestamp.now().floor('D')
        end_date = start_date + pd.Timedelta(days=SCHEDULING_DAYS - 1)  # Subtract 1 to include the start date
        
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        time_range = pd.date_range(
            start=pd.Timestamp.combine(start_date, WORK_START_TIME_OBJ.time()),
            end=pd.Timestamp.combine(start_date, WORK_END_TIME_OBJ.time()),
            freq=f'{TIME_BLOCKS}min'
        ).time
        
        index = pd.MultiIndex.from_product([date_range, time_range], names=['Date', 'Time'])
        
        schedule = pd.DataFrame(index=index, columns=['Client_ID'])
        schedule['Client_ID'] = None
        
        logger.info(f"Generated empty schedule from {start_date.date()} to {end_date.date()}")
        return schedule
