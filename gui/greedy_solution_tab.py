import wx
import wx.lib.scrolledpanel as scrolled
from typing import List
from models.customer import Customer
from models.contractor import Contractor
from models.schedule import Schedule
from algorithms.initial_greedy_scheduler import initial_greedy_schedule
from datetime import datetime, date, timedelta
from utils.travel_time import calculate_travel_time
from constants import WORK_START_TIME_OBJ, WORK_END_TIME_OBJ
import logging

logger = logging.getLogger(__name__)

class GreedySolutionTab(scrolled.ScrolledPanel):
    def __init__(self, parent: wx.Window, main_frame) -> None:
        super().__init__(parent, -1, style=wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER)
        self.main_frame = main_frame
        self.vbox: wx.BoxSizer
        self.schedule: Schedule = None
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
        logger.info("Generating greedy solution")
        # Get the generated problem from the problem generation tab
        customers = self.main_frame.problem_generation.customers
        contractors = self.main_frame.problem_generation.contractors
        
        logger.debug(f"Number of customers: {len(customers)}")
        logger.debug(f"Number of contractors: {len(contractors)}")
        
        # Generate the greedy solution
        self.schedule = initial_greedy_schedule(customers, contractors)
        
        # Update the content of this tab
        self.UpdateContent(customers, contractors, self.schedule)
        
        # Update the contractor schedule tab
        self.main_frame.update_contractor_schedule(self.schedule)
        
        # Enable the "Optimize Greedy Solution" button
        logger.debug("Enabling Optimize Greedy Solution button")
        self.main_frame.enable_optimized_solution()

    def UpdateContent(self, customers: List[Customer], contractors: List[Contractor], schedule: Schedule) -> None:
        logger.info("Updating GreedySolutionTab content")
        self.content_box.Clear(True)
        
        # Display schedule information
        self.content_box.Add(wx.StaticText(self, label="Initial Greedy Schedule:"), flag=wx.ALL, border=5)
        for day, assignments in schedule.assignments.items():
            if isinstance(day, (date, datetime)):
                day_str = day.strftime("%Y-%m-%d")
            else:
                day_str = f"Day {day + 1}"
            self.content_box.Add(wx.StaticText(self, label=f"\n{day_str}:"), flag=wx.ALL, border=5)
            
            for contractor in contractors:
                prev_location = contractor.initial_location
                contractor_assignments = [a for a in assignments if a[1].id == contractor.id]
                
                for customer, _, start_time in contractor_assignments:
                    # Add a separator line
                    self.content_box.Add(wx.StaticLine(self), flag=wx.EXPAND|wx.ALL, border=5)
                    
                    # Calculate travel time
                    travel_time, _ = calculate_travel_time(prev_location, customer.location)
                    
                    # Calculate times
                    work_start_time = datetime.combine(day, WORK_START_TIME_OBJ)
                    travel_start_time = max(work_start_time, start_time - travel_time)
                    travel_end_time = start_time
                    errand_start_time = start_time
                    errand_end_time = errand_start_time + customer.desired_errand.base_time
                    
                    # Format times
                    time_format = "%H:%M:%S"
                    travel_start_str = travel_start_time.strftime(time_format)
                    travel_end_str = travel_end_time.strftime(time_format)
                    errand_start_str = errand_start_time.strftime(time_format)
                    errand_end_str = errand_end_time.strftime(time_format)
                    
                    # Display information
                    info: str = f"Contractor {contractor.id} - Customer {customer.id}:"
                    self.content_box.Add(wx.StaticText(self, label=info), flag=wx.ALL, border=2)
                    info = f"  Errand: {customer.desired_errand.type}"
                    self.content_box.Add(wx.StaticText(self, label=info), flag=wx.ALL, border=2)
                    info = f"  Travel Start Time: {travel_start_str}"
                    self.content_box.Add(wx.StaticText(self, label=info), flag=wx.ALL, border=2)
                    info = f"  Travel End Time: {travel_end_str}"
                    self.content_box.Add(wx.StaticText(self, label=info), flag=wx.ALL, border=2)
                    info = f"  Errand Start Time: {errand_start_str}"
                    self.content_box.Add(wx.StaticText(self, label=info), flag=wx.ALL, border=2)
                    info = f"  Errand End Time: {errand_end_str}"
                    self.content_box.Add(wx.StaticText(self, label=info), flag=wx.ALL, border=2)
                    info = f"  Location: {customer.location}"
                    self.content_box.Add(wx.StaticText(self, label=info), flag=wx.ALL, border=2)
                    
                    logger.debug(f"Contractor {contractor.id} - Customer {customer.id}: "
                                 f"Travel Start: {travel_start_str}, Travel End: {travel_end_str}, "
                                 f"Errand Start: {errand_start_str}, Errand End: {errand_end_str}")
                    
                    prev_location = customer.location

        profit: float = schedule.calculate_total_profit()
        self.content_box.Add(wx.StaticText(self, label=f"\nTotal Profit: ${profit:.2f}"), flag=wx.ALL, border=5)

        self.Layout()
        self.SetupScrolling(scroll_x=False, scroll_y=True, rate_y=20)
        self.Refresh()
        self.Update()
        logger.info("GreedySolutionTab content updated")

    def OnSize(self, event: wx.SizeEvent) -> None:
        self.SetupScrolling(scroll_x=False, scroll_y=True, rate_y=20)
        event.Skip()