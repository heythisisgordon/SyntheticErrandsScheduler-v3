from typing import Dict
from utils.problem_definition_manager import ProblemDefinitionManager

class ProblemDefinitionController:
    def __init__(self):
        self.problem_definition_manager = ProblemDefinitionManager()

    def get_problem_params(self):
        return self.problem_definition_manager.get_problem_params()

    def get_errand_params(self):
        return self.problem_definition_manager.get_errand_params()

    def calculate_costs(self, errand_params: Dict[str, Dict[str, float]], contractor_rate: float):
        costs = self.problem_definition_manager.calculate_costs(errand_params, contractor_rate)
        total_costs = self.problem_definition_manager.calculate_total_costs(costs)
        return costs, total_costs

    def update_config(self, num_customers: int, num_contractors: int, contractor_rate: float, errand_params: Dict[str, Dict[str, float]], save_to_file: bool):
        updated_config = self.problem_definition_manager.prepare_config_update(
            num_customers, num_contractors, contractor_rate, errand_params
        )
        self.problem_definition_manager.update_config(updated_config, save_to_file)
