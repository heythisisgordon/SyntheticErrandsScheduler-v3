from typing import List, Tuple, Any
from managers.config_manager import ConfigManager

class ProblemDefinitionManager:
    """
    Manages problem definition parameters and calculations.
    This class handles retrieving and updating problem parameters,
    calculating costs, and preparing configuration updates.
    """

    def __init__(self):
        self.config_manager = ConfigManager()

    def apply_config_update(self, updated_config: List[Tuple[str, Any]], save_to_file: bool) -> None:
        config_dict = dict(updated_config)
        self.config_manager.update(config_dict)
        if save_to_file:
            self.config_manager.save()

    def prepare_config_update(self, num_customers: int, num_contractors: int, contractor_rate: float, errand_params: List[Tuple[str, List[Tuple[str, float]]]]) -> List[Tuple[str, Any]]:
        updated_config = [
            ('num_customers', num_customers),
            ('num_contractors', num_contractors),
            ('contractor_rate', contractor_rate)
        ]

        errand_types = []
        for errand_type, params in errand_params:
            errand_config = {
                'name': errand_type,
                'base_time': next(param[1] for param in params if param[0] == 'base_time'),
                'incentive': next(param[1] for param in params if param[0] == 'incentive'),
                'disincentive': {
                    'type': 'percentage',
                    'value': next(param[1] for param in params if param[0] == 'disincentive'),
                    'days': 14  # Assuming it's always 14 days
                }
            }
            errand_types.append(errand_config)

        updated_config.append(('errand_types', errand_types))

        return updated_config
