"""
GreedySolutionController: Manages the generation and display of greedy solutions for the scheduling problem.
"""

from typing import List
from models.customer import Customer
from models.contractor import Contractor
from models.schedule import Schedule
from utils.greedy_solution_manager import GreedySolutionManager
from utils.schedule_formatter import ScheduleFormatter
from utils.event_manager import EventManager

class GreedySolutionController:
    def __init__(self, greedy_solution_tab, event_manager: EventManager):
        self.greedy_solution_tab = greedy_solution_tab
        self.event_manager = event_manager
        self.greedy_solution_manager = GreedySolutionManager()
        self.schedule_formatter = ScheduleFormatter()

    def on_generate_solution(self, customers: List[Customer], contractors: List[Contractor]):
        try:
            schedule, message = self.greedy_solution_manager.generate_solution(customers, contractors)
            if schedule:
                profit = self.greedy_solution_manager.calculate_profit(schedule)
                formatted_schedule = self.schedule_formatter.format_schedule(customers, contractors, schedule)
                
                self.greedy_solution_tab.display_solution(formatted_schedule, profit)
                self.event_manager.emit(EventManager.SOLUTION_GENERATED, {'schedule': schedule, 'profit': profit})
                
                if message:
                    self.greedy_solution_tab.show_warning(message)
            else:
                self.greedy_solution_tab.show_error(f"Failed to generate solution: {message}")
        except Exception as e:
            self.greedy_solution_tab.show_error(str(e))

    def on_visualize_solution(self, customers: List[Customer], contractors: List[Contractor], schedule: Schedule):
        try:
            self.greedy_solution_tab.visualize_solution(customers, contractors, schedule)
        except Exception as e:
            self.greedy_solution_tab.show_error(str(e))
