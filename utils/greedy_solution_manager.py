from typing import List, Tuple
from models.customer import Customer
from models.contractor import Contractor
from models.schedule import Schedule
from utils.schedule_manager import ScheduleManager
import logging

logger = logging.getLogger(__name__)

class GreedySolutionManager:
    @staticmethod
    def generate_solution(customers: List[Customer], contractors: List[Contractor]) -> Tuple[Schedule, str]:
        logger.info("Generating greedy solution")
        logger.debug(f"Number of customers: {len(customers)}")
        logger.debug(f"Number of contractors: {len(contractors)}")
        
        schedule, message = ScheduleManager.generate_greedy_schedule(customers, contractors)
        
        if schedule:
            total_assignments = len(schedule.get_assignments())
            logger.info(f"Total assignments made: {total_assignments}")
            logger.info(f"Total customers: {len(customers)}")
            logger.info(f"Unscheduled customers: {len(customers) - total_assignments}")
            
            if total_assignments == 0:
                message = "No assignments were made in the greedy solution"
            elif total_assignments < len(customers):
                message = f"Only {total_assignments} out of {len(customers)} customers were scheduled"
        
        return schedule, message

    @staticmethod
    def calculate_profit(schedule: Schedule) -> float:
        return schedule.calculate_total_profit()
