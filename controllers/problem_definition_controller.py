"""
ProblemDefinitionController: Manages the problem definition process, including parameter updates and cost calculations.
"""

from typing import List, Tuple
from managers.problem_definition_manager import ProblemDefinitionManager
from managers.event_manager import EventManager

class ProblemDefinitionController:
    def __init__(self, problem_definition_tab, event_manager: EventManager):
        self.problem_definition_tab = problem_definition_tab
        self.event_manager = event_manager
        self.problem_definition_manager = ProblemDefinitionManager()

# Need to update these to so that problem definition buttons work properly
    def on_update_config(self, num_customers: int, num_contractors: int, contractor_rate: float, errand_params: List[Tuple[str, List[Tuple[str, float]]]], save_to_file: bool):
        try:
            updated_config = self.problem_definition_manager.prepare_config_update(
                num_customers, num_contractors, contractor_rate, errand_params
            )
            self.problem_definition_manager.apply_config_update(updated_config, save_to_file)
            self.event_manager.emit(EventManager.PROBLEM_DEFINED)
        except ValueError as e:
            self.problem_definition_tab.show_error(str(e))

    def on_commit_changes(self, save_to_file: bool):
        self.on_update_config(
            self.problem_definition_tab.get_num_customers(),
            self.problem_definition_tab.get_num_contractors(),
            self.problem_definition_tab.get_contractor_rate(),
            self.problem_definition_tab.get_errand_params(),
            save_to_file
        )
