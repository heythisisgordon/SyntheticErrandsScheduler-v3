from typing import List, Tuple
from models.schedule import Schedule
from models.contractor import Contractor
from models.customer import Customer
from models.contractor_calendar import ErrandAssignment
from constants import WORK_START_TIME_OBJ, WORK_END_TIME_OBJ
from utils.schedule_formatter import ScheduleFormatter
import pandas as pd

class ContractorScheduleFormatter:
    @staticmethod
    def format_grid(schedule: Schedule) -> Tuple[List[str], List[str], List[List[str]], List[List[str]]]:
        contractors = schedule.contractors
        assignments = schedule.get_assignments()
        
        # Convert assignments to a DataFrame
        df = pd.DataFrame([
            {
                'day': errand.travel_start_time.floor('D'),
                'contractor_id': contractor.id,
                'errand': errand,
                'customer': customer,
                'contractor': contractor,
                'start_time': errand.travel_start_time,
                'end_time': errand.task_end_time
            }
            for errand, customer, contractor in assignments
        ])
        
        if df.empty:
            return [], [], [], []

        # Calculate work hours
        work_start = WORK_START_TIME_OBJ
        work_end = WORK_END_TIME_OBJ
        hours_per_day = int((work_end - work_start).total_seconds() / 3600)

        # Create a date range for all days
        date_range = pd.date_range(df['day'].min(), df['day'].max())

        # Create a time range for work hours
        time_range = pd.date_range(work_start, work_end, freq='H').time

        # Create a MultiIndex for the grid
        multi_index = pd.MultiIndex.from_product([date_range, time_range], names=['date', 'time'])

        # Create an empty DataFrame for the grid
        grid = pd.DataFrame(index=multi_index, columns=[f"Contractor {c.id}" for c in contractors])

        # Fill the grid with errand information
        for _, row in df.iterrows():
            errand_info = ScheduleFormatter.format_errand(row['errand'], row['customer'], row['contractor'])
            mask = (grid.index.get_level_values('date') == row['day']) & \
                   (grid.index.get_level_values('time') >= row['start_time'].time()) & \
                   (grid.index.get_level_values('time') < row['end_time'].time())
            grid.loc[mask, f"Contractor {row['contractor_id']}"] = errand_info

        # Prepare the output format
        col_labels = ["Day"] + list(grid.columns)
        row_labels = [f"{date.strftime('%Y-%m-%d')} {time.strftime('%I:%M %p')}" 
                      for date, time in grid.index]
        
        grid_data = [[date.strftime('%Y-%m-%d') if time == grid.index.get_level_values('time')[0] else ''] + 
                     [str(grid.loc[(date, time), col]) if pd.notna(grid.loc[(date, time), col]) else '' 
                      for col in grid.columns]
                     for date, time in grid.index]
        
        grid_colors = [['LIGHT_BLUE' if time == grid.index.get_level_values('time')[0] else 'WHITE'] + 
                       ['LIGHT_GREEN' if pd.notna(grid.loc[(date, time), col]) else 'WHITE' 
                        for col in grid.columns]
                       for date, time in grid.index]

        return col_labels, row_labels, grid_data, grid_colors
