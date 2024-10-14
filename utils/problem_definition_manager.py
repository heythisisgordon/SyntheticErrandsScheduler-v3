from typing import List, Tuple, Any
from utils.config_manager import ConfigManager

class ProblemDefinitionManager:
    """
    Manages problem definition parameters and calculations.
    This class handles retrieving and updating problem parameters,
    calculating costs, and preparing configuration updates.
    """

    def __init__(self):
        self.config_manager = ConfigManager()

    def get_problem_params(self) -> List[Tuple[str, float]]:
        return [
            ('num_customers', self.config_manager.get('num_customers', 10)),
            ('num_contractors', self.config_manager.get('num_contractors', 2)),
            ('contractor_rate', self.config_manager.get('contractor_rate', 0.50))
        ]

    def get_errand_params(self) -> List[Tuple[str, List[Tuple[str, float]]]]:
        errand_types = self.config_manager.get('errand_types', [])
        return [(errand['name'], [
            ('base_time', errand['base_time']),
            ('incentive', errand['incentive']),
            ('disincentive', errand['disincentive']['value'])
        ]) for errand in errand_types]

    def calculate_costs(self, errand_params: List[Tuple[str, List[Tuple[str, float]]]], contractor_rate: float) -> List[Tuple[str, List[Tuple[str, float]]]]:
        costs = []
        for errand_type, params in errand_params:
            base_time = next(param[1] for param in params if param[0] == 'base_time')
            incentive = next(param[1] for param in params if param[0] == 'incentive')

            base_cost = base_time * contractor_rate
            max_cost = base_cost * incentive

            costs.append((errand_type, [
                ('base_cost', base_cost),
                ('max_cost', max_cost)
            ]))

        return costs

    def calculate_total_costs(self, costs: List[Tuple[str, List[Tuple[str, float]]]]) -> List[Tuple[str, float]]:
        total_base_cost = sum(next(cost[1] for cost in errand_costs if cost[0] == 'base_cost') for _, errand_costs in costs)
        total_max_cost = sum(next(cost[1] for cost in errand_costs if cost[0] == 'max_cost') for _, errand_costs in costs)

        return [
            ('total_base_cost', total_base_cost),
            ('total_max_cost', total_max_cost)
        ]

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
