"""
Optimizer module for the Synthetic Errands Scheduler

This module contains functions for optimizing the schedule using Google OR-Tools,
checking the validity of a schedule, and comparing schedules.
"""

import logging
from typing import Dict, List, Tuple, Optional
from ortools.sat.python import cp_model
from datetime import datetime, timedelta, time
from models.schedule import Schedule
from models.customer import Customer
from models.contractor import Contractor
from utils.travel_time import calculate_travel_time
from utils.errand_utils import get_errand_time, calculate_errand_end_time
from constants import SCHEDULING_DAYS, WORK_START_TIME, WORK_END_TIME

logger: logging.Logger = logging.getLogger(__name__)

# Type aliases for improved readability
Assignment = Tuple[Customer, Contractor, datetime]
DailyAssignments = List[Assignment]
ScheduleAssignments = Dict[datetime, DailyAssignments]

# Convert WORK_START_TIME and WORK_END_TIME to datetime.time objects
WORK_START_TIME_OBJ = time(hour=WORK_START_TIME // 60, minute=WORK_START_TIME % 60)
WORK_END_TIME_OBJ = time(hour=WORK_END_TIME // 60, minute=WORK_END_TIME % 60)

def setup_model_and_variables(schedule: Schedule) -> Tuple[cp_model.CpModel, Dict, Dict]:
    """
    Set up the CP model and variables for optimization.
    
    Args:
        schedule (Schedule): The initial schedule to optimize
    
    Returns:
        Tuple[cp_model.CpModel, Dict, Dict]: The model, assignment variables, and start time variables
    """
    model = cp_model.CpModel()
    num_contractors = len(schedule.contractors)
    num_customers = len(schedule.customers)
    
    # Binary variable: is customer i assigned to contractor j on day k
    x: Dict[Tuple[int, int, int], cp_model.IntVar] = {}
    for i in range(num_customers):
        for j in range(num_contractors):
            for k in range(SCHEDULING_DAYS):
                x[i, j, k] = model.NewBoolVar(f'x[{i},{j},{k}]')

    # Start time variable for each customer (in minutes since midnight)
    start_times: Dict[Tuple[int, int], cp_model.IntVar] = {}
    for i in range(num_customers):
        for k in range(SCHEDULING_DAYS):
            start_times[i, k] = model.NewIntVar(
                WORK_START_TIME_OBJ.hour * 60 + WORK_START_TIME_OBJ.minute,
                WORK_END_TIME_OBJ.hour * 60 + WORK_END_TIME_OBJ.minute,
                f'start_time[{i},{k}]'
            )
    
    return model, x, start_times

def add_constraints(model: cp_model.CpModel, schedule: Schedule, x: Dict, start_times: Dict) -> None:
    """
    Add constraints to the CP model.
    
    Args:
        model (cp_model.CpModel): The CP model
        schedule (Schedule): The initial schedule
        x (Dict): The assignment variables
        start_times (Dict): The start time variables
    """
    num_contractors = len(schedule.contractors)
    num_customers = len(schedule.customers)

    # Each customer must be assigned exactly once
    for i in range(num_customers):
        model.Add(sum(x[i, j, k] for j in range(num_contractors) for k in range(SCHEDULING_DAYS)) == 1)

    # Time constraints
    for k in range(SCHEDULING_DAYS):
        for j in range(num_contractors):
            contractor_location = schedule.contractors[j].location
            for i in range(num_customers):
                customer = schedule.customers[i]
                errand = customer.desired_errand
                total_time = get_errand_time(errand, contractor_location, customer.location)

                # Ensure the errand starts and ends within working hours
                model.Add(start_times[i, k] + int(total_time.total_seconds() // 60) <= WORK_END_TIME_OBJ.hour * 60 + WORK_END_TIME_OBJ.minute).OnlyEnforceIf(x[i, j, k])

                for i2 in range(i+1, num_customers):
                    # If both customers are assigned to this contractor on this day
                    condition = model.NewBoolVar('condition')
                    model.Add(x[i, j, k] + x[i2, j, k] == 2).OnlyEnforceIf(condition)
                    model.Add(x[i, j, k] + x[i2, j, k] != 2).OnlyEnforceIf(condition.Not())
                    
                    # Ensure no overlap, including travel time
                    next_travel_time, _ = calculate_travel_time(customer.location, schedule.customers[i2].location)
                    model.Add(start_times[i2, k] >= start_times[i, k] + int(total_time.total_seconds() // 60) + int(next_travel_time.total_seconds() // 60)).OnlyEnforceIf(condition)

def setup_objective(model: cp_model.CpModel, schedule: Schedule, x: Dict) -> None:
    """
    Set up the objective function for the CP model.
    
    Args:
        model (cp_model.CpModel): The CP model
        schedule (Schedule): The initial schedule
        x (Dict): The assignment variables
    """
    num_contractors = len(schedule.contractors)
    num_customers = len(schedule.customers)

    objective: List[cp_model.LinearExpr] = []
    for i in range(num_customers):
        for j in range(num_contractors):
            for k in range(SCHEDULING_DAYS):
                customer = schedule.customers[i]
                errand = customer.desired_errand
                contractor = schedule.contractors[j]
                total_time = get_errand_time(errand, contractor.location, customer.location)
                
                charge = errand.calculate_final_charge(datetime.now() + timedelta(days=k), datetime.now())
                cost = total_time.total_seconds() / 60 * contractor.rate
                profit = charge - cost
                
                objective.append(cp_model.LinearExpr.Term(x[i, j, k], int(profit * 100)))  # Convert to cents for integer optimization

    model.Maximize(sum(objective))

def solve_model_and_extract_solution(model: cp_model.CpModel, schedule: Schedule, x: Dict, start_times: Dict) -> Optional[Schedule]:
    """
    Solve the CP model and extract the solution.
    
    Args:
        model (cp_model.CpModel): The CP model
        schedule (Schedule): The initial schedule
        x (Dict): The assignment variables
        start_times (Dict): The start time variables
    
    Returns:
        Optional[Schedule]: The optimized schedule, or None if no solution was found
    """
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 60.0  # Limit solving time to 60 seconds
    solver.parameters.log_search_progress = True  # Enable logging

    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        new_schedule = Schedule(schedule.contractors.copy(), schedule.customers.copy())
        new_schedule.assignments = {}

        logger.info("Optimized Schedule:")
        today = datetime.now().date()
        for k in range(SCHEDULING_DAYS):
            current_date = today + timedelta(days=k)
            logger.info(f"Day {k} ({current_date}):")
            for j, contractor in enumerate(schedule.contractors):
                contractor_location = contractor.location
                for i, customer in enumerate(schedule.customers):
                    if solver.BooleanValue(x[i, j, k]):
                        start_time_minutes = solver.Value(start_times[i, k])
                        start_time = datetime.combine(current_date, time(hour=start_time_minutes // 60, minute=start_time_minutes % 60))
                        new_schedule.assignments.setdefault(current_date, []).append((customer, contractor, start_time))
                        
                        total_time = get_errand_time(customer.desired_errand, contractor_location, customer.location)
                        charge = customer.desired_errand.calculate_final_charge(start_time, datetime.now())
                        cost = total_time.total_seconds() / 60 * contractor.rate
                        profit = charge - cost

                        logger.info(f"  Customer {customer.id} assigned to Contractor {contractor.id}")
                        logger.debug(f"    Start Time: {start_time.time()}")
                        logger.debug(f"    Total Time: {total_time}")
                        logger.debug(f"    Charge: ${charge:.2f}")
                        logger.debug(f"    Cost: ${cost:.2f}")
                        logger.debug(f"    Profit: ${profit:.2f}")
                        
                        # Update contractor location
                        contractor_location = customer.location

        # Calculate and log the total profit
        total_profit = new_schedule.calculate_total_profit()
        logger.info(f"Optimized schedule total profit: ${total_profit:.2f}")

        return new_schedule
    else:
        logger.warning('No solution found.')
        return None

def optimize_schedule(schedule: Schedule) -> Schedule:
    """
    Optimize the given schedule using Google OR-Tools.
    
    Args:
        schedule (Schedule): The initial schedule to optimize
    
    Returns:
        Schedule: The optimized schedule
    """
    model, x, start_times = setup_model_and_variables(schedule)
    add_constraints(model, schedule, x, start_times)
    setup_objective(model, schedule, x)
    optimized_schedule = solve_model_and_extract_solution(model, schedule, x, start_times)
    
    return optimized_schedule if optimized_schedule else schedule

def is_valid_schedule(schedule: Schedule) -> bool:
    """
    Check if the given schedule is valid (respects working hours and travel times).
    
    Args:
        schedule (Schedule): The schedule to check
    
    Returns:
        bool: True if the schedule is valid, False otherwise
    """
    for day, assignments in schedule.assignments.items():
        for i, (customer, contractor, start_time) in enumerate(assignments):
            errand = customer.desired_errand
            total_time = get_errand_time(errand, contractor.location, customer.location)
            
            # Check if the errand starts and ends within working hours
            if start_time.time() < WORK_START_TIME_OBJ or start_time.time() >= WORK_END_TIME_OBJ:
                logger.warning(f"Invalid schedule: Errand for customer {customer.id} starts outside working hours on {day}")
                return False
            
            end_time = calculate_errand_end_time(start_time, total_time)
            if end_time.time() > WORK_END_TIME_OBJ:
                logger.warning(f"Invalid schedule: Errand for customer {customer.id} ends after working hours on {day}")
                return False

            # Check if there's enough time to travel to the next errand
            if i < len(assignments) - 1:
                next_customer, _, next_start_time = assignments[i + 1]
                next_travel_time, _ = calculate_travel_time(customer.location, next_customer.location)
                if end_time + next_travel_time > next_start_time:
                    logger.warning(f"Invalid schedule: Not enough time between errands for customers {customer.id} and {next_customer.id} on {day}")
                    return False

            # Update contractor location
            contractor.location = customer.location

    return True

def compare_schedules(initial_schedule: Schedule, optimized_schedule: Schedule) -> None:
    """
    Compare the initial and optimized schedules side-by-side.
    
    Args:
        initial_schedule (Schedule): The initial greedy schedule
        optimized_schedule (Schedule): The optimized schedule
    """
    logger.info("Schedule Comparison:")
    logger.info("=" * 80)
    logger.info(f"{'Initial Schedule':^40}|{'Optimized Schedule':^40}")
    logger.info("=" * 80)

    initial_profit = initial_schedule.calculate_total_profit()
    optimized_profit = optimized_schedule.calculate_total_profit()

    all_days = set(initial_schedule.assignments.keys()) | set(optimized_schedule.assignments.keys())
    for day in sorted(all_days):
        logger.info(f"Day {day.strftime('%Y-%m-%d')}:")
        initial_assignments = initial_schedule.assignments.get(day, [])
        optimized_assignments = optimized_schedule.assignments.get(day, [])

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
    logger.info(f"{'Total Profit':^40}|{'Total Profit':^40}")
    logger.info(f"${initial_profit:.2f}".center(40) + "|" + f"${optimized_profit:.2f}".center(40))
    logger.info("=" * 80)

    if optimized_profit > initial_profit:
        improvement = (optimized_profit - initial_profit) / initial_profit * 100
        logger.info(f"The optimized schedule improved profit by {improvement:.2f}%")
    elif optimized_profit < initial_profit:
        decrease = (initial_profit - optimized_profit) / initial_profit * 100
        logger.info(f"The optimized schedule decreased profit by {decrease:.2f}%")
    else:
        logger.info("Both schedules have the same profit.")