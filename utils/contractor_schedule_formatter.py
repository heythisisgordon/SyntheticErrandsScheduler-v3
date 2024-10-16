from typing import List, Tuple
from models.schedule import Schedule
from models.contractor import Contractor
from models.customer import Customer
from models.contractor_calendar import ErrandAssignment
from datetime import datetime, timedelta, date
from constants import WORK_START_TIME_OBJ, WORK_END_TIME_OBJ
from utils.schedule_formatter import ScheduleFormatter

class ContractorScheduleFormatter:
    @staticmethod
    def format_grid(schedule: Schedule) -> Tuple[List[str], List[str], List[List[str]], List[List[str]]]:
        contractors = schedule.contractors
        assignments = schedule.get_assignments()
        
        # Group assignments by day and contractor
        assignments_by_day_contractor = {}
        for errand, customer, contractor in assignments:
            day = errand.travel_start_time.date()
            if day not in assignments_by_day_contractor:
                assignments_by_day_contractor[day] = {c.id: [] for c in contractors}
            assignments_by_day_contractor[day][contractor.id].append((errand, customer, contractor))
        
        days = sorted(assignments_by_day_contractor.keys())

        # Column labels
        col_labels = ["Day"] + [f"Contractor {contractor.id}" for contractor in contractors]

        # Calculate work hours
        work_start = WORK_START_TIME_OBJ
        work_end = WORK_END_TIME_OBJ
        hours_per_day = work_end.hour - work_start.hour + (work_end.minute - work_start.minute) / 60

        # Row labels
        row_labels = []
        for day in days:
            for hour in range(int(hours_per_day)):
                current_time = datetime.combine(day, work_start) + timedelta(hours=hour)
                row_labels.append(f"{current_time.strftime('%I:%M %p')}")

        # Initialize grid data and colors
        grid_data = [['' for _ in range(len(col_labels))] for _ in range(len(row_labels))]
        grid_colors = [['WHITE' for _ in range(len(col_labels))] for _ in range(len(row_labels))]

        # Fill in the day column
        for day_index, day in enumerate(days):
            start_row = day_index * int(hours_per_day)
            grid_data[start_row][0] = day.strftime('%Y-%m-%d')
            for row in range(start_row, start_row + int(hours_per_day)):
                grid_colors[row][0] = 'LIGHT_BLUE'

        # Fill in the grid with errand information
        for day_index, day in enumerate(days):
            for contractor in contractors:
                col = contractor.id + 1  # +1 for day column
                day_assignments = assignments_by_day_contractor[day][contractor.id]
                
                # Sort day_assignments by travel_start_time
                for errand, customer, _ in sorted(day_assignments, key=lambda x: x[0].travel_start_time):
                    start_hour = (errand.travel_start_time - datetime.combine(day, work_start)).total_seconds() / 3600
                    start_row = day_index * int(hours_per_day) + int(start_hour)
                    
                    duration_hours = errand.total_duration.total_seconds() / 3600
                    end_row = start_row + int(duration_hours)
                    
                    # Format errand information
                    errand_info = ScheduleFormatter.format_errand(errand, customer, contractor)
                    
                    # Add errand information only to the first cell
                    if not grid_data[start_row][col]:
                        grid_data[start_row][col] = errand_info
                    else:
                        grid_data[start_row][col] += "\n" + errand_info
                    
                    # Color all cells for the duration of the errand
                    for row in range(start_row, min(end_row + 1, len(row_labels))):
                        grid_colors[row][col] = 'LIGHT_GREEN'

        return col_labels, row_labels, grid_data, grid_colors
