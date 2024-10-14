"""
ProblemGenerationTab: Displays the generated problem instance and allows for problem visualization.
"""

import wx
import wx.lib.scrolledpanel as scrolled
from typing import List, Tuple
from models.customer import Customer
from models.contractor import Contractor

class ProblemGenerationTab(scrolled.ScrolledPanel):
    def __init__(self, parent: wx.Window):
        super().__init__(parent, -1, style=wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER)
        self.vbox: wx.BoxSizer
        self.customers: List[Customer] = []
        self.contractors: List[Contractor] = []
        self.InitUI()

    def InitUI(self) -> None:
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        
        # Add "Generate Problem" button at the top
        self.generate_button = wx.Button(self, label="Generate Problem")
        self.generate_button.Bind(wx.EVT_BUTTON, self.OnGenerateProblem)
        self.vbox.Add(self.generate_button, 0, wx.ALL|wx.EXPAND, 5)
        
        self.content_box = wx.BoxSizer(wx.VERTICAL)
        self.vbox.Add(self.content_box, 1, wx.EXPAND)
        
        self.SetSizer(self.vbox)
        self.SetupScrolling(scroll_x=False, scroll_y=True, rate_y=20)
        self.SetMinSize((780, 500))  # Set a minimum size for the panel

    def OnGenerateProblem(self, event: wx.CommandEvent) -> None:
        wx.PostEvent(self.GetParent(), wx.PyCommandEvent(wx.EVT_BUTTON.typeId, self.generate_button.GetId()))

    def display_problem(self, customer_info: List[List[str]], contractor_info: List[str], contractor_rate_info: str) -> None:
        self.content_box.Clear(True)
        
        # Display customer information
        customer_section = wx.StaticBox(self, label="Customers")
        customer_sizer = wx.StaticBoxSizer(customer_section, wx.VERTICAL)
        
        for i, customer in enumerate(customer_info):
            customer_info_box = wx.StaticBox(self, label=f"Customer {i+1}")
            customer_info_sizer = wx.StaticBoxSizer(customer_info_box, wx.VERTICAL)
            
            for line in customer:
                customer_info_sizer.Add(wx.StaticText(self, label=line), flag=wx.ALL, border=2)
            
            customer_sizer.Add(customer_info_sizer, flag=wx.ALL|wx.EXPAND, border=5)
        
        self.content_box.Add(customer_sizer, flag=wx.ALL|wx.EXPAND, border=10)

        # Display contractor information
        contractor_section = wx.StaticBox(self, label="Contractors")
        contractor_sizer = wx.StaticBoxSizer(contractor_section, wx.VERTICAL)
        
        for info in contractor_info:
            contractor_sizer.Add(wx.StaticText(self, label=info), flag=wx.ALL, border=2)

        # Display contractor rate
        contractor_sizer.Add(wx.StaticText(self, label=contractor_rate_info), flag=wx.ALL, border=2)

        self.content_box.Add(contractor_sizer, flag=wx.ALL|wx.EXPAND, border=10)

        self.Layout()
        self.SetupScrolling(scroll_x=False, scroll_y=True, rate_y=20)
        self.Refresh()
        self.Update()

    def OnSize(self, event: wx.SizeEvent) -> None:
        self.SetupScrolling(scroll_x=False, scroll_y=True, rate_y=20)
        event.Skip()

    def visualize_problem(self, customers: List[Customer], contractors: List[Contractor]):
        # This method should be implemented to visualize the problem
        # It will be called by the controller when needed
        pass

    def show_error(self, message: str):
        wx.MessageBox(message, "Error", wx.OK | wx.ICON_ERROR)

    def set_problem_params(self, num_customers: int, num_contractors: int, contractor_rate: float):
        self.num_customers = num_customers
        self.num_contractors = num_contractors
        self.contractor_rate = contractor_rate

    def get_problem_params(self) -> Tuple[int, int, float]:
        return self.num_customers, self.num_contractors, self.contractor_rate
