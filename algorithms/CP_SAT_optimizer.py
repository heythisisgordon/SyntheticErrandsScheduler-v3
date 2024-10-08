"""
Optimizer module for the Synthetic Errands Scheduler

This module contains functions for optimizing the schedule using Google OR-Tools,
checking the validity of a schedule, and comparing schedules.
"""

import logging
from typing import Dict, List, Tuple, Optional
from ortools.sat.python import cp_model
from datetime import datetime, timedelta
from models.schedule import Schedule
from models.customer import Customer
from models.contractor import Contractor
from utils.travel_time import calculate_travel_time
from utils.errand_utils import get_errand_time, calculate_errand_end_time
from constants import SCHEDULING_DAYS, WORK_START_TIME_OBJ, WORK_END_TIME_OBJ
from utils.scheduling_utils import (
    calculate_total_time,
    is_within_working_hours,
    calculate_profit
)

logger: logging.Logger = logging.getLogger(__name__)

# Type aliases for improved readability
Assignment = Tuple[Customer, Contractor, datetime]
DailyAssignments = List[Assignment]
ScheduleAssignments = Dict[datetime, DailyAssignments]

def setup_model_and_variables(schedule: Schedule) -> Tuple[cp_model.CpModel, Dict, Dict]:
    """Set up the CP model and variables for optimization."""
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
    """Add constraints to the CP model."""
    num_contractors = len(schedule.contractors)
    num_customers = len(schedule.customers)

    add_customer_assignment_constraint(model, x, num_customers, num_contractors)
    add_time_constraints(model, schedule, x, start_times, num_contractors, num_customers)

def add_customer_assignment_constraint(model: cp_model.CpModel, x: Dict, num_customers: int, num_contractors: int) -> None:
    """Ensure each customer is assigned exactly once."""
    for i in range(num_customers):
        model.Add(sum(x[i, j, k] for j in range(num_contractors) for k in range(SCHEDULING_DAYS)) == 1)

def add_time_constraints(model: cp_model.CpModel, schedule: Schedule, x: Dict, start_times: Dict, num_contractors: int, num_customers: int) -> None:
    """Add time-related constraints to the model."""
    today = datetime.now().date()
    for k in range(SCHEDULING_DAYS):
        current_date = today + timedelta(days=k)
        for j in range(num_contractors):
            contractor = schedule.contractors[j]
            contractor_location = initialize_contractor_location(model, contractor, j, k)

            for i in range(num_customers):
                customer = schedule.customers[i]
                errand = customer.desired_errand
                total_time = calculate_total_time(contractor, customer, errand)

                # Ensure the errand starts and ends within working hours
                model.Add(start_times[i, k] + int(total_time.total_seconds() // 60) <= WORK_END_TIME_OBJ.hour * 60 + WORK_END_TIME_OBJ.minute).OnlyEnforceIf(x[i, j, k])

                # Ensure the contractor is available for the errand
                start_datetime = datetime.combine(current_date, datetime.min.time()) + timedelta(minutes=start_times[i, k])
                end_datetime = start_datetime + total_time
                
                # Create a boolean variable for contractor availability
                is_available = model.NewBoolVar(f'is_available[{i},{j},{k}]')
                
                # Link the availability variable to the assignment variable
                model.Add(is_available == 1).OnlyEnforceIf(x[i, j, k])
                model.Add(is_available == 0).OnlyEnforceIf(x[i, j, k].Not())
                
                # Add a custom constraint to check availability
                model.Add(contractor.calendar.is_available(start_datetime, end_datetime) == is_available)

                contractor_location = update_contractor_location(model, customer, start_times[i, k], total_time)

def initialize_contractor_location(model: cp_model.CpModel, contractor: Contractor, j: int, k: int) -> Tuple[cp_model.IntVar, cp_model.IntVar]:
    """Initialize the contractor's location variables."""
    contractor_location_x = model.NewIntVar(0, 100, f'contractor_location_x[{j},{k},0]')
    contractor_location_y = model.NewIntVar(0, 100, f'contractor_location_y[{j},{k},0]')
    model.Add(contractor_location_x == contractor.location[0])
    model.Add(contractor_location_y == contractor.location[1])
    return contractor_location_x, contractor_location_y

def update_contractor_location(model: cp_model.CpModel, customer: Customer, start_time: cp_model.IntVar, total_time: timedelta) -> Tuple[cp_model.IntVar, cp_model.IntVar]:
    """Update the contractor's location after an errand."""
    new_location_x = model.NewIntVar(0, 100, f'new_location_x_{customer.id}')
    new_location_y = model.NewIntVar(0, 100, f'new_location_y_{customer.id}')
    model.Add(new_location_x == customer.location[0])
    model.Add(new_location_y == customer.location[1])
    return new_location_x, new_location_y

def setup_objective(model: cp_model.CpModel, schedule: Schedule, x: Dict, start_times: Dict) -> None:
    """Set up the objective function for the CP model."""
    num_contractors = len(schedule.contractors)
    num_customers = len(schedule.customers)

    objective: List[cp_model.LinearExpr] = []
    today = datetime.now().date()
    for i in range(num_customers):
        for j in range(num_contractors):
            for k in range(SCHEDULING_DAYS):
                current_datetime = datetime.combine(today, datetime.min.time()) + timedelta(days=k, minutes=start_times[i, k].Proto().domain[0])
                profit = calculate_profit(schedule.customers[i], schedule.contractors[j], current_datetime, calculate_total_time(schedule.contractors[j], schedule.customers[i], schedule.customers[i].desired_errand))
                objective.append(profit * x[i, j, k])

    model.Maximize(sum(objective))

def solve_model_and_extract_solution(model: cp_model.CpModel, schedule: Schedule, x: Dict, start_times: Dict) -> Optional[Schedule]:
    """Solve the CP model and extract the solution."""
    solver = setup_solver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        return extract_solution(solver, schedule, x, start_times)
    else:
        logger.warning('No solution found.')
        return None

def setup_solver() -> cp_model.CpSolver:
    """Set up the CP-SAT solver with appropriate parameters."""
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 600.0  # Increase solving time to 10 minutes
    solver.parameters.log_search_progress = True  # Enable logging
    return solver

def extract_solution(solver: cp_model.CpSolver, schedule: Schedule, x: Dict, start_times: Dict) -> Schedule:
    """Extract the solution from the solved model and create a new schedule."""
    new_schedule = Schedule(schedule.contractors.copy(), schedule.customers.copy())

    logger.info("Optimized Schedule:")
    today = datetime.now().date()
    
    for k in range(SCHEDULING_DAYS):
        current_date = today + timedelta(days=k)
        logger.info(f"Day {k} ({current_date}):")
        
        for j, contractor in enumerate(schedule.contractors):
            contractor_location = contractor.location
            for i, customer in enumerate(schedule.customers):
                if solver.BooleanValue(x[i, j, k]):
                    process_assigned_errand(new_schedule, solver, schedule, start_times, i, j, k, current_date, contractor, customer, contractor_location)
                    contractor_location = customer.location

    log_total_profit(new_schedule)
    return new_schedule

def process_assigned_errand(new_schedule: Schedule, solver: cp_model.CpSolver, schedule: Schedule, start_times: Dict, 
                            i: int, j: int, k: int, current_date: datetime, contractor: Contractor, customer: Customer, 
                            contractor_location: Tuple[int, int]) -> None:
    """Process an assigned errand and add it to the new schedule."""
    start_time_minutes = solver.Value(start_times[i, k])
    start_time = datetime.combine(current_date, datetime.min.time()) + timedelta(minutes=start_time_minutes)
    
    total_time = calculate_total_time(contractor, customer, customer.desired_errand)
    end_time = start_time + total_time

    errand_id = f"errand_{customer.id}_{contractor.id}_{start_time.strftime('%Y%m%d%H%M')}"
    if contractor.calendar.reserve_time_slot(errand_id, start_time, end_time):
        new_schedule.add_assignment(start_time, customer, contractor)
        
        profit = calculate_profit(customer, contractor, start_time, total_time)

        log_errand_details(customer, contractor, start_time, total_time, profit)
    else:
        logger.warning(f"Failed to reserve time slot for customer {customer.id} with contractor {contractor.id} on {current_date}")

def log_errand_details(customer: Customer, contractor: Contractor, start_time: datetime, 
                       total_time: timedelta, profit: float) -> None:
    """Log the details of an assigned errand."""
    logger.info(f"  Customer {customer.id} assigned to Contractor {contractor.id}")
    logger.debug(f"    Start Time: {start_time.time()}")
    logger.debug(f"    Total Time: {total_time}")
    logger.debug(f"    Profit: ${profit:.2f}")

def log_total_profit(schedule: Schedule) -> None:
    """Calculate and log the total profit of the schedule."""
    total_profit = schedule.calculate_total_profit()
    logger.info(f"Optimized schedule total profit: ${total_profit:.2f}")

def optimize_schedule(schedule: Schedule) -> Tuple[Schedule, Schedule]:
    """Optimize the given schedule using Google OR-Tools."""
    logger.info("Starting schedule optimization")
    try:
        model, x, start_times = setup_model_and_variables(schedule)
        logger.info("Model and variables set up successfully")
        
        add_constraints(model, schedule, x, start_times)
        logger.info("Constraints added successfully")
        
        setup_objective(model, schedule, x, start_times)
        logger.info("Objective function set up successfully")
        
        optimized_schedule = solve_model_and_extract_solution(model, schedule, x, start_times)
        logger.info("Model solved and solution extracted successfully")
        
        if optimized_schedule:
            logger.info("Optimization completed successfully")
            return schedule, optimized_schedule
        else:
            logger.warning("Optimization failed to find a solution")
            return schedule, schedule
    except Exception as e:
        logger.error(f"An error occurred during optimization: {str(e)}")
        return schedule, schedule

def is_valid_schedule(schedule: Schedule) -> bool:
    """Check if the given schedule is valid (respects working hours and travel times)."""
    for day, assignments in schedule.assignments.items():
        if not is_valid_day_schedule(day, assignments):
            return False
    return True

def is_valid_day_schedule(day: datetime, assignments: List[Assignment]) -> bool:
    """Check if the schedule for a specific day is valid."""
    contractor_location = None
    for i, (customer, contractor, start_time) in enumerate(assignments):
        if not is_valid_errand(day, customer, contractor, start_time, contractor_location):
            return False
        contractor_location = update_contractor_location_after_errand(customer, start_time, get_errand_time(customer.desired_errand, contractor.location, customer.location))
    return True

def is_valid_errand(day: datetime, customer: Customer, contractor: Contractor, start_time: datetime, contractor_location: Optional[Tuple[Tuple[int, int], datetime]]) -> bool:
    """Check if a single errand assignment is valid."""
    errand = customer.desired_errand
    total_time = calculate_total_time(contractor, customer, errand)
    end_time = start_time + total_time
    
    if not is_within_working_hours(start_time, total_time):
        logger.warning(f"Invalid schedule: Errand for customer {customer.id} starts or ends outside working hours on {day}")
        return False
    
    if contractor_location and not has_enough_travel_time(contractor_location, customer.location, start_time):
        logger.warning(f"Invalid schedule: Not enough time to travel to errand for customer {customer.id} on {day}")
        return False
    
    if not contractor.calendar.is_available(start_time, end_time):
        logger.warning(f"Invalid schedule: Contractor {contractor.id} is not available for errand for customer {customer.id} on {day}")
        return False
    
    return True

def has_enough_travel_time(contractor_location: Tuple[Tuple[int, int], datetime], customer_location: Tuple[int, int], start_time: datetime) -> bool:
    """Check if there's enough time to travel to the errand location."""
    travel_time, _ = calculate_travel_time(contractor_location[0], customer_location)
    return start_time >= contractor_location[1] + travel_time

def update_contractor_location_after_errand(customer: Customer, start_time: datetime, errand_time: timedelta) -> Tuple[Tuple[int, int], datetime]:
    """Update the contractor's location after completing an errand."""
    end_time = calculate_errand_end_time(start_time, errand_time)
    return (customer.location, end_time)

def compare_schedules(initial_schedule: Schedule, optimized_schedule: Schedule) -> None:
    """Compare the initial and optimized schedules side-by-side."""
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