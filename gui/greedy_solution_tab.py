import wx
import wx.lib.scrolledpanel as scrolled
from algorithms.initial_scheduler import initial_schedule

class GreedySolutionTab(scrolled.ScrolledPanel):
    def __init__(self, parent):
        super().__init__(parent, -1, style=wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER)
        self.InitUI()

    def InitUI(self):
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.vbox)
        self.SetupScrolling(scroll_x=False, scroll_y=True, rate_y=20)
        self.SetMinSize((780, 500))  # Set a minimum size for the panel

    def UpdateContent(self, customers, contractors):
        self.vbox.Clear(True)
        
        # Generate initial schedule
        schedule = initial_schedule(customers, contractors)
        
        # Display schedule information
        self.vbox.Add(wx.StaticText(self, label="Initial Schedule:"), flag=wx.ALL, border=5)
        for day, assignments in schedule.assignments.items():
            self.vbox.Add(wx.StaticText(self, label=f"\nDay {day + 1}:"), flag=wx.ALL, border=5)
            for customer, contractor, start_time in assignments:
                hours, minutes = divmod(start_time, 60)
                info = f"  Contractor {contractor.id} - Customer {customer.id}:"
                self.vbox.Add(wx.StaticText(self, label=info), flag=wx.ALL, border=2)
                info = f"    Errand: {customer.desired_errand.type}"
                self.vbox.Add(wx.StaticText(self, label=info), flag=wx.ALL, border=2)
                info = f"    Start Time: {hours:02d}:{minutes:02d}"
                self.vbox.Add(wx.StaticText(self, label=info), flag=wx.ALL, border=2)
                info = f"    Location: {customer.location}"
                self.vbox.Add(wx.StaticText(self, label=info), flag=wx.ALL, border=2)

        profit = schedule.calculate_total_profit()
        self.vbox.Add(wx.StaticText(self, label=f"\nTotal Profit: ${profit:.2f}"), flag=wx.ALL, border=5)

        self.Layout()
        self.SetupScrolling(scroll_x=False, scroll_y=True, rate_y=20)
        self.Refresh()
        self.Update()

    def OnSize(self, event):
        self.SetupScrolling(scroll_x=False, scroll_y=True, rate_y=20)
        event.Skip()