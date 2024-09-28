# This is the initial greedy scheduler for the program.
# This always schedules errands in the order they are received and assigns them to the first available time slot.
# This should never be changed to optimize the initial solution.
# This initial greedy scheduler serves as a starting point for the optimizer.py file.
# This initial greedy scheduler serves as a baseline for performance comparison of the optimizer.py performance.

from models.schedule import Schedule
from utils.errand_utils import calculate_errand_time
from utils.travel_time import calculate_travel_time
from datetime import datetime, timedelta
from constants import SCHEDULING_DAYS, WORK_START_TIME, WORK_END_TIME

def initial_schedule(customers, contractors):
    schedule = Schedule(contractors, customers)
    today = datetime.now().date()

    print("Starting initial scheduling process...")

    for day in range(SCHEDULING_DAYS):
        current_date = today + timedelta(days=day)
        print(f"\nScheduling for day {day} ({current_date}):")
        
        # Reset contractor availability at the start of each day
        for contractor in contractors:
            contractor.available_time = WORK_START_TIME
            contractor.current_location = contractor.location

        for customer in customers:
            print(f"  Attempting to schedule customer {customer.id} for errand type {customer.desired_errand.type}")
            if customer.id not in [assignment[0].id for assignments in schedule.assignments.values() for assignment in assignments]:
                # Find the first available contractor and time slot
                assigned_contractor = None
                start_time = None

                for contractor in contractors:
                    travel_time, _ = calculate_travel_time(contractor.current_location, customer.location)
                    errand_time = calculate_errand_time(customer.desired_errand, contractor.current_location, customer.location)
                    total_time = travel_time + errand_time

                    if contractor.available_time + total_time <= WORK_END_TIME:
                        assigned_contractor = contractor
                        start_time = contractor.available_time + travel_time
                        break

                if assigned_contractor:
                    schedule.assignments.setdefault(day, []).append((customer, assigned_contractor, start_time))
                    
                    # Calculate and log profit
                    contractor_cost = total_time * Schedule.contractor_cost_per_minute
                    errand_charge = customer.desired_errand.calculate_final_charge(current_date, datetime.now())
                    profit = errand_charge - contractor_cost
                    
                    print(f"    Scheduled with contractor {assigned_contractor.id} at start time {start_time}")
                    print(f"    Travel time: {travel_time} minutes")
                    print(f"    Errand time: {errand_time} minutes")
                    print(f"    Errand charge: ${errand_charge:.2f}")
                    print(f"    Contractor cost: ${contractor_cost:.2f}")
                    print(f"    Profit: ${profit:.2f}")
                    
                    assigned_contractor.available_time = start_time + errand_time
                    assigned_contractor.current_location = customer.location
                    print(f"    Contractor {assigned_contractor.id} new available time: {assigned_contractor.available_time}")
                else:
                    print(f"    Could not schedule customer {customer.id} on day {day}")

    print("\nInitial scheduling process completed.")
    total_profit = schedule.calculate_total_profit()
    print(f"Total profit for initial schedule: ${total_profit:.2f}")
    return schedule