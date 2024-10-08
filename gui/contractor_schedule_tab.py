import wx
import wx.grid
from typing import List, Dict, Any
from models.schedule import Schedule
from models.contractor import Contractor
from models.customer import Customer
from models.errand import Errand
from datetime import datetime, time, timedelta
from utils.config_manager import ConfigManager
from utils.travel_time import calculate_travel_time
from constants import WORK_START_TIME_OBJ, WORK_END_TIME_OBJ
import logging

logger = logging.getLogger(__name__)

class ContractorScheduleTab(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.config = ConfigManager()
        self.init_ui()

    def init_ui(self):
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.grid = wx.grid.Grid(self)
        self.grid.CreateGrid(0, 0)
        self.grid.EnableScrolling(False, True)
        self.grid.ShowScrollbars(wx.SHOW_SB_NEVER, wx.SHOW_SB_ALWAYS)
        self.sizer.Add(self.grid, 1, wx.EXPAND | wx.ALL, 10)
        self.SetSizer(self.sizer)

    def update_schedule(self, schedule: Schedule):
        self.grid.ClearGrid()
        if self.grid.GetNumberRows() > 0:
            self.grid.DeleteRows(0, self.grid.GetNumberRows())
        if self.grid.GetNumberCols() > 0:
            self.grid.DeleteCols(0, self.grid.GetNumberCols())

        contractors = schedule.contractors
        days = sorted(schedule.assignments.keys())

        # Create columns for each contractor
        self.grid.AppendCols(len(contractors))
        for col, contractor in enumerate(contractors):
            self.grid.SetColLabelValue(col, f"Contractor {contractor.id}")

        # Use WORK_START_TIME_OBJ and WORK_END_TIME_OBJ
        work_start = WORK_START_TIME_OBJ
        work_end = WORK_END_TIME_OBJ

        hours_per_day = work_end.hour - work_start.hour + (work_end.minute - work_start.minute) / 60
        total_rows = len(days) * int(hours_per_day)
        self.grid.AppendRows(total_rows)

        # Set row labels
        for day_index, day in enumerate(days):
            for hour in range(int(hours_per_day)):
                row = day_index * int(hours_per_day) + hour
                current_time = datetime.combine(day, work_start) + timedelta(hours=hour)
                self.grid.SetRowLabelValue(row, f"{day.strftime('%Y-%m-%d')} {current_time.strftime('%I:%M %p')}")

        # Fill in the grid with errand information
        for day_index, day in enumerate(days):
            assignments = schedule.assignments[day]
            for customer, contractor, start_time in assignments:
                col = contractors.index(contractor)
                start_hour = (start_time - datetime.combine(day, work_start)).total_seconds() / 3600
                start_row = day_index * int(hours_per_day) + int(start_hour)
                
                errand = customer.desired_errand
                end_time = schedule.get_errand_end_time(customer, contractor, start_time)
                duration_hours = (end_time - start_time).total_seconds() / 3600
                end_row = start_row + int(duration_hours)
                
                # Set the errand information in the first cell
                self.grid.SetCellValue(start_row, col, self.format_errand(customer, contractor, start_time, end_time))
                
                # Color all cells for the duration of the errand
                for row in range(start_row, min(end_row + 1, total_rows)):
                    self.grid.SetCellBackgroundColour(row, col, wx.LIGHT_GREY)

        self.grid.AutoSize()

    def format_errand(self, customer: Customer, contractor: Contractor, start_time: datetime, end_time: datetime) -> str:
        errand = customer.desired_errand
        travel_time, _ = calculate_travel_time(contractor.location, customer.location)
        travel_start = start_time - travel_time
        travel_end = start_time
        return f"{errand.type.name}\nTravel Start: {travel_start.strftime('%I:%M %p')}\nTravel End: {travel_end.strftime('%I:%M %p')}\nErrand Start: {start_time.strftime('%I:%M %p')}\nErrand End: {end_time.strftime('%I:%M %p')}"
