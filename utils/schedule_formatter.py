from typing import List
from models.customer import Customer
from models.contractor import Contractor
from models.schedule import Schedule
from models.contractor_calendar import ErrandAssignment
from datetime import datetime
from constants import WORK_START_TIME_OBJ

class ScheduleFormatter:
    @staticmethod
    def format_schedule(schedule: Schedule) -> List[str]:
        formatted_schedule = []
        
        assignments = schedule.get_assignments()
        # Group assignments by day
        assignments_by_day = {}
        for errand, customer, contractor in assignments:
            day = errand.travel_start_time.date()
            if day not in assignments_by_day:
                assignments_by_day[day] = []
            assignments_by_day[day].append((errand, customer, contractor))
        
        for day, day_assignments in sorted(assignments_by_day.items()):
            day_str = day.strftime("%Y-%m-%d")
            formatted_schedule.append(f"\n{day_str}:")
            
            # Sort day_assignments by travel_start_time
            for errand, customer, contractor in sorted(day_assignments, key=lambda x: x[0].travel_start_time):
                formatted_schedule.extend([
                    f"  Contractor {contractor.id} - Customer {customer.id}:",
                    f"    Errand: {errand.errand_type}",
                    f"    Travel Start Time: {errand.travel_start_time.strftime('%H:%M:%S')}",
                    f"    Travel End Time: {errand.travel_end_time.strftime('%H:%M:%S')}",
                    f"    Task Start Time: {errand.task_start_time.strftime('%H:%M:%S')}",
                    f"    Task End Time: {errand.task_end_time.strftime('%H:%M:%S')}",
                    f"    Travel Duration: {errand.travel_duration}",
                    f"    Total Duration: {errand.total_duration}",
                    f"    Location: {customer.location}"
                ])
        
        return formatted_schedule

    @staticmethod
    def format_errand(errand: ErrandAssignment, customer: Customer, contractor: Contractor) -> str:
        return (f"C{customer.id}: {errand.errand_type}\n"
                f"Travel: {errand.travel_start_time.strftime('%H:%M')} - {errand.travel_end_time.strftime('%H:%M')}\n"
                f"Task: {errand.task_start_time.strftime('%H:%M')} - {errand.task_end_time.strftime('%H:%M')}")
