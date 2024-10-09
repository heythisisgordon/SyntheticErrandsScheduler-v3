"""
Optimizer module for the Synthetic Errands Scheduler using Google OR-Tools CP-SAT solver.
"""

import logging
from typing import Dict, List, Tuple, Optional
from ortools.sat.python import cp_model
from datetime import datetime, timedelta
from models.schedule import Schedule
from models.customer import Customer
from models.contractor import Contractor
from models.master_contractor_calendar import MasterContractorCalendar
from constants import SCHEDULING_DAYS, WORK_START_TIME_OBJ, WORK_END_TIME_OBJ
from utils.scheduling_utils import calculate_total_time, calculate_profit

logger: logging.Logger = logging.getLogger(__name__)

def optimize_schedule(schedule: Schedule, master_calendar: MasterContractorCalendar) -> Tuple[Schedule, Schedule]:
    """Optimize the given schedule using Google OR-Tools CP-SAT solver."""
    logger.info("Starting schedule optimization")
    try:
        model, x, start_times = setup_model(schedule, master_calendar)
        optimized_schedule = solve_model(model, schedule, x, start_times, master_calendar)
        return schedule, optimized_schedule or schedule
    except Exception as e:
        logger.error(f"An error occurred during optimization: {str(e)}")
        return schedule, schedule

def setup_model(schedule: Schedule, master_calendar: MasterContractorCalendar) -> Tuple[cp_model.CpModel, Dict, Dict]:
    """Set up the CP model, variables, constraints, and objective."""
    model = cp_model.CpModel()
    x, start_times = create_variables(model, schedule)
    add_constraints(model, schedule, x, start_times, master_calendar)
    setup_objective(model, schedule, x, start_times)
    return model, x, start_times

def create_variables(model: cp_model.CpModel, schedule: Schedule) -> Tuple[Dict, Dict]:
    """Create decision variables for the CP model."""
    num_contractors = len(schedule.contractors)
    num_customers = len(schedule.customers)
    
    x = {(i, j, k): model.NewBoolVar(f'x[{i},{j},{k}]')
         for i in range(num_customers)
         for j in range(num_contractors)
         for k in range(SCHEDULING_DAYS)}

    start_times = {(i, k): model.NewIntVar(
        WORK_START_TIME_OBJ.hour * 60 + WORK_START_TIME_OBJ.minute,
        WORK_END_TIME_OBJ.hour * 60 + WORK_END_TIME_OBJ.minute,
        f'start_time[{i},{k}]'
    ) for i in range(num_customers) for k in range(SCHEDULING_DAYS)}
    
    return x, start_times

def add_constraints(model: cp_model.CpModel, schedule: Schedule, x: Dict, start_times: Dict, master_calendar: MasterContractorCalendar) -> None:
    """Add constraints to the CP model."""
    num_contractors = len(schedule.contractors)
    num_customers = len(schedule.customers)

    # Each customer must be assigned exactly once
    for i in range(num_customers):
        model.Add(sum(x[i, j, k] for j in range(num_contractors) for k in range(SCHEDULING_DAYS)) == 1)

    add_time_constraints(model, schedule, x, start_times, master_calendar)

def add_time_constraints(model: cp_model.CpModel, schedule: Schedule, x: Dict, start_times: Dict, master_calendar: MasterContractorCalendar) -> None:
    """Add time-related constraints to the model."""
    today = datetime.now().date()
    for k in range(SCHEDULING_DAYS):
        current_date = today + timedelta(days=k)
        for j, contractor in enumerate(schedule.contractors):
            for i, customer in enumerate(schedule.customers):
                add_errand_constraints(model, x, start_times, i, j, k, contractor, customer, current_date, master_calendar)

def add_errand_constraints(model: cp_model.CpModel, x: Dict, start_times: Dict, 
                           i: int, j: int, k: int, contractor: Contractor, customer: Customer, 
                           current_date: datetime, master_calendar: MasterContractorCalendar) -> None:
    """Add constraints for a specific errand assignment."""
    total_time = calculate_total_time(contractor, customer, customer.desired_errand)
    
    # Ensure the errand ends within working hours
    model.Add(start_times[i, k] + int(total_time.total_seconds() // 60) <= WORK_END_TIME_OBJ.hour * 60 + WORK_END_TIME_OBJ.minute).OnlyEnforceIf(x[i, j, k])

    start_datetime = datetime.combine(current_date, datetime.min.time()) + timedelta(minutes=start_times[i, k])
    end_datetime = start_datetime + total_time
    
    # Ensure the contractor is available for the errand
    is_available = model.NewBoolVar(f'is_available[{i},{j},{k}]')
    model.Add(is_available == 1).OnlyEnforceIf(x[i, j, k])
    model.Add(is_available == 0).OnlyEnforceIf(x[i, j, k].Not())
    model.Add(master_calendar.is_contractor_available(contractor.id, start_datetime, end_datetime) == is_available)

def setup_objective(model: cp_model.CpModel, schedule: Schedule, x: Dict, start_times: Dict) -> None:
    """Set up the objective function for the CP model."""
    objective_terms = []
    today = datetime.now().date()
    for i, customer in enumerate(schedule.customers):
        for j, contractor in enumerate(schedule.contractors):
            for k in range(SCHEDULING_DAYS):
                current_datetime = datetime.combine(today, datetime.min.time()) + timedelta(days=k, minutes=start_times[i, k].Proto().domain[0])
                profit = calculate_profit(customer, contractor, current_datetime, calculate_total_time(contractor, customer, customer.desired_errand))
                objective_terms.append(profit * x[i, j, k])

    model.Maximize(sum(objective_terms))

def solve_model(model: cp_model.CpModel, schedule: Schedule, x: Dict, start_times: Dict, master_calendar: MasterContractorCalendar) -> Optional[Schedule]:
    """Solve the CP model and extract the solution."""
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 600.0  # 10 minutes
    solver.parameters.log_search_progress = True
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        return extract_solution(solver, schedule, x, start_times, master_calendar)
    else:
        logger.warning('No solution found.')
        return None

def extract_solution(solver: cp_model.CpSolver, schedule: Schedule, x: Dict, start_times: Dict, master_calendar: MasterContractorCalendar) -> Schedule:
    """Extract the solution from the solved model and create a new schedule."""
    new_schedule = Schedule(schedule.contractors.copy(), schedule.customers.copy())
    today = datetime.now().date()
    
    for k in range(SCHEDULING_DAYS):
        current_date = today + timedelta(days=k)
        for j, contractor in enumerate(schedule.contractors):
            for i, customer in enumerate(schedule.customers):
                if solver.BooleanValue(x[i, j, k]):
                    process_assignment(new_schedule, solver, start_times, i, j, k, current_date, contractor, customer, master_calendar)

    log_total_profit(new_schedule)
    return new_schedule

def process_assignment(new_schedule: Schedule, solver: cp_model.CpSolver, start_times: Dict, 
                       i: int, j: int, k: int, current_date: datetime, contractor: Contractor, 
                       customer: Customer, master_calendar: MasterContractorCalendar) -> None:
    """Process an assigned errand and add it to the new schedule."""
    start_time = datetime.combine(current_date, datetime.min.time()) + timedelta(minutes=solver.Value(start_times[i, k]))
    total_time = calculate_total_time(contractor, customer, customer.desired_errand)
    end_time = start_time + total_time

    errand_id = f"errand_{customer.id}_{contractor.id}_{start_time.strftime('%Y%m%d%H%M')}"
    if master_calendar.reserve_time_slot(contractor.id, errand_id, start_time, end_time):
        new_schedule.add_assignment(start_time, customer, contractor)
        profit = calculate_profit(customer, contractor, start_time, total_time)
        logger.info(f"Customer {customer.id} assigned to Contractor {contractor.id} at {start_time.time()}, profit: ${profit:.2f}")
    else:
        logger.warning(f"Failed to reserve time slot for customer {customer.id} with contractor {contractor.id} on {current_date}")

def log_total_profit(schedule: Schedule) -> None:
    """Calculate and log the total profit of the schedule."""
    total_profit = schedule.calculate_total_profit()
    logger.info(f"Optimized schedule total profit: ${total_profit:.2f}")

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
        log_daily_comparison(day, initial_schedule, optimized_schedule)

    log_profit_comparison(initial_profit, optimized_profit)

def log_daily_comparison(day: datetime, initial_schedule: Schedule, optimized_schedule: Schedule) -> None:
    """Log the comparison of assignments for a specific day."""
    logger.info(f"Day {day.strftime('%Y-%m-%d')}:")
    initial_assignments = initial_schedule.assignments.get(day, [])
    optimized_assignments = optimized_schedule.assignments.get(day, [])

    max_assignments = max(len(initial_assignments), len(optimized_assignments))

    for i in range(max_assignments):
        initial_str = format_assignment(initial_assignments, i) if i < len(initial_assignments) else ""
        optimized_str = format_assignment(optimized_assignments, i) if i < len(optimized_assignments) else ""
        logger.info(f"{initial_str:^40}|{optimized_str:^40}")

def format_assignment(assignments: List[Tuple[Customer, Contractor, datetime]], index: int) -> str:
    """Format a single assignment for logging."""
    customer, contractor, start_time = assignments[index]
    return f"C{customer.id}-T{contractor.id} @ {start_time.strftime('%H:%M')}"

def log_profit_comparison(initial_profit: float, optimized_profit: float) -> None:
    """Log the profit comparison between initial and optimized schedules."""
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