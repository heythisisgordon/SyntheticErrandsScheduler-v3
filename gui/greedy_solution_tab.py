import wx
import wx.lib.scrolledpanel as scrolled
from typing import List
from models.customer import Customer
from models.contractor import Contractor
from models.schedule import Schedule
from algorithms.initial_scheduler import initial_schedule
from datetime import datetime, date

class GreedySolutionTab(scrolled.ScrolledPanel):
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
        
        # Generate initial schedule
        schedule: Schedule = initial_schedule(customers, contractors)
        
        # Display schedule information
        self.vbox.Add(wx.StaticText(self, label="Initial Schedule:"), flag=wx.ALL, border=5)
        for day, assignments in schedule.assignments.items():
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

        profit: float = schedule.calculate_total_profit()
        self.vbox.Add(wx.StaticText(self, label=f"\nTotal Profit: ${profit:.2f}"), flag=wx.ALL, border=5)

        self.Layout()
        self.SetupScrolling(scroll_x=False, scroll_y=True, rate_y=20)
        self.Refresh()
        self.Update()

    def OnSize(self, event: wx.SizeEvent) -> None:
        self.SetupScrolling(scroll_x=False, scroll_y=True, rate_y=20)
        event.Skip()