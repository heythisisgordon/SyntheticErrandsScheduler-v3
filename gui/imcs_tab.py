import wx
import wx.grid
from datetime import datetime, timedelta
from utils.calendar_initialization import initialize_calendars
from constants import WORK_START_TIME_OBJ, WORK_END_TIME_OBJ, SCHEDULING_DAYS

class IMCSTab(wx.Panel):
    def __init__(self, parent, main_frame, problem_generation_tab):
        super().__init__(parent)
        self.main_frame = main_frame
        self.problem_generation_tab = problem_generation_tab
        self.contractor_calendars = None
        self.init_ui()

    def init_ui(self):
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Initialize Calendars button
        self.init_button = wx.Button(self, label="Initialize Calendars")
        self.init_button.Bind(wx.EVT_BUTTON, self.on_initialize_calendars)
        self.init_button.Disable()  # Initially disabled
        vbox.Add(self.init_button, 0, wx.ALL | wx.EXPAND, 5)

        # Grid for displaying calendar data
        self.grid = wx.grid.Grid(self)
        self.grid.CreateGrid(1, 1)  # Create a minimal grid initially
        vbox.Add(self.grid, 1, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(vbox)

    def enable_init_button(self):
        self.init_button.Enable()

    def on_initialize_calendars(self, event):
        if not hasattr(self.problem_generation_tab, 'contractors') or not self.problem_generation_tab.contractors:
            wx.MessageBox("Please generate a problem first.", "No Contractors", wx.OK | wx.ICON_WARNING)
            return

        contractors = self.problem_generation_tab.contractors
        self.contractor_calendars = initialize_calendars(contractors)
        self.update_schedule()
        self.main_frame.enable_generate_greedy_solution()

    def update_schedule(self):
        if not self.contractor_calendars:
            return

        contractors = list(self.contractor_calendars.keys())
        num_contractors = len(contractors)
        num_days = SCHEDULING_DAYS
        num_slots = int((WORK_END_TIME_OBJ.hour - WORK_START_TIME_OBJ.hour))

        # Resize the grid
        current_rows = self.grid.GetNumberRows()
        current_cols = self.grid.GetNumberCols()
        new_rows = num_days * num_slots
        new_cols = num_contractors

        if new_rows < current_rows:
            self.grid.DeleteRows(new_rows, current_rows - new_rows)
        elif new_rows > current_rows:
            self.grid.AppendRows(new_rows - current_rows)

        if new_cols < current_cols:
            self.grid.DeleteCols(new_cols, current_cols - new_cols)
        elif new_cols > current_cols:
            self.grid.AppendCols(new_cols - current_cols)

        # Clear existing cell contents and colors
        self.grid.ClearGrid()

        # Set column labels (contractor IDs)
        for col, contractor_id in enumerate(contractors):
            self.grid.SetColLabelValue(col, f"Contractor {contractor_id}")

        # Set row labels (day and time) and fill the grid with availability data
        start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        for day in range(num_days):
            current_date = start_date + timedelta(days=day)
            for slot in range(num_slots):
                row = day * num_slots + slot
                current_time = current_date.replace(hour=WORK_START_TIME_OBJ.hour + slot, minute=0)
                self.grid.SetRowLabelValue(row, f"{current_date.date()} {current_time.time()}")

                for col, contractor_id in enumerate(contractors):
                    contractor_calendar = self.contractor_calendars[contractor_id]
                    is_available = contractor_calendar.is_available(current_time, current_time + timedelta(hours=1))
                    cell_color = wx.GREEN if is_available else wx.RED
                    self.grid.SetCellBackgroundColour(row, col, cell_color)
                    self.grid.SetCellValue(row, col, "Available" if is_available else "Unavailable")

        self.grid.AutoSize()
        self.Layout()  # Ensure the panel layout is updated
