from models.schedule import Schedule
from utils.travel_time import calculate_travel_time
from utils.errand_utils import calculate_errand_time
from datetime import datetime, timedelta

def initial_schedule(customers, contractors):
    schedule = Schedule(contractors, customers)
    today = datetime.now().date()

    for day in range(14):  # 14-day period
        current_date = today + timedelta(days=day)
        available_contractors = list(contractors)  # Reset available contractors each day
        
        # Sort customers by incentive (prioritize same-day errands)
        sorted_customers = sorted(customers, key=lambda c: c.desired_errand.incentive if current_date == today else 0, reverse=True)
        
        for customer in sorted_customers:
            if customer.id not in [assignment[0].id for assignments in schedule.assignments.values() for assignment in assignments]:
                best_contractor = None
                best_start_time = None
                
                for contractor in available_contractors:
                    contractor_schedule = [assignment for assignment in schedule.assignments.get(day, []) if assignment[1].id == contractor.id]
                    
                    if not contractor_schedule:
                        travel_time, _ = calculate_travel_time(contractor.location, customer.location)
                        start_time = max(480, 480 + travel_time)  # Start at 8am (480 minutes from midnight) or later if travel time is long
                    else:
                        last_customer, _, last_start_time = contractor_schedule[-1]
                        last_errand_time = calculate_errand_time(last_customer.desired_errand, last_customer.location, last_customer.location)
                        travel_time, _ = calculate_travel_time(last_customer.location, customer.location)
                        start_time = last_start_time + last_errand_time + travel_time

                    errand_time = calculate_errand_time(customer.desired_errand, customer.location, customer.location)
                    end_time = start_time + errand_time

                    if end_time <= 1020:  # 5pm (1020 minutes from midnight)
                        if best_contractor is None or start_time < best_start_time:
                            best_contractor = contractor
                            best_start_time = start_time

                if best_contractor:
                    schedule.assignments.setdefault(day, []).append((customer, best_contractor, best_start_time))
                    best_contractor.location = customer.location  # Update contractor's location
                    if len(available_contractors) > 1:
                        available_contractors.remove(best_contractor)  # Try to use other contractors if available

    return schedule