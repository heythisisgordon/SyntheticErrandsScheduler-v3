from ortools.sat.python import cp_model
from datetime import datetime, timedelta
from models.schedule import Schedule
from utils.travel_time import calculate_travel_time
from utils.errand_utils import calculate_errand_time
from constants import SCHEDULING_DAYS, WORK_START_TIME, WORK_END_TIME

def optimize_schedule(schedule: Schedule) -> Schedule:
    """
    Optimize the given schedule using Google OR-Tools.
    
    :param schedule: The initial schedule to optimize
    :return: The optimized schedule
    """
    model = cp_model.CpModel()
    solver = cp_model.CpSolver()

    # Set solver parameters
    solver.parameters.max_time_in_seconds = 60.0  # Limit solving time to 60 seconds
    solver.parameters.log_search_progress = True  # Enable logging

    # Create variables
    num_contractors = len(schedule.contractors)
    num_customers = len(schedule.customers)
    
    # Binary variable: is customer i assigned to contractor j on day k
    x = {}
    for i in range(num_customers):
        for j in range(num_contractors):
            for k in range(SCHEDULING_DAYS):
                x[i, j, k] = model.NewBoolVar(f'x[{i},{j},{k}]')

    # Start time variable for each customer
    start_times = {}
    for i in range(num_customers):
        for k in range(SCHEDULING_DAYS):
            start_times[i, k] = model.NewIntVar(WORK_START_TIME, WORK_END_TIME, f'start_time[{i},{k}]')

    # Constraints
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
                travel_time, _ = calculate_travel_time(contractor_location, customer.location)
                errand_time = calculate_errand_time(errand, contractor_location, customer.location)
                total_time = travel_time + errand_time

                # Ensure the errand starts and ends within working hours
                model.Add(start_times[i, k] + total_time <= WORK_END_TIME).OnlyEnforceIf(x[i, j, k])

                for i2 in range(i+1, num_customers):
                    # If both customers are assigned to this contractor on this day
                    condition = model.NewBoolVar('condition')
                    model.Add(x[i, j, k] + x[i2, j, k] == 2).OnlyEnforceIf(condition)
                    model.Add(x[i, j, k] + x[i2, j, k] != 2).OnlyEnforceIf(condition.Not())
                    
                    # Ensure no overlap, including travel time
                    next_travel_time, _ = calculate_travel_time(customer.location, schedule.customers[i2].location)
                    model.Add(start_times[i2, k] >= start_times[i, k] + total_time + next_travel_time).OnlyEnforceIf(condition)

    # Objective: Maximize profit
    objective = []
    for i in range(num_customers):
        for j in range(num_contractors):
            for k in range(SCHEDULING_DAYS):
                customer = schedule.customers[i]
                errand = customer.desired_errand
                contractor = schedule.contractors[j]
                travel_time, _ = calculate_travel_time(contractor.location, customer.location)
                errand_time = calculate_errand_time(errand, contractor.location, customer.location)
                total_time = travel_time + errand_time
                
                charge = errand.calculate_final_charge(datetime.now().date() + timedelta(days=k), datetime.now())
                cost = total_time * Schedule.contractor_cost_per_minute
                profit = charge - cost
                
                objective.append(cp_model.LinearExpr.Term(x[i, j, k], profit))

    model.Maximize(sum(objective))

    # Solve the problem
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        # Convert the solution back to our Schedule format
        new_schedule = Schedule(schedule.contractors.copy(), schedule.customers.copy())
        new_schedule.assignments = {k: [] for k in range(SCHEDULING_DAYS)}

        print("\nOptimized Schedule:")
        for k in range(SCHEDULING_DAYS):
            print(f"\nDay {k}:")
            for j in range(num_contractors):
                contractor_location = schedule.contractors[j].location
                for i in range(num_customers):
                    if solver.BooleanValue(x[i, j, k]):
                        start_time = solver.Value(start_times[i, k])
                        customer = schedule.customers[i]
                        new_schedule.assignments[k].append((customer, schedule.contractors[j], start_time))
                        
                        travel_time, _ = calculate_travel_time(contractor_location, customer.location)
                        errand_time = calculate_errand_time(customer.desired_errand, contractor_location, customer.location)
                        total_time = travel_time + errand_time
                        charge = customer.desired_errand.calculate_final_charge(datetime.now().date() + timedelta(days=k), datetime.now())
                        cost = total_time * Schedule.contractor_cost_per_minute
                        profit = charge - cost

                        print(f"  Customer {customer.id} assigned to Contractor {schedule.contractors[j].id}")
                        print(f"    Start Time: {start_time}")
                        print(f"    Travel Time: {travel_time}")
                        print(f"    Errand Time: {errand_time}")
                        print(f"    Charge: ${charge:.2f}")
                        print(f"    Cost: ${cost:.2f}")
                        print(f"    Profit: ${profit:.2f}")
                        
                        # Update contractor location
                        contractor_location = customer.location

        # Calculate and print the total profit
        total_profit = new_schedule.calculate_total_profit()
        print(f"\nOptimized schedule total profit: ${total_profit:.2f}")

        return new_schedule
    else:
        print('No solution found.')
        return schedule

def is_valid_schedule(schedule: Schedule) -> bool:
    """
    Check if the given schedule is valid (respects working hours and travel times).
    
    :param schedule: The schedule to check
    :return: True if the schedule is valid, False otherwise
    """
    today = datetime.now().date()
    
    for day, assignments in schedule.assignments.items():
        current_date = today + timedelta(days=day)
        for i, (customer, contractor, start_time) in enumerate(assignments):
            errand = customer.desired_errand
            travel_time, _ = calculate_travel_time(contractor.location, customer.location)
            errand_time = calculate_errand_time(errand, contractor.location, customer.location)
            total_time = travel_time + errand_time
            
            # Check if the errand starts and ends within working hours
            if start_time < WORK_START_TIME or start_time >= WORK_END_TIME:
                return False
            
            end_time = start_time + total_time
            if end_time > WORK_END_TIME:
                return False

            # Check if there's enough time to travel to the next errand
            if i < len(assignments) - 1:
                next_customer, _, next_start_time = assignments[i + 1]
                next_travel_time, _ = calculate_travel_time(customer.location, next_customer.location)
                if end_time + next_travel_time > next_start_time:
                    return False

            # Update contractor location
            contractor.location = customer.location

    return True

def compare_schedules(initial_schedule: Schedule, optimized_schedule: Schedule):
    """
    Compare the initial and optimized schedules side-by-side.
    
    :param initial_schedule: The initial greedy schedule
    :param optimized_schedule: The optimized schedule
    """
    print("\nSchedule Comparison:")
    print("=" * 80)
    print(f"{'Initial Schedule':^40}|{'Optimized Schedule':^40}")
    print("=" * 80)

    initial_profit = initial_schedule.calculate_total_profit()
    optimized_profit = optimized_schedule.calculate_total_profit()

    for day in range(SCHEDULING_DAYS):
        print(f"\nDay {day}:")
        initial_assignments = initial_schedule.assignments.get(day, [])
        optimized_assignments = optimized_schedule.assignments.get(day, [])

        max_assignments = max(len(initial_assignments), len(optimized_assignments))

        for i in range(max_assignments):
            initial_str = ""
            optimized_str = ""

            if i < len(initial_assignments):
                customer, contractor, start_time = initial_assignments[i]
                initial_str = f"C{customer.id}-T{contractor.id} @ {start_time}"

            if i < len(optimized_assignments):
                customer, contractor, start_time = optimized_assignments[i]
                optimized_str = f"C{customer.id}-T{contractor.id} @ {start_time}"

            print(f"{initial_str:^40}|{optimized_str:^40}")

    print("\n" + "=" * 80)
    print(f"{'Total Profit':^40}|{'Total Profit':^40}")
    print(f"${initial_profit:.2f}".center(40) + "|" + f"${optimized_profit:.2f}".center(40))
    print("=" * 80)

    if optimized_profit > initial_profit:
        improvement = (optimized_profit - initial_profit) / initial_profit * 100
        print(f"\nThe optimized schedule improved profit by {improvement:.2f}%")
    elif optimized_profit < initial_profit:
        decrease = (initial_profit - optimized_profit) / initial_profit * 100
        print(f"\nThe optimized schedule decreased profit by {decrease:.2f}%")
    else:
        print("\nBoth schedules have the same profit.")