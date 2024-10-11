from typing import Dict, List
from utils.config_manager import ConfigManager

class ProblemDefinitionManager:
    def __init__(self):
        self.config_manager = ConfigManager()

    def get_problem_params(self) -> Dict[str, float]:
        return {
            'num_customers': self.config_manager.get('num_customers', 10),
            'num_contractors': self.config_manager.get('num_contractors', 2),
            'contractor_rate': self.config_manager.get('contractor_rate', 0.50)
        }

    def get_errand_params(self) -> List[Dict]:
        return self.config_manager.get('errand_types', [])

    def calculate_costs(self, errand_params: Dict[str, Dict[str, float]], contractor_rate: float) -> Dict[str, Dict[str, float]]:
        costs = {}
        for errand_type, params in errand_params.items():
            base_time = params['base_time']
            incentive = params['incentive']

            base_cost = base_time * contractor_rate
            max_cost = base_cost * incentive

            costs[errand_type] = {
                'base_cost': base_cost,
                'max_cost': max_cost
            }

        return costs

    def calculate_total_costs(self, costs: Dict[str, Dict[str, float]]) -> Dict[str, float]:
        total_base_cost = sum(cost['base_cost'] for cost in costs.values())
        total_max_cost = sum(cost['max_cost'] for cost in costs.values())

        return {
            'total_base_cost': total_base_cost,
            'total_max_cost': total_max_cost
        }

    def update_config(self, updated_config: Dict, save_to_file: bool) -> None:
        self.config_manager.update(updated_config)
        if save_to_file:
            self.config_manager.save()

    def prepare_config_update(self, num_customers: int, num_contractors: int, contractor_rate: float, errand_params: Dict[str, Dict[str, float]]) -> Dict:
        updated_config = {
            'num_customers': num_customers,
            'num_contractors': num_contractors,
            'contractor_rate': contractor_rate
        }

        errand_types = []
        for errand_type, params in errand_params.items():
            errand_config = {
                'name': errand_type,
                'base_time': params['base_time'],
                'incentive': params['incentive'],
                'disincentive': {
                    'type': 'percentage',
                    'value': params['disincentive'],
                    'days': 14  # Assuming it's always 14 days
                }
            }
            errand_types.append(errand_config)

        updated_config['errand_types'] = errand_types

        return updated_config
