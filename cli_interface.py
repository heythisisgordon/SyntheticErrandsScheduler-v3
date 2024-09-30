"""
CLI interface module for the Synthetic Errands Scheduler

This module contains functions for running the Synthetic Errands Scheduler in CLI mode.
It handles problem generation, scheduling, optimization, and result presentation.
"""

import logging
import sys
from typing import List, Optional

from models.customer import Customer
from models.contractor import Contractor
from models.schedule import Schedule
from algorithms.initial_greedy_scheduler import initial_greedy_schedule
from algorithms.CP_SAT_optimizer import optimize_schedule
from algorithms.vehicle_routing_optimizer import optimize_schedule_vrp
from utils.visualization import visualize_schedule, print_schedule
from utils.problem_generator import generate_problem, ProblemGenerationError

logger: logging.Logger = logging.getLogger(__name__)

class SchedulingError(Exception):
    """Custom exception for errors during scheduling."""
    pass

def cli_main(optimizer: str) -> None:
    """
    Main function for CLI mode.

    Args:
        optimizer (str): The chosen optimizer ('cp-sat' or 'vrp')
    """
    try:
        logger.info("Starting Synthetic Errands Scheduler in CLI mode")
        logger.info(f"Selected optimizer: {optimizer}")

        customers, contractors = generate_problem()
        logger.info(f"Generated {len(customers)} customers and {len(contractors)} contractors")

        logger.info("Customer Details:")
        for customer in customers:
            logger.info(f"Customer {customer.id}: Location {customer.location}, Errand: {customer.desired_errand.type.name}")

        logger.info("Contractor Details:")
        for contractor in contractors:
            logger.info(f"Contractor {contractor.id}: Location {contractor.location}")

        initial_sched: Optional[Schedule] = initial_greedy_schedule(customers, contractors)
        if not initial_sched:
            raise SchedulingError("Failed to create initial greedy schedule")
        
        logger.info("Initial greedy schedule created")
        print_schedule(initial_sched)
        visualize_schedule(initial_sched, "initial_greedy_schedule.png")

        # Print some basic information about the initial schedule
        initial_profit: float = initial_sched.calculate_total_profit()
        logger.info(f"Initial greedy schedule - Profit: ${initial_profit:.2f}")

        # Optimize the schedule
        if optimizer == "cp-sat":
            optimized_sched: Optional[Schedule] = optimize_schedule(initial_sched)
        elif optimizer == "vrp":
            optimized_sched: Optional[Schedule] = optimize_schedule_vrp(initial_sched)
        else:
            raise ValueError(f"Unknown optimizer: {optimizer}")

        if not optimized_sched:
            raise SchedulingError("Failed to optimize schedule")
        
        logger.info("Schedule optimized")
        print_schedule(optimized_sched)
        visualize_schedule(optimized_sched, "optimized_schedule.png")

        # Print information about the optimized schedule
        optimized_profit: float = optimized_sched.calculate_total_profit()
        logger.info(f"Optimized schedule - Profit: ${optimized_profit:.2f}")

        profit_improvement: float = optimized_profit - initial_profit
        logger.info(f"Profit improvement: ${profit_improvement:.2f}")

        # Compare the schedules
        compare_schedules(initial_sched, optimized_sched)

    except ProblemGenerationError as e:
        logger.error(f"Problem generation failed: {str(e)}")
        sys.exit(1)
    except SchedulingError as e:
        logger.error(f"Scheduling failed: {str(e)}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    cli_main("cp-sat")  # Default to CP-SAT optimizer when run directly