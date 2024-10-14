from typing import List, Tuple
from models.schedule import Schedule
from models.contractor import Contractor
from datetime import datetime, timedelta
from constants import WORK_START_TIME_OBJ, WORK_END_TIME_OBJ
from utils.schedule_formatter import ScheduleFormatter
from collections import defaultdict

class ContractorScheduleFormatter:
    @staticmethod
    def format_grid(schedule: Schedule) -> Tuple[List[str], List[str], List[List[str]], List[List[str]]]:
        contractors = schedule.contractors
        
        # Group assignments by day
        assignments_by_day = defaultdict(list)
        for start_time, customer, contractor in schedule.assignments:
            day = start_time.date()
            assignments_by_day[day].append((start_time, customer, contractor))
        
        days = sorted(assignments_by_day.keys())

        # Column labels
        col_labels = [f"Contractor {contractor.id}" for contractor in contractors]

        # Calculate work hours
        work_start = WORK_START_TIME_OBJ
        work_end = WORK_END_TIME_OBJ
        hours_per_day = work_end.hour - work_start.hour + (work_end.minute - work_start.minute) / 60

        # Row labels
        row_labels = []
        for day in days:
            for hour in range(int(hours_per_day)):
                current_time = datetime.combine(day, work_start) + timedelta(hours=hour)
                row_labels.append(f"{day.strftime('%Y-%m-%d')} {current_time.strftime('%I:%M %p')}")

        # Initialize grid data and colors
        grid_data = [['' for _ in range(len(contractors))] for _ in range(len(row_labels))]
        grid_colors = [[None for _ in range(len(contractors))] for _ in range(len(row_labels))]

        # Fill in the grid with errand information
        for day_index, day in enumerate(days):
            assignments = assignments_by_day[day]
            for start_time, customer, contractor in assignments:
                col = contractors.index(contractor)
                start_hour = (start_time - datetime.combine(day, work_start)).total_seconds() / 3600
                start_row = day_index * int(hours_per_day) + int(start_hour)
                
                end_time = schedule.get_errand_end_time(customer, contractor, start_time)
                duration_hours = (end_time - start_time).total_seconds() / 3600
                end_row = start_row + int(duration_hours)
                
                # Set the errand information in the first cell
                grid_data[start_row][col] = ScheduleFormatter.format_errand(customer, contractor, start_time, end_time)
                
                # Color all cells for the duration of the errand
                for row in range(start_row, min(end_row + 1, len(row_labels))):
                    grid_colors[row][col] = 'LIGHT_GREY'

        return col_labels, row_labels, grid_data, grid_colors
