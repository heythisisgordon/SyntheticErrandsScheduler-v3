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
        
        return ScheduleManager.generate_greedy_schedule(customers, contractors)

    @staticmethod
    def calculate_profit(schedule: Schedule) -> float:
        return ScheduleManager.calculate_total_profit(schedule)
