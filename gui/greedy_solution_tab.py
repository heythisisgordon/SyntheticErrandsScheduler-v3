import wx
import wx.lib.scrolledpanel as scrolled
from typing import List
from models.customer import Customer
from models.contractor import Contractor
from models.schedule import Schedule
from controllers.greedy_solution_controller import GreedySolutionController
import logging

logger = logging.getLogger(__name__)

class GreedySolutionTab(scrolled.ScrolledPanel):
    def __init__(self, parent: wx.Window, main_frame) -> None:
        super().__init__(parent, -1, style=wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER)
        self.main_frame = main_frame
        self.controller = GreedySolutionController()
        self.vbox: wx.BoxSizer
        self.schedule: Schedule = None
        self.InitUI()
       
    def InitUI(self) -> None:
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        
        self.generate_button = wx.Button(self, label="Generate Greedy Solution")
        self.generate_button.Bind(wx.EVT_BUTTON, self.OnGenerateGreedySolution)
        self.generate_button.Disable()
        self.vbox.Add(self.generate_button, 0, wx.ALL|wx.EXPAND, 5)
        
        self.content_box = wx.BoxSizer(wx.VERTICAL)
        self.vbox.Add(self.content_box, 1, wx.EXPAND)
        
        self.SetSizer(self.vbox)
        self.SetupScrolling(scroll_x=False, scroll_y=True, rate_y=20)
        self.SetMinSize((780, 500))
     
    def enable_generate_button(self) -> None:
        self.generate_button.Enable()

    def disable_generate_button(self) -> None:
        self.generate_button.Disable()
   
    def OnGenerateGreedySolution(self, event: wx.CommandEvent) -> None:
        customers = self.main_frame.problem_generation.customers
        contractors = self.main_frame.problem_generation.contractors
        
        self.schedule, message = self.controller.generate_solution(customers, contractors)
        
        if self.schedule:
            self.UpdateContent(customers, contractors, self.schedule)
            self.main_frame.update_contractor_schedule(self.schedule)
            if message:
                wx.MessageBox(message, "Scheduling Information", wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox(message, "Scheduling Error", wx.OK | wx.ICON_ERROR)

    def UpdateContent(self, customers: List[Customer], contractors: List[Contractor], schedule: Schedule) -> None:
        logger.info("Updating GreedySolutionTab content")
        self.content_box.Clear(True)
        
        self.content_box.Add(wx.StaticText(self, label="Initial Greedy Schedule:"), flag=wx.ALL, border=5)
        
        formatted_schedule = self.controller.format_schedule(customers, contractors, schedule)
        for line in formatted_schedule:
            self.content_box.Add(wx.StaticText(self, label=line), flag=wx.ALL, border=2)

        profit: float = self.controller.calculate_profit(schedule)
        self.content_box.Add(wx.StaticText(self, label=f"\nTotal Profit: ${profit:.2f}"), flag=wx.ALL, border=5)

        self.Layout()
        self.SetupScrolling(scroll_x=False, scroll_y=True, rate_y=20)
        self.Refresh()
        self.Update()
        logger.info("GreedySolutionTab content updated")

    def OnSize(self, event: wx.SizeEvent) -> None:
        self.SetupScrolling(scroll_x=False, scroll_y=True, rate_y=20)
        event.Skip()
