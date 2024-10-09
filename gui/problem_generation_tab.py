import wx
import wx.lib.scrolledpanel as scrolled
from typing import List
from models.customer import Customer
from models.contractor import Contractor
from utils.problem_generator import generate_problem
from utils.config_manager import ConfigManager

class ProblemGenerationTab(scrolled.ScrolledPanel):
    def __init__(self, parent: wx.Window, main_frame) -> None:
        super().__init__(parent, -1, style=wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER)
        self.main_frame = main_frame
        self.config_manager = ConfigManager()
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
        contractor_rate = self.main_frame.problem_definition.get_contractor_rate()
        
        # Generate the problem
        self.customers, self.contractors = generate_problem(num_customers, num_contractors, contractor_rate)
        
        # Update the content with the generated problem
        self.UpdateContent(self.customers, self.contractors)
        
        # Disable the "Generate Greedy Solution" button
        self.main_frame.greedy_solution.disable_generate_button()
        
        # Enable the "Initialize Calendars" button in the IMCS tab
        self.main_frame.imcs.enable_init_button()

    def UpdateContent(self, customers: List[Customer], contractors: List[Contractor]) -> None:
        self.content_box.Clear(True)
        
        # Display customer information
        customer_section = wx.StaticBox(self, label="Customers")
        customer_sizer = wx.StaticBoxSizer(customer_section, wx.VERTICAL)
        
        for customer in customers:
            customer_info = wx.StaticBox(self, label=f"Customer {customer.id}")
            customer_info_sizer = wx.StaticBoxSizer(customer_info, wx.VERTICAL)
            
            info: List[str] = [
                f"Location: {customer.location}",
                f"Errand: {customer.desired_errand.type.name}",
                f"Base Time: {customer.desired_errand.base_time}",
                f"Charge: ${customer.desired_errand.charge:.2f}"
            ]
            
            for line in info:
                customer_info_sizer.Add(wx.StaticText(self, label=line), flag=wx.ALL, border=2)
            
            customer_sizer.Add(customer_info_sizer, flag=wx.ALL|wx.EXPAND, border=5)
        
        self.content_box.Add(customer_sizer, flag=wx.ALL|wx.EXPAND, border=10)

        # Display contractor information
        contractor_section = wx.StaticBox(self, label="Contractors")
        contractor_sizer = wx.StaticBoxSizer(contractor_section, wx.VERTICAL)
        
        for contractor in contractors:
            info: str = f"Contractor {contractor.id}: Location {contractor.location}"
            contractor_sizer.Add(wx.StaticText(self, label=info), flag=wx.ALL, border=2)

        # Display contractor rate
        contractor_rate = self.main_frame.problem_definition.get_contractor_rate()
        rate_info: str = f"Contractor Rate: ${contractor_rate:.2f} per minute"
        contractor_sizer.Add(wx.StaticText(self, label=rate_info), flag=wx.ALL, border=2)

        self.content_box.Add(contractor_sizer, flag=wx.ALL|wx.EXPAND, border=10)

        self.Layout()
        self.SetupScrolling(scroll_x=False, scroll_y=True, rate_y=20)
        self.Refresh()
        self.Update()

    def OnSize(self, event: wx.SizeEvent) -> None:
        self.SetupScrolling(scroll_x=False, scroll_y=True, rate_y=20)
        event.Skip()