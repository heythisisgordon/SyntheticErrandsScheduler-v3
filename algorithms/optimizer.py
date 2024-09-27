import random
from datetime import datetime, timedelta
from models.schedule import Schedule
from utils.travel_time import calculate_travel_time
from algorithms.initial_scheduler import calculate_errand_time

def optimize_schedule(schedule: Schedule, iterations: int = 1000) -> Schedule:
    """
    Optimize the given schedule using a simple hill-climbing algorithm.
    
    :param schedule: The initial schedule to optimize
    :param iterations: Number of optimization iterations to perform
    :return: The optimized schedule
    """
    best_schedule = schedule
    best_profit = schedule.calculate_total_profit()
    today = datetime.now().date()

    for _ in range(iterations):
        # Create a copy of the current best schedule
        new_schedule = Schedule(best_schedule.contractors.copy(), best_schedule.customers.copy())
        new_schedule.assignments = {day: assignments.copy() for day, assignments in best_schedule.assignments.items()}

        # Randomly select two assignments and swap them
        days = list(new_schedule.assignments.keys())
        if len(days) < 2:
            continue

        day1, day2 = random.sample(days, 2)
        if not new_schedule.assignments[day1] or not new_schedule.assignments[day2]:
            continue

        idx1 = random.randint(0, len(new_schedule.assignments[day1]) - 1)
        idx2 = random.randint(0, len(new_schedule.assignments[day2]) - 1)

        new_schedule.assignments[day1][idx1], new_schedule.assignments[day2][idx2] = \
            new_schedule.assignments[day2][idx2], new_schedule.assignments[day1][idx1]

        # Recalculate start times for the affected days
        new_schedule.assignments[day1] = recalculate_start_times(new_schedule.assignments[day1], today + timedelta(days=day1))
        new_schedule.assignments[day2] = recalculate_start_times(new_schedule.assignments[day2], today + timedelta(days=day2))

        # Check if the new schedule is valid and calculate its profit
        if is_valid_schedule(new_schedule):
            new_profit = new_schedule.calculate_total_profit()
            if new_profit > best_profit:
                best_schedule = new_schedule
                best_profit = new_profit

    return best_schedule

def recalculate_start_times(assignments, current_date):
    """
    Recalculate start times for a list of assignments.
    
    :param assignments: List of (customer, contractor, start_time) tuples
    :param current_date: The date of the assignments
    :return: Updated list of assignments with recalculated start times
    """
    updated_assignments = []
    current_time = 480  # Start at 8am (480 minutes from midnight)

    for i, (customer, contractor, _) in enumerate(assignments):
        if i == 0:
            travel_time, _ = calculate_travel_time(contractor.location, customer.location)
            current_time = max(480, 480 + travel_time)
        else:
            prev_customer, _, prev_start_time = updated_assignments[-1]
            errand_time = calculate_errand_time(prev_customer.desired_errand, prev_customer.location, customer.location)
            current_time = max(current_time, prev_start_time + errand_time)

        updated_assignments.append((customer, contractor, current_time))
        current_time += calculate_errand_time(customer.desired_errand, contractor.location, customer.location)

    return updated_assignments

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
            errand_time = calculate_errand_time(errand, contractor.location, customer.location)
            
            # Check if the errand starts and ends within working hours
            if start_time < 480 or start_time >= 1020:  # Before 8am or after 5pm
                return False
            
            end_time = start_time + errand_time
            if end_time > 1020:  # After 5pm
                return False

            # Check if there's enough time to travel to the next errand
            if i < len(assignments) - 1:
                next_customer, _, next_start_time = assignments[i + 1]
                if end_time > next_start_time:
                    return False

            # Check specific constraints for each errand type
            if errand.type == "Outing" and errand_time != errand.base_time:
                return False

    return True