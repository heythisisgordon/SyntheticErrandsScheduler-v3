import wx
import wx.lib.scrolledpanel as scrolled
from typing import List
from models.customer import Customer
from models.contractor import Contractor
from models.schedule import Schedule
from algorithms.initial_scheduler import initial_schedule
from algorithms.optimizer import optimize_schedule
from datetime import datetime, date

class OptimizedSolutionTab(scrolled.ScrolledPanel):
    def __init__(self, parent: wx.Window) -> None:
        super().__init__(parent, -1, style=wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER)
        self.vbox: wx.BoxSizer
        self.InitUI()

    def InitUI(self) -> None:
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.vbox)
        self.SetupScrolling(scroll_x=False, scroll_y=True, rate_y=20)
        self.SetMinSize((780, 500))  # Set a minimum size for the panel

    def UpdateContent(self, customers: List[Customer], contractors: List[Contractor]) -> None:
        self.vbox.Clear(True)
        
        # Generate initial schedule and optimize it
        initial_sched: Schedule = initial_schedule(customers, contractors)
        optimized_sched: Schedule = optimize_schedule(initial_sched)
        
        # Display optimized schedule information
        self.vbox.Add(wx.StaticText(self, label="Optimized Schedule:"), flag=wx.ALL, border=5)
        for day, assignments in optimized_sched.assignments.items():
            if isinstance(day, date):
                day_str = day.strftime("%Y-%m-%d")
            else:
                day_str = f"Day {day + 1}"
            self.vbox.Add(wx.StaticText(self, label=f"\n{day_str}:"), flag=wx.ALL, border=5)
            for customer, contractor, start_time in assignments:
                if isinstance(start_time, datetime):
                    time_str = start_time.strftime("%H:%M")
                else:
                    hours, minutes = divmod(start_time, 60)
                    time_str = f"{hours:02d}:{minutes:02d}"
                info: str = f"  Contractor {contractor.id} - Customer {customer.id}:"
                self.vbox.Add(wx.StaticText(self, label=info), flag=wx.ALL, border=2)
                info = f"    Errand: {customer.desired_errand.type}"
                self.vbox.Add(wx.StaticText(self, label=info), flag=wx.ALL, border=2)
                info = f"    Start Time: {time_str}"
                self.vbox.Add(wx.StaticText(self, label=info), flag=wx.ALL, border=2)
                info = f"    Location: {customer.location}"
                self.vbox.Add(wx.StaticText(self, label=info), flag=wx.ALL, border=2)

        initial_profit: float = initial_sched.calculate_total_profit()
        optimized_profit: float = optimized_sched.calculate_total_profit()
        profit_improvement: float = optimized_profit - initial_profit
        
        self.vbox.Add(wx.StaticText(self, label=f"\nInitial Profit: ${initial_profit:.2f}"), flag=wx.ALL, border=5)
        self.vbox.Add(wx.StaticText(self, label=f"Optimized Profit: ${optimized_profit:.2f}"), flag=wx.ALL, border=5)
        self.vbox.Add(wx.StaticText(self, label=f"Profit Improvement: ${profit_improvement:.2f}"), flag=wx.ALL, border=5)

        self.Layout()
        self.SetupScrolling(scroll_x=False, scroll_y=True, rate_y=20)
        self.Refresh()
        self.Update()

    def OnSize(self, event: wx.SizeEvent) -> None:
        self.SetupScrolling(scroll_x=False, scroll_y=True, rate_y=20)
        event.Skip()