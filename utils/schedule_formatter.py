from typing import List, Tuple
from models.customer import Customer
from models.contractor import Contractor
from models.schedule import Schedule
from datetime import datetime, date
from utils.travel_time import calculate_travel_time
from constants import WORK_START_TIME_OBJ
from collections import defaultdict

class ScheduleFormatter:
    @staticmethod
    def format_schedule(customers: List[Customer], contractors: List[Contractor], schedule: Schedule) -> List[str]:
        formatted_schedule = []
        
        # Group assignments by day
        assignments_by_day = defaultdict(list)
        for start_time, customer, contractor in schedule.assignments:
            day = start_time.date()
            assignments_by_day[day].append((start_time, customer, contractor))
        
        for day, assignments in sorted(assignments_by_day.items()):
            day_str = day.strftime("%Y-%m-%d")
            formatted_schedule.append(f"\n{day_str}:")
            
            for contractor in contractors:
                prev_location = contractor.initial_location
                contractor_assignments = [a for a in assignments if a[2].id == contractor.id]
                
                for start_time, customer, _ in contractor_assignments:
                    formatted_schedule.append("----------------------------------------")
                    
                    travel_time, _ = calculate_travel_time(prev_location, customer.location)
                    
                    work_start_time = datetime.combine(day, WORK_START_TIME_OBJ)
                    travel_start_time = max(work_start_time, start_time - travel_time)
                    travel_end_time = start_time
                    errand_start_time = start_time
                    errand_end_time = errand_start_time + customer.desired_errand.base_time
                    
                    time_format = "%H:%M:%S"
                    travel_start_str = travel_start_time.strftime(time_format)
                    travel_end_str = travel_end_time.strftime(time_format)
                    errand_start_str = errand_start_time.strftime(time_format)
                    errand_end_str = errand_end_time.strftime(time_format)
                    
                    formatted_schedule.extend([
                        f"Contractor {contractor.id} - Customer {customer.id}:",
                        f"  Errand: {customer.desired_errand.type}",
                        f"  Travel Start Time: {travel_start_str}",
                        f"  Travel End Time: {travel_end_str}",
                        f"  Errand Start Time: {errand_start_str}",
                        f"  Errand End Time: {errand_end_str}",
                        f"  Location: {customer.location}"
                    ])
                    
                    prev_location = customer.location
        
        return formatted_schedule

    @staticmethod
    def format_errand(customer: Customer, contractor: Contractor, start_time: datetime, end_time: datetime) -> str:
        return f"C{customer.id}: {customer.desired_errand.type}\n{start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}"
