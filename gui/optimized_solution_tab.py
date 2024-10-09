import wx
import wx.lib.scrolledpanel as scrolled
from typing import List, Tuple, Dict
from models.customer import Customer
from models.contractor import Contractor
from models.schedule import Schedule
from models.master_contractor_calendar import MasterContractorCalendar
from algorithms.initial_greedy_scheduler import initial_greedy_schedule
from algorithms.CP_SAT_optimizer import optimize_schedule
from utils.schedule_analyzer import compare_schedules
from datetime import datetime, date
import logging

logger = logging.getLogger(__name__)

class OptimizedSolutionTab(scrolled.ScrolledPanel):
    def __init__(self, parent: wx.Window, main_frame) -> None:
        super().__init__(parent, -1, style=wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER)
        self.main_frame = main_frame
        self.vbox: wx.BoxSizer
        self.optimizer_choice: wx.Choice
        self.InitUI()

    def InitUI(self) -> None:
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        
        # Add optimizer selection dropdown
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.optimizer_choice = wx.Choice(self, choices=["CP-SAT Solver"])
        self.optimizer_choice.SetSelection(0)  # Default to CP-SAT Solver
        hbox.Add(wx.StaticText(self, label="Optimizer:"), flag=wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, border=8)
        hbox.Add(self.optimizer_choice)
        self.vbox.Add(hbox, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
        
        # Add "Optimize Greedy Solution" button
        self.optimize_button = wx.Button(self, label="Optimize Greedy Solution")
        self.optimize_button.Bind(wx.EVT_BUTTON, self.OnOptimizeGreedySolution)
        self.optimize_button.Disable()  # Initially disabled
        self.vbox.Add(self.optimize_button, 0, wx.ALL|wx.EXPAND, 5)
        
        self.content_box = wx.BoxSizer(wx.VERTICAL)
        self.vbox.Add(self.content_box, 1, wx.EXPAND)
        
        self.SetSizer(self.vbox)
        self.SetupScrolling(scroll_x=False, scroll_y=True, rate_y=20)
        self.SetMinSize((780, 500))  # Set a minimum size for the panel

    def enable_optimize_button(self) -> None:
        self.optimize_button.Enable()

    def OnOptimizeGreedySolution(self, event: wx.CommandEvent) -> None:
        # Get the generated problem from the problem generation tab
        customers = self.main_frame.problem_generation.customers
        contractors = self.main_frame.problem_generation.contractors
        
        # Get the selected optimizer
        optimizer = self.optimizer_choice.GetString(self.optimizer_choice.GetSelection())
        
        # Generate the optimized solution
        self.UpdateContent(customers, contractors, optimizer)

    def UpdateContent(self, customers: List[Customer], contractors: List[Contractor], optimizer: str) -> None:
        self.content_box.Clear(True)
        
        # Get the master calendar from the IMCS tab
        master_calendar = self.main_frame.imcs.master_calendar
        
        if not master_calendar:
            wx.MessageBox("Master calendar has not been initialized. Please initialize calendars first.", "Error", wx.OK | wx.ICON_ERROR)
            return
        
        # Generate initial greedy schedule
        initial_sched: Schedule = initial_greedy_schedule(customers, contractors, master_calendar)
        
        # Optimize schedule based on selected optimizer
        if optimizer == "CP-SAT Solver":
            initial_sched, optimized_sched = optimize_schedule(initial_sched, master_calendar)
        else:
            raise ValueError(f"Unknown optimizer: {optimizer}")
        
        # Display schedules side by side
        self.display_schedules_side_by_side(initial_sched, optimized_sched, optimizer)
        
        # Compare schedules
        self.display_schedule_comparison(initial_sched, optimized_sched)

        self.Layout()
        self.SetupScrolling(scroll_x=False, scroll_y=True, rate_y=20)
        self.Refresh()
        self.Update()

        # Update the Contractor Schedule tab
        self.main_frame.update_contractor_schedule(optimized_sched)

    def display_schedules_side_by_side(self, initial_sched: Schedule, optimized_sched: Schedule, optimizer: str) -> None:
        self.content_box.Add(wx.StaticText(self, label=f"Schedule Comparison ({optimizer}):"), flag=wx.ALL, border=5)
        
        grid_sizer = wx.GridSizer(rows=1, cols=2, hgap=10, vgap=10)
        
        initial_panel = self.create_schedule_panel(initial_sched, "Initial Greedy Schedule")
        optimized_panel = self.create_schedule_panel(optimized_sched, "Optimized Schedule")
        
        grid_sizer.Add(initial_panel, 0, wx.EXPAND)
        grid_sizer.Add(optimized_panel, 0, wx.EXPAND)
        
        self.content_box.Add(grid_sizer, 0, wx.EXPAND|wx.ALL, 10)

    def create_schedule_panel(self, schedule: Schedule, title: str) -> wx.Panel:
        panel = wx.Panel(self)
        box = wx.StaticBox(panel, label=title)
        sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        
        for day, assignments in schedule.assignments.items():
            if isinstance(day, date):
                day_str = day.strftime("%Y-%m-%d")
            else:
                day_str = f"Day {day + 1}"
            sizer.Add(wx.StaticText(panel, label=f"\n{day_str}:"), flag=wx.ALL, border=5)
            for customer, contractor, start_time in assignments:
                if isinstance(start_time, datetime):
                    time_str = start_time.strftime("%H:%M")
                else:
                    hours, minutes = divmod(start_time, 60)
                    time_str = f"{hours:02d}:{minutes:02d}"
                info: str = f"  C{customer.id}-T{contractor.id} @ {time_str}"
                sizer.Add(wx.StaticText(panel, label=info), flag=wx.ALL, border=2)
        
        panel.SetSizer(sizer)
        return panel

    def display_schedule_comparison(self, initial_sched: Schedule, optimized_sched: Schedule) -> None:
        initial_analysis, optimized_analysis, profit_difference = compare_schedules(initial_sched, optimized_sched)
        
        comparison_box = wx.StaticBox(self, label="Schedule Comparison")
        comparison_sizer = wx.StaticBoxSizer(comparison_box, wx.VERTICAL)
        
        metrics = [
            ("Total Travel Time (hours)", "total_travel_time"),
            ("Average Travel Time (hours)", "average_travel_time"),
            ("Total Errands", "total_errands"),
            ("Average Errands per Day", "average_errands_per_day"),
            ("Max Errands per Day", "max_errands_per_day"),
            ("Min Errands per Day", "min_errands_per_day"),
        ]
        
        for metric_name, metric_key in metrics:
            initial_value = initial_analysis[metric_key]
            optimized_value = optimized_analysis[metric_key]
            difference = optimized_value - initial_value
            comparison_sizer.Add(wx.StaticText(self, label=f"{metric_name}:"), flag=wx.ALL, border=2)
            comparison_sizer.Add(wx.StaticText(self, label=f"  Initial: {initial_value:.2f}"), flag=wx.ALL, border=2)
            comparison_sizer.Add(wx.StaticText(self, label=f"  Optimized: {optimized_value:.2f}"), flag=wx.ALL, border=2)
            comparison_sizer.Add(wx.StaticText(self, label=f"  Difference: {difference:.2f}"), flag=wx.ALL, border=2)
        
        initial_profit = initial_sched.calculate_total_profit()
        optimized_profit = optimized_sched.calculate_total_profit()
        
        comparison_sizer.Add(wx.StaticText(self, label=f"Total Profit:"), flag=wx.ALL, border=2)
        comparison_sizer.Add(wx.StaticText(self, label=f"  Initial: ${initial_profit:.2f}"), flag=wx.ALL, border=2)
        comparison_sizer.Add(wx.StaticText(self, label=f"  Optimized: ${optimized_profit:.2f}"), flag=wx.ALL, border=2)
        comparison_sizer.Add(wx.StaticText(self, label=f"  Difference: ${profit_difference:.2f}"), flag=wx.ALL, border=2)
        
        if profit_difference > 0:
            improvement_percentage = (profit_difference / initial_profit) * 100
            comparison_sizer.Add(wx.StaticText(self, label=f"Improvement Percentage: {improvement_percentage:.2f}%"), flag=wx.ALL, border=5)
        elif profit_difference == 0:
            comparison_sizer.Add(wx.StaticText(self, label="Note: The optimizer couldn't improve upon the initial greedy schedule."), flag=wx.ALL, border=5)
        else:
            decrease_percentage = (-profit_difference / initial_profit) * 100
            comparison_sizer.Add(wx.StaticText(self, label=f"Decrease Percentage: {decrease_percentage:.2f}%"), flag=wx.ALL, border=5)
            comparison_sizer.Add(wx.StaticText(self, label="Warning: The optimized schedule performed worse than the initial greedy schedule."), flag=wx.ALL, border=5)
        
        self.content_box.Add(comparison_sizer, 0, wx.EXPAND|wx.ALL, 10)
        
        logger.info(f"Optimization results: Initial profit: ${initial_profit:.2f}, Optimized profit: ${optimized_profit:.2f}, Difference: ${profit_difference:.2f}")

    def OnSize(self, event: wx.SizeEvent) -> None:
        self.SetupScrolling(scroll_x=False, scroll_y=True, rate_y=20)
        event.Skip()