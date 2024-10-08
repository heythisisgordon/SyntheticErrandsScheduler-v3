from typing import Dict, Tuple
from models.schedule import Schedule
from datetime import timedelta
from utils.travel_time import calculate_travel_time

def analyze_schedule(schedule: Schedule) -> Dict[str, float]:
    total_travel_time = timedelta()
    total_errands = 0
    errands_per_day = []
    
    for day, assignments in schedule.assignments.items():
        daily_errands = len(assignments)
        total_errands += daily_errands
        errands_per_day.append(daily_errands)
        
        for i, (customer, contractor, start_time) in enumerate(assignments):
            if i == 0:
                travel_time, _ = calculate_travel_time(contractor.location, customer.location)
            else:
                prev_customer = assignments[i-1][0]
                travel_time, _ = calculate_travel_time(prev_customer.location, customer.location)
            total_travel_time += travel_time
    
    return {
        "total_travel_time": total_travel_time.total_seconds() / 3600,  # in hours
        "average_travel_time": (total_travel_time.total_seconds() / 3600) / total_errands if total_errands > 0 else 0,
        "total_errands": total_errands,
        "average_errands_per_day": sum(errands_per_day) / len(errands_per_day) if errands_per_day else 0,
        "max_errands_per_day": max(errands_per_day) if errands_per_day else 0,
        "min_errands_per_day": min(errands_per_day) if errands_per_day else 0,
    }

def compare_schedules(initial_schedule: Schedule, optimized_schedule: Schedule) -> Tuple[Dict[str, float], Dict[str, float], float]:
    initial_analysis = analyze_schedule(initial_schedule)
    optimized_analysis = analyze_schedule(optimized_schedule)
    
    initial_profit = initial_schedule.calculate_total_profit()
    optimized_profit = optimized_schedule.calculate_total_profit()
    profit_difference = optimized_profit - initial_profit
    
    return initial_analysis, optimized_analysis, profit_difference