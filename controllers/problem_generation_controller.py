"""
ProblemGenerationController: Handles the generation of problem instances based on defined parameters.
"""

from typing import List, Tuple
from models.customer import Customer
from models.contractor import Contractor
from utils.problem_generator import generate_problem
from utils.event_manager import EventManager
from utils.formatting_utils import FormattingUtils

class ProblemGenerationController:
    def __init__(self, problem_generation_tab, event_manager: EventManager):
        self.problem_generation_tab = problem_generation_tab
        self.event_manager = event_manager
        self.current_problem: Tuple[List[Customer], List[Contractor]] = None

    def on_generate_problem(self, event):
        try:
            num_customers, num_contractors, contractor_rate = self.problem_generation_tab.get_problem_params()
            self.current_problem = generate_problem(num_customers, num_contractors, contractor_rate)
            customers, contractors = self.current_problem
            
            self.update_ui_with_problem(customers, contractors, contractor_rate)
            self.event_manager.emit(EventManager.PROBLEM_GENERATED, {'customers': customers, 'contractors': contractors})
        except ValueError as e:
            self.problem_generation_tab.show_error(str(e))

    def update_ui_with_problem(self, customers: List[Customer], contractors: List[Contractor], contractor_rate: float):
        customer_info = [FormattingUtils.format_customer_info(customer) for customer in customers]
        contractor_info = [FormattingUtils.format_contractor_info(contractor) for contractor in contractors]
        contractor_rate_info = FormattingUtils.format_contractor_rate(contractor_rate)

        self.problem_generation_tab.display_problem(customer_info, contractor_info, contractor_rate_info)

    def on_visualize_problem(self):
        if self.current_problem:
            customers, contractors = self.current_problem
            self.problem_generation_tab.visualize_problem(customers, contractors)
        else:
            self.problem_generation_tab.show_error("No problem has been generated yet.")

    def set_problem_params(self, num_customers: int, num_contractors: int, contractor_rate: float):
        self.problem_generation_tab.set_problem_params(num_customers, num_contractors, contractor_rate)
