import wx
import wx.lib.scrolledpanel as scrolled
from typing import List
from models.customer import Customer
from models.contractor import Contractor
from models.schedule import Schedule
from algorithms.initial_greedy_scheduler import initial_greedy_schedule
from algorithms.CP_SAT_optimizer import optimize_schedule
from algorithms.vehicle_routing_optimizer import optimize_schedule_vrp
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
        self.optimizer_choice = wx.Choice(self, choices=["CP-SAT Solver", "Vehicle Routing Solver"])
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
        
        # Generate initial greedy schedule
        initial_sched: Schedule = initial_greedy_schedule(customers, contractors)
        
        # Optimize schedule based on selected optimizer
        if optimizer == "CP-SAT Solver":
            optimized_sched: Schedule = optimize_schedule(initial_sched)
        elif optimizer == "Vehicle Routing Solver":
            optimized_sched: Schedule = optimize_schedule_vrp(initial_sched)
        else:
            raise ValueError(f"Unknown optimizer: {optimizer}")
        
        # Display optimized schedule information
        self.content_box.Add(wx.StaticText(self, label=f"Optimized Schedule ({optimizer}):"), flag=wx.ALL, border=5)
        
        if not optimized_sched.assignments:
            self.content_box.Add(wx.StaticText(self, label="No optimized schedule found. Displaying initial greedy schedule."), flag=wx.ALL, border=5)
            schedule_to_display = initial_sched
        else:
            schedule_to_display = optimized_sched

        for day, assignments in schedule_to_display.assignments.items():
            if isinstance(day, date):
                day_str = day.strftime("%Y-%m-%d")
            else:
                day_str = f"Day {day + 1}"
            self.content_box.Add(wx.StaticText(self, label=f"\n{day_str}:"), flag=wx.ALL, border=5)
            for customer, contractor, start_time in assignments:
                if isinstance(start_time, datetime):
                    time_str = start_time.strftime("%H:%M")
                else:
                    hours, minutes = divmod(start_time, 60)
                    time_str = f"{hours:02d}:{minutes:02d}"
                info: str = f"  Contractor {contractor.id} - Customer {customer.id}:"
                self.content_box.Add(wx.StaticText(self, label=info), flag=wx.ALL, border=2)
                info = f"    Errand: {customer.desired_errand.type}"
                self.content_box.Add(wx.StaticText(self, label=info), flag=wx.ALL, border=2)
                info = f"    Start Time: {time_str}"
                self.content_box.Add(wx.StaticText(self, label=info), flag=wx.ALL, border=2)
                info = f"    Location: {customer.location}"
                self.content_box.Add(wx.StaticText(self, label=info), flag=wx.ALL, border=2)

        initial_profit: float = initial_sched.calculate_total_profit()
        optimized_profit: float = optimized_sched.calculate_total_profit()
        profit_improvement: float = optimized_profit - initial_profit
        
        self.content_box.Add(wx.StaticText(self, label=f"\nInitial Greedy Schedule Profit: ${initial_profit:.2f}"), flag=wx.ALL, border=5)
        self.content_box.Add(wx.StaticText(self, label=f"Optimized Schedule Profit: ${optimized_profit:.2f}"), flag=wx.ALL, border=5)
        self.content_box.Add(wx.StaticText(self, label=f"Profit Improvement: ${profit_improvement:.2f}"), flag=wx.ALL, border=5)

        if profit_improvement == 0:
            self.content_box.Add(wx.StaticText(self, label="Note: The optimizer couldn't improve upon the initial greedy schedule."), flag=wx.ALL, border=5)

        logger.info(f"Optimization results: Initial greedy profit: ${initial_profit:.2f}, Optimized profit: ${optimized_profit:.2f}, Improvement: ${profit_improvement:.2f}")

        self.Layout()
        self.SetupScrolling(scroll_x=False, scroll_y=True, rate_y=20)
        self.Refresh()
        self.Update()

        # Update the Visualization tab
        self.main_frame.update_visualization(customers, contractors, optimized_sched)

    def OnSize(self, event: wx.SizeEvent) -> None:
        self.SetupScrolling(scroll_x=False, scroll_y=True, rate_y=20)
        event.Skip()