"""
Constants for the Synthetic Errands Scheduler

This module defines constants used throughout the application. It uses the
ConfigManager to load values from the config.yaml file, ensuring that all
constants are centralized and easily modifiable.

Usage:
    from constants import WORK_START_TIME_OBJ, ErrandType, ERRAND_TYPES

Note: This file should not be modified directly. To change any values,
update the config.yaml file instead.
"""

from utils.config_manager import config
from utils.time_utils import convert_minutes_to_time
from typing import List, Tuple, Dict, Union
from enum import Enum, auto
import datetime

class ErrandType(Enum):
    """
    Enum representing different types of errands.
    
    This enum is used to ensure type safety when working with errand types
    throughout the application.
    """
    DELIVERY = auto()
    DOG_WALK = auto()
    CUT_GRASS = auto()
    DETAIL_CAR = auto()
    OUTING = auto()
    MOVING = auto()
    GROCERY_SHOPPING = auto()

    @classmethod
    def from_string(cls, name: str) -> 'ErrandType':
        """
        Convert a string to an ErrandType enum value.
        
        Args:
            name (str): The name of the errand type.
        
        Returns:
            ErrandType: The corresponding ErrandType enum value.
        
        Raises:
            ValueError: If the input string doesn't match any ErrandType.
        """
        try:
            return cls[name.upper().replace(' ', '_')]
        except KeyError:
            raise ValueError(f"'{name}' is not a valid ErrandType")

# Maximum incentive multiplier
# This caps the maximum incentive that can be applied for same-day service.
MAX_INCENTIVE_MULTIPLIER: float = config.get('max_incentive_multiplier')

# Errand types with their characteristics
# Each tuple contains: (ErrandType, base_time, incentive, disincentive)
ERRAND_TYPES: List[Tuple[ErrandType, int, float, Union[Dict[str, Union[str, int]], None]]] = [
    (
        ErrandType.from_string(errand['name']),
        errand['base_time'],
        errand['incentive'],
        errand['disincentive']
    )
    for errand in config.get('errand_types')
]

# Errand rates ($ per minute)
ERRAND_RATES: Dict[ErrandType, float] = {
    ErrandType.from_string(name): rate
    for name, rate in config.get('errand_rates').items()
}

# Additional time for specific errand types (in minutes)
DELIVERY_ADDITIONAL_TIME: int = config.get('delivery_additional_time')

# Working hours
# These values define the start and end of the working day as datetime.time objects.
WORK_START_TIME_OBJ: datetime.time = convert_minutes_to_time(config.get('work_start_time'))
WORK_END_TIME_OBJ: datetime.time = convert_minutes_to_time(config.get('work_end_time'))

# Default problem generation parameters
# These values are used when generating random problem instances.
DEFAULT_NUM_CUSTOMERS: int = config.get('default_num_customers')
DEFAULT_NUM_CONTRACTORS: int = config.get('default_num_contractors')

# Scheduling period
# The number of days to schedule errands for.
SCHEDULING_DAYS: int = config.get('scheduling_days')

# Optimization parameters
# These parameters are used by the optimization algorithm.
OPTIMIZATION_MAX_TIME: int = config.get('optimization', {}).get('max_time_in_seconds', 60)
OPTIMIZATION_LOG_PROGRESS: bool = config.get('optimization', {}).get('log_search_progress', True)

# For backwards compatibility, define individual incentive constants
# Note: It's recommended to use ERRAND_TYPES instead of these individual constants
for errand in config.get('errand_types'):
    globals()[f"{errand['name'].upper().replace(' ', '_')}_INCENTIVE"] = errand['incentive']