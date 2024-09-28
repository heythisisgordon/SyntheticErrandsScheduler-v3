from models.schedule import Schedule
from utils.travel_time import calculate_travel_time
from utils.errand_utils import calculate_errand_time
from datetime import datetime, timedelta

def initial_schedule(customers, contractors):
    schedule = Schedule(contractors, customers)
    today = datetime.now().date()

    print("Starting initial scheduling process...")

    for day in range(14):  # 14-day period
        current_date = today + timedelta(days=day)
        print(f"\nScheduling for day {day} ({current_date}):")
        
        # Reset contractor locations and availability at the start of each day
        for contractor in contractors:
            contractor.location = contractor.initial_location
            contractor.available_time = 480  # 8:00 AM in minutes

        for customer in customers:
            print(f"  Attempting to schedule customer {customer.id} for errand type {customer.desired_errand.type}")
            if customer.id not in [assignment[0].id for assignments in schedule.assignments.values() for assignment in assignments]:
                best_contractor = None
                best_start_time = float('inf')

                for contractor in contractors:
                    travel_time, _ = calculate_travel_time(contractor.location, customer.location)
                    errand_time = calculate_errand_time(customer.desired_errand, customer.location, customer.location)
                    possible_start_time = max(contractor.available_time + travel_time, 480)
                    possible_end_time = possible_start_time + errand_time

                    print(f"    Contractor {contractor.id}: Available at {contractor.available_time}, Travel time: {travel_time}, Possible start: {possible_start_time}, Possible end: {possible_end_time}")

                    if possible_end_time <= 1020 and possible_start_time < best_start_time:  # 5:00 PM in minutes
                        best_contractor = contractor
                        best_start_time = possible_start_time

                if best_contractor:
                    # Check if there's a previous errand for this contractor on this day
                    prev_assignments = [a for a in schedule.assignments.get(day, []) if a[1].id == best_contractor.id]
                    if prev_assignments:
                        prev_customer, _, prev_start_time = prev_assignments[-1]
                        prev_errand_time = calculate_errand_time(prev_customer.desired_errand, prev_customer.location, prev_customer.location)
                        prev_end_time = prev_start_time + prev_errand_time
                        travel_time, _ = calculate_travel_time(prev_customer.location, customer.location)
                        best_start_time = max(best_start_time, prev_end_time + travel_time)

                    schedule.assignments.setdefault(day, []).append((customer, best_contractor, best_start_time))
                    best_contractor.location = customer.location
                    best_contractor.available_time = best_start_time + errand_time
                    print(f"    Scheduled with contractor {best_contractor.id} at start time {best_start_time}")
                    print(f"    Contractor {best_contractor.id} new available time: {best_contractor.available_time}")
                else:
                    print(f"    Could not schedule customer {customer.id} on day {day}")

    print("\nInitial scheduling process completed.")
    return schedule