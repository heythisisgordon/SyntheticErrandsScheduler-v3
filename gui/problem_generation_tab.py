import wx
import wx.lib.scrolledpanel as scrolled
from typing import List
from models.customer import Customer
from models.contractor import Contractor
from controllers.problem_generation_controller import ProblemGenerationController

class ProblemGenerationTab(scrolled.ScrolledPanel):
    def __init__(self, parent: wx.Window, main_frame, ui_manager) -> None:
        super().__init__(parent, -1, style=wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER)
        self.main_frame = main_frame
        self.ui_manager = ui_manager
        self.controller = ProblemGenerationController()
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
        problem_definition_tab = self.ui_manager.get_tab("Problem Definition")
        num_customers = problem_definition_tab.get_num_customers()
        num_contractors = problem_definition_tab.get_num_contractors()
        contractor_rate = problem_definition_tab.get_contractor_rate()
        
        # Generate the problem using ProblemGenerationController
        self.customers, self.contractors = self.controller.generate_problem(num_customers, num_contractors, contractor_rate)
        
        # Update the content with the generated problem
        self.UpdateContent(self.customers, self.contractors, contractor_rate)
        
        # Enable the "Generate Greedy Solution" button
        greedy_solution_tab = self.ui_manager.get_tab("Greedy Solution")
        greedy_solution_tab.enable_generate_button()

    def UpdateContent(self, customers: List[Customer], contractors: List[Contractor], contractor_rate: float) -> None:
        self.content_box.Clear(True)
        
        # Display customer information
        customer_section = wx.StaticBox(self, label="Customers")
        customer_sizer = wx.StaticBoxSizer(customer_section, wx.VERTICAL)
        
        for customer in customers:
            customer_info = wx.StaticBox(self, label=f"Customer {customer.id}")
            customer_info_sizer = wx.StaticBoxSizer(customer_info, wx.VERTICAL)
            
            info: List[str] = self.controller.format_customer_info(customer)
            
            for line in info:
                customer_info_sizer.Add(wx.StaticText(self, label=line), flag=wx.ALL, border=2)
            
            customer_sizer.Add(customer_info_sizer, flag=wx.ALL|wx.EXPAND, border=5)
        
        self.content_box.Add(customer_sizer, flag=wx.ALL|wx.EXPAND, border=10)

        # Display contractor information
        contractor_section = wx.StaticBox(self, label="Contractors")
        contractor_sizer = wx.StaticBoxSizer(contractor_section, wx.VERTICAL)
        
        for contractor in contractors:
            info: str = self.controller.format_contractor_info(contractor)
            contractor_sizer.Add(wx.StaticText(self, label=info), flag=wx.ALL, border=2)

        # Display contractor rate
        rate_info: str = self.controller.format_contractor_rate(contractor_rate)
        contractor_sizer.Add(wx.StaticText(self, label=rate_info), flag=wx.ALL, border=2)

        self.content_box.Add(contractor_sizer, flag=wx.ALL|wx.EXPAND, border=10)

        self.Layout()
        self.SetupScrolling(scroll_x=False, scroll_y=True, rate_y=20)
        self.Refresh()
        self.Update()

    def OnSize(self, event: wx.SizeEvent) -> None:
        self.SetupScrolling(scroll_x=False, scroll_y=True, rate_y=20)
        event.Skip()
