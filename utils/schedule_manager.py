from typing import List, Tuple
from models.customer import Customer
from models.contractor import Contractor
from models.schedule import Schedule
from models.contractor_calendar import ContractorCalendar
from algorithms.initial_greedy_scheduler import initial_greedy_schedule, InitialSchedulingError
import logging

logger = logging.getLogger(__name__)

class ScheduleManager:
    @staticmethod
    def generate_greedy_schedule(customers: List[Customer], contractors: List[Contractor]) -> Tuple[Schedule, str]:
        try:
            contractor_calendars = {contractor.id: contractor.calendar for contractor in contractors}
            
            if not contractor_calendars:
                raise ValueError("Failed to initialize contractor calendars.")
            
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
