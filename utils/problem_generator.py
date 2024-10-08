"""
Problem generator module for the Synthetic Errands Scheduler.
Generates random problem instances with customers and contractors.
"""

import random
import logging
from typing import List, Tuple, Dict
from datetime import datetime, timedelta

from models.customer import Customer
from models.contractor import Contractor
from models.errand import Errand
from utils.city_map import is_valid_road_location, GRID_SIZE
from constants import ERRAND_TYPES, DEFAULT_NUM_CUSTOMERS, DEFAULT_NUM_CONTRACTORS, SCHEDULING_DAYS, WORK_START_TIME_OBJ, WORK_END_TIME_OBJ

logger: logging.Logger = logging.getLogger(__name__)

class ProblemGenerationError(Exception):
    """Custom exception for errors during problem generation."""
    pass

def generate_problem(num_customers: int = DEFAULT_NUM_CUSTOMERS, num_contractors: int = DEFAULT_NUM_CONTRACTORS, contractor_rate: float = 0.5) -> Tuple[List[Customer], List[Contractor]]:
    """Generate a random problem instance with customers and contractors."""
    try:
        start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        customers = [_generate_customer(i, start_date) for i in range(num_customers)]
        contractors = [_generate_contractor(i, contractor_rate) for i in range(num_contractors)]
        
        logger.info(f"Generated problem with {num_customers} customers and {num_contractors} contractors")
        return customers, contractors
    except Exception as e:
        logger.error(f"Error during problem generation: {str(e)}")
        raise ProblemGenerationError(f"Failed to generate problem: {str(e)}")

def _generate_customer(customer_id: int, start_date: datetime) -> Customer:
    """Generate a single customer with random attributes."""
    return Customer(
        customer_id,
        _generate_valid_location(),
        _generate_random_errand(customer_id),
        _generate_full_day_availability(start_date)
    )

def _generate_contractor(contractor_id: int, rate: float) -> Contractor:
    """Generate a single contractor with random attributes."""
    return Contractor(contractor_id, _generate_valid_location(), rate)

def _generate_valid_location() -> Tuple[int, int]:
    """Generate a random valid road location."""
    for _ in range(100):  # Limit attempts to find valid location
        x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        if is_valid_road_location(x, y):
            return x, y
    raise ProblemGenerationError("Failed to find valid road location")

def _generate_random_errand(errand_id: int) -> Errand:
    """Generate a random errand."""
    errand_type, base_time, incentive, disincentive = random.choice(ERRAND_TYPES)
    return Errand(errand_id, errand_type, timedelta(minutes=base_time), incentive, disincentive)

def _generate_full_day_availability(start_date: datetime) -> Dict[datetime, List[Tuple[datetime, datetime]]]:
    """Generate full-day availability for all scheduling days."""
    return {
        start_date + timedelta(days=day): [
            (
                datetime.combine(start_date + timedelta(days=day), WORK_START_TIME_OBJ),
                datetime.combine(start_date + timedelta(days=day), WORK_END_TIME_OBJ)
            )
        ]
        for day in range(SCHEDULING_DAYS)
    }