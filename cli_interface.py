"""
CLI interface module for the Synthetic Errands Scheduler

This module contains functions for running the Synthetic Errands Scheduler in CLI mode.
It handles problem generation, scheduling, optimization, and result presentation.
"""

import logging
import sys
from typing import List, Optional
from datetime import datetime, timedelta

from models.customer import Customer
from models.contractor import Contractor
from models.schedule import Schedule
from models.master_contractor_calendar import MasterContractorCalendar
from algorithms.initial_greedy_scheduler import initial_greedy_schedule
from algorithms.CP_SAT_optimizer import optimize_schedule
from algorithms.vehicle_routing_optimizer import optimize_schedule_vrp
from utils.visualization import visualize_schedule, print_schedule
from utils.problem_generator import generate_problem, ProblemGenerationError
from constants import WORK_START_TIME_OBJ, WORK_END_TIME_OBJ

logger: logging.Logger = logging.getLogger(__name__)

class SchedulingError(Exception):
    """Custom exception for errors during scheduling."""
    pass

def print_contractor_calendars(master_calendar: MasterContractorCalendar, contractors: List[Contractor]) -> None:
    """
    Print the calendar information for each contractor using the MasterContractorCalendar.

    Args:
        master_calendar (MasterContractorCalendar): The master calendar containing all contractor calendars
        contractors (List[Contractor]): List of contractors
    """
    logger.info("Contractor Calendar Information:")
    start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    for contractor in contractors:
        logger.info(f"Contractor {contractor.id}:")
        for day in range(7):  # Print calendar for the next 7 days
            current_date = start_date + timedelta(days=day)
            logger.info(f"  {current_date.date()}:")
            current_time = datetime.combine(current_date, WORK_START_TIME_OBJ)
            end_time = datetime.combine(current_date, WORK_END_TIME_OBJ)
            while current_time < end_time:
                next_hour = current_time + timedelta(hours=1)
                if master_calendar.is_contractor_available(contractor.id, current_time, next_hour):
                    logger.info(f"    {current_time.time()} - {next_hour.time()}: Available")
                else:
                    logger.info(f"    {current_time.time()} - {next_hour.time()}: Not Available")
                current_time = next_hour

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

        master_calendar = MasterContractorCalendar()
        for contractor in contractors:
            master_calendar.add_contractor(contractor)

        print_contractor_calendars(master_calendar, contractors)

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

        # Print updated contractor calendars after optimization
        logger.info("Updated Contractor Calendars after Optimization:")
        print_contractor_calendars(master_calendar, contractors)

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

def compare_schedules(initial_sched: Schedule, optimized_sched: Schedule) -> None:
    """
    Compare the initial and optimized schedules.

    Args:
        initial_sched (Schedule): The initial greedy schedule
        optimized_sched (Schedule): The optimized schedule
    """
    logger.info("Schedule Comparison:")
    logger.info("=" * 80)
    logger.info(f"{'Initial Schedule':^40}|{'Optimized Schedule':^40}")
    logger.info("=" * 80)

    all_days = set(initial_sched.assignments.keys()) | set(optimized_sched.assignments.keys())
    for day in sorted(all_days):
        logger.info(f"Day {day.strftime('%Y-%m-%d')}:")
        initial_assignments = initial_sched.assignments.get(day, [])
        optimized_assignments = optimized_sched.assignments.get(day, [])

        max_assignments = max(len(initial_assignments), len(optimized_assignments))

        for i in range(max_assignments):
            initial_str = ""
            optimized_str = ""

            if i < len(initial_assignments):
                customer, contractor, start_time = initial_assignments[i]
                initial_str = f"C{customer.id}-T{contractor.id} @ {start_time.strftime('%H:%M')}"

            if i < len(optimized_assignments):
                customer, contractor, start_time = optimized_assignments[i]
                optimized_str = f"C{customer.id}-T{contractor.id} @ {start_time.strftime('%H:%M')}"

            logger.info(f"{initial_str:^40}|{optimized_str:^40}")

    logger.info("=" * 80)

if __name__ == "__main__":
    cli_main("cp-sat")  # Default to CP-SAT optimizer when run directly