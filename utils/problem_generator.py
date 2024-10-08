"""
Problem generator module for the Synthetic Errands Scheduler

This module contains functions for generating random problem instances
with customers and contractors.
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
    """
    Generate a random problem instance with customers and contractors.

    Args:
        num_customers (int): Number of customers to generate. Defaults to DEFAULT_NUM_CUSTOMERS.
        num_contractors (int): Number of contractors to generate. Defaults to DEFAULT_NUM_CONTRACTORS.
        contractor_rate (float): The rate per minute for contractors. Defaults to 0.5.

    Returns:
        Tuple[List[Customer], List[Contractor]]: Lists of generated customers and contractors.

    Raises:
        ProblemGenerationError: If there's an error during problem generation.
    """
    try:
        customers: List[Customer] = []
        contractors: List[Contractor] = []

        logger.info(f"Generating problem with {num_customers} customers and {num_contractors} contractors")

        start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        # Generate customers
        for i in range(num_customers):
            # Generate random valid road location
            for _ in range(100):  # Limit attempts to find valid location
                x = random.randint(0, GRID_SIZE - 1)
                y = random.randint(0, GRID_SIZE - 1)
                if is_valid_road_location(x, y):
                    break
            else:
                raise ProblemGenerationError(f"Failed to find valid road location for customer {i}")

            # Randomly assign desired errand
            errand_type, base_time, incentive, disincentive = random.choice(ERRAND_TYPES)
            errand = Errand(i, errand_type, timedelta(minutes=base_time), incentive, disincentive)

            # Generate full-day availability for all scheduling days
            availability: Dict[datetime, List[Tuple[datetime, datetime]]] = {}
            for day in range(SCHEDULING_DAYS):
                current_date = start_date + timedelta(days=day)
                availability[current_date] = [
                    (
                        datetime.combine(current_date, WORK_START_TIME_OBJ),
                        datetime.combine(current_date, WORK_END_TIME_OBJ)
                    )
                ]

            customer = Customer(i, (x, y), errand, availability)
            customers.append(customer)
            logger.debug(f"Generated customer {i} at location {(x, y)} with errand {errand_type.name}")

        # Generate contractors
        for i in range(num_contractors):
            # Generate random valid road location
            for _ in range(100):  # Limit attempts to find valid location
                x = random.randint(0, GRID_SIZE - 1)
                y = random.randint(0, GRID_SIZE - 1)
                if is_valid_road_location(x, y):
                    break
            else:
                raise ProblemGenerationError(f"Failed to find valid road location for contractor {i}")

            contractor = Contractor(i, (x, y), contractor_rate)
            contractors.append(contractor)
            logger.debug(f"Generated contractor {i} at location {(x, y)} with rate ${contractor_rate:.2f}/minute")

        return customers, contractors
    except Exception as e:
        logger.error(f"Error during problem generation: {str(e)}")
        raise ProblemGenerationError(f"Failed to generate problem: {str(e)}")