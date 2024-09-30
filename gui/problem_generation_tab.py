import wx
import wx.lib.scrolledpanel as scrolled
from typing import List
from models.customer import Customer
from models.contractor import Contractor
from utils.problem_generator import generate_problem

class ProblemGenerationTab(scrolled.ScrolledPanel):
    def __init__(self, parent: wx.Window, main_frame) -> None:
        super().__init__(parent, -1, style=wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER)
        self.main_frame = main_frame
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
        # Get the problem parameters from the problem definition tab
        num_customers = self.main_frame.problem_definition.get_num_customers()
        num_contractors = self.main_frame.problem_definition.get_num_contractors()
        
        # Generate the problem
        self.customers, self.contractors = generate_problem(num_customers, num_contractors)
        
        # Update the content with the generated problem
        self.UpdateContent(self.customers, self.contractors)
        
        # Enable the "Generate Greedy Solution" button
        self.main_frame.enable_greedy_solution()

    def UpdateContent(self, customers: List[Customer], contractors: List[Contractor]) -> None:
        self.content_box.Clear(True)
        
        # Display customer information
        self.content_box.Add(wx.StaticText(self, label="Customers:"), flag=wx.ALL, border=5)
        for customer in customers:
            info: str = f"Customer {customer.id}: Location {customer.location}, " \
                   f"Errand: {customer.desired_errand.type}, " \
                   f"Base Time: {customer.desired_errand.base_time}, " \
                   f"Charge: ${customer.desired_errand.charge:.2f}"
            self.content_box.Add(wx.StaticText(self, label=info), flag=wx.ALL, border=5)

        # Display contractor information
        self.content_box.Add(wx.StaticText(self, label="\nContractors:"), flag=wx.ALL, border=5)
        for contractor in contractors:
            info: str = f"Contractor {contractor.id}: Location {contractor.location}"
            self.content_box.Add(wx.StaticText(self, label=info), flag=wx.ALL, border=5)

        self.Layout()
        self.SetupScrolling(scroll_x=False, scroll_y=True, rate_y=20)
        self.Refresh()
        self.Update()

    def OnSize(self, event: wx.SizeEvent) -> None:
        self.SetupScrolling(scroll_x=False, scroll_y=True, rate_y=20)
        event.Skip()