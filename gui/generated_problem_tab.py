import wx
import wx.lib.scrolledpanel as scrolled
from typing import List
from models.customer import Customer
from models.contractor import Contractor

class GeneratedProblemTab(scrolled.ScrolledPanel):
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
        
        # Display customer information
        self.vbox.Add(wx.StaticText(self, label="Customers:"), flag=wx.ALL, border=5)
        for customer in customers:
            info: str = f"Customer {customer.id}: Location {customer.location}, " \
                   f"Errand: {customer.desired_errand.type}, " \
                   f"Base Time: {customer.desired_errand.base_time}, " \
                   f"Charge: ${customer.desired_errand.charge:.2f}"
            self.vbox.Add(wx.StaticText(self, label=info), flag=wx.ALL, border=5)

        # Display contractor information
        self.vbox.Add(wx.StaticText(self, label="\nContractors:"), flag=wx.ALL, border=5)
        for contractor in contractors:
            info: str = f"Contractor {contractor.id}: Location {contractor.location}"
            self.vbox.Add(wx.StaticText(self, label=info), flag=wx.ALL, border=5)

        self.Layout()
        self.SetupScrolling(scroll_x=False, scroll_y=True, rate_y=20)
        self.Refresh()
        self.Update()

    def OnSize(self, event: wx.SizeEvent) -> None:
        self.SetupScrolling(scroll_x=False, scroll_y=True, rate_y=20)
        event.Skip()