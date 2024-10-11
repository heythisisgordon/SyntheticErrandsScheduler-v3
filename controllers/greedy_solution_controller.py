from typing import List, Tuple
from models.customer import Customer
from models.contractor import Contractor
from models.schedule import Schedule
from utils.greedy_solution_manager import GreedySolutionManager
from utils.schedule_formatter import ScheduleFormatter

class GreedySolutionController:
    @staticmethod
    def generate_solution(customers: List[Customer], contractors: List[Contractor]) -> Tuple[Schedule, str]:
        return GreedySolutionManager.generate_solution(customers, contractors)

    @staticmethod
    def format_schedule(customers: List[Customer], contractors: List[Contractor], schedule: Schedule) -> List[str]:
        return ScheduleFormatter.format_schedule(customers, contractors, schedule)

    @staticmethod
    def calculate_profit(schedule: Schedule) -> float:
        return GreedySolutionManager.calculate_profit(schedule)
