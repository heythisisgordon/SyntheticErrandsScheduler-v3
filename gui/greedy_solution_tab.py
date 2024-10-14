"""
GreedySolutionTab: Displays the generated greedy solution and provides options for solution visualization.
"""

import wx
import wx.lib.scrolledpanel as scrolled
from typing import List
import logging

logger = logging.getLogger(__name__)

class GreedySolutionTab(scrolled.ScrolledPanel):
    def __init__(self, parent: wx.Window):
        super().__init__(parent, -1, style=wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER)
        self.vbox: wx.BoxSizer
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
        wx.PostEvent(self.GetParent(), wx.PyCommandEvent(wx.EVT_BUTTON.typeId, self.generate_button.GetId()))

    def display_solution(self, formatted_schedule: List[str], profit: float) -> None:
        logger.info("Updating GreedySolutionTab content")
        self.content_box.Clear(True)
        
        self.content_box.Add(wx.StaticText(self, label="Initial Greedy Schedule:"), flag=wx.ALL, border=5)
        
        for line in formatted_schedule:
            self.content_box.Add(wx.StaticText(self, label=line), flag=wx.ALL, border=2)

        self.content_box.Add(wx.StaticText(self, label=f"\nTotal Profit: ${profit:.2f}"), flag=wx.ALL, border=5)

        self.Layout()
        self.SetupScrolling(scroll_x=False, scroll_y=True, rate_y=20)
        self.Refresh()
        self.Update()
        logger.info("GreedySolutionTab content updated")

    def OnSize(self, event: wx.SizeEvent) -> None:
        self.SetupScrolling(scroll_x=False, scroll_y=True, rate_y=20)
        event.Skip()

    def visualize_solution(self, customers, contractors, schedule):
        # This method should be implemented to visualize the solution
        # It will be called by the controller when needed
        pass

    def show_error(self, message: str):
        wx.MessageBox(message, "Error", wx.OK | wx.ICON_ERROR)

    def show_warning(self, message: str):
        wx.MessageBox(message, "Warning", wx.OK | wx.ICON_WARNING)
