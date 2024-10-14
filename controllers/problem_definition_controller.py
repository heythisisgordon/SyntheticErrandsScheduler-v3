from typing import List, Tuple
from utils.problem_definition_manager import ProblemDefinitionManager

class ProblemDefinitionController:
    def __init__(self):
        self.problem_definition_manager = ProblemDefinitionManager()

    def get_problem_params(self) -> List[Tuple[str, float]]:
        return self.problem_definition_manager.get_problem_params()

    def get_errand_params(self) -> List[Tuple[str, List[Tuple[str, float]]]]:
        return self.problem_definition_manager.get_errand_params()

    def calculate_costs(self, errand_params: List[Tuple[str, List[Tuple[str, float]]]], contractor_rate: float):
        costs = self.problem_definition_manager.calculate_costs(errand_params, contractor_rate)
        total_costs = self.problem_definition_manager.calculate_total_costs(costs)
        return costs, total_costs

    def update_config(self, num_customers: int, num_contractors: int, contractor_rate: float, errand_params: List[Tuple[str, List[Tuple[str, float]]]], save_to_file: bool):
        updated_config = self.problem_definition_manager.prepare_config_update(
            num_customers, num_contractors, contractor_rate, errand_params
        )
        self.problem_definition_manager.update_config(updated_config, save_to_file)
