import wx
import wx.lib.scrolledpanel as scrolled
from typing import List
from models.customer import Customer
from models.contractor import Contractor
from models.schedule import Schedule
from algorithms.initial_greedy_scheduler import initial_greedy_schedule
from datetime import datetime, date

class GreedySolutionTab(scrolled.ScrolledPanel):
    def __init__(self, parent: wx.Window, main_frame) -> None:
        super().__init__(parent, -1, style=wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER)
        self.main_frame = main_frame
        self.vbox: wx.BoxSizer
        self.InitUI()

    def InitUI(self) -> None:
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        
        # Add "Generate Greedy Solution" button at the top
        self.generate_button = wx.Button(self, label="Generate Greedy Solution")
        self.generate_button.Bind(wx.EVT_BUTTON, self.OnGenerateGreedySolution)
        self.generate_button.Disable()  # Initially disabled
        self.vbox.Add(self.generate_button, 0, wx.ALL|wx.EXPAND, 5)
        
        self.content_box = wx.BoxSizer(wx.VERTICAL)
        self.vbox.Add(self.content_box, 1, wx.EXPAND)
        
        self.SetSizer(self.vbox)
        self.SetupScrolling(scroll_x=False, scroll_y=True, rate_y=20)
        self.SetMinSize((780, 500))  # Set a minimum size for the panel

    def enable_generate_button(self) -> None:
        self.generate_button.Enable()

    def OnGenerateGreedySolution(self, event: wx.CommandEvent) -> None:
        # Get the generated problem from the problem generation tab
        customers = self.main_frame.problem_generation.customers
        contractors = self.main_frame.problem_generation.contractors
        
        # Generate the greedy solution
        self.UpdateContent(customers, contractors)
        
        # Enable the "Optimize Greedy Solution" button
        self.main_frame.enable_optimized_solution()

    def UpdateContent(self, customers: List[Customer], contractors: List[Contractor]) -> None:
        self.content_box.Clear(True)
        
        # Generate initial greedy schedule
        schedule: Schedule = initial_greedy_schedule(customers, contractors)
        
        # Display schedule information
        self.content_box.Add(wx.StaticText(self, label="Initial Greedy Schedule:"), flag=wx.ALL, border=5)
        for day, assignments in schedule.assignments.items():
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

        profit: float = schedule.calculate_total_profit()
        self.content_box.Add(wx.StaticText(self, label=f"\nTotal Profit: ${profit:.2f}"), flag=wx.ALL, border=5)

        self.Layout()
        self.SetupScrolling(scroll_x=False, scroll_y=True, rate_y=20)
        self.Refresh()
        self.Update()

    def OnSize(self, event: wx.SizeEvent) -> None:
        self.SetupScrolling(scroll_x=False, scroll_y=True, rate_y=20)
        event.Skip()