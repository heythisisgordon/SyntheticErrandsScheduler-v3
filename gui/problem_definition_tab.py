import wx
from main import generate_problem, ERRAND_TYPES
from models.schedule import Schedule

class ProblemDefinitionTab(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.InitUI()

    def InitUI(self):
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Add input fields for problem parameters
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.num_customers = wx.SpinCtrl(self, value='10', min=1, max=100)
        hbox1.Add(wx.StaticText(self, label="Number of Customers:"), flag=wx.RIGHT, border=8)
        hbox1.Add(self.num_customers)
        vbox.Add(hbox1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.num_contractors = wx.SpinCtrl(self, value='2', min=1, max=10)
        hbox2.Add(wx.StaticText(self, label="Number of Contractors:"), flag=wx.RIGHT, border=8)
        hbox2.Add(self.num_contractors)
        vbox.Add(hbox2, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        # Add model information
        vbox.Add(wx.StaticLine(self), flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
        vbox.Add(wx.StaticText(self, label="Model Information:"), flag=wx.LEFT|wx.TOP, border=10)

        # Errand model information
        errand_info = wx.StaticText(self, label="Errand: id, type, base_time, incentive, disincentive")
        vbox.Add(errand_info, flag=wx.LEFT|wx.TOP, border=10)

        # Customer model information
        customer_info = wx.StaticText(self, label="Customer: id, location, desired_errand, availability")
        vbox.Add(customer_info, flag=wx.LEFT|wx.TOP, border=10)

        # Contractor model information
        contractor_info = wx.StaticText(self, label="Contractor: id, location, schedule")
        vbox.Add(contractor_info, flag=wx.LEFT|wx.TOP, border=10)

        # Add contractor labor rate information
        contractor_rate_info = wx.StaticText(self, label=f"Contractor Labor Rate: ${Schedule.contractor_cost_per_minute:.2f} per minute")
        vbox.Add(contractor_rate_info, flag=wx.LEFT|wx.TOP, border=10)

        # Add errand types information
        vbox.Add(wx.StaticLine(self), flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
        vbox.Add(wx.StaticText(self, label="Errand Types:"), flag=wx.LEFT|wx.TOP, border=10)

        for errand_type, base_time, incentive, disincentive in ERRAND_TYPES:
            errand_type_info = wx.StaticText(self, label=f"{errand_type}:")
            vbox.Add(errand_type_info, flag=wx.LEFT|wx.TOP, border=10)
            
            details = f"  Base Time: {base_time} minutes\n"
            details += f"  Incentive: {incentive}x same-day\n"
            if disincentive:
                if disincentive['type'] == 'percentage':
                    details += f"  Disincentive: -{disincentive['value']}%/day past {disincentive['days']} days"
                else:
                    details += f"  Disincentive: -${disincentive['value']}/day past {disincentive['days']} days"
            else:
                details += "  Disincentive: None"
            
            errand_details = wx.StaticText(self, label=details)
            vbox.Add(errand_details, flag=wx.LEFT|wx.TOP, border=20)

        # Add SLA window information
        vbox.Add(wx.StaticLine(self), flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
        sla_info = wx.StaticText(self, label="SLA Window: 14 days")
        vbox.Add(sla_info, flag=wx.LEFT|wx.TOP, border=10)

        # Add working hours information
        working_hours_info = wx.StaticText(self, label="Working Hours: 8am to 5pm each day")
        vbox.Add(working_hours_info, flag=wx.LEFT|wx.TOP, border=10)

        # Add a button to generate the problem
        self.generate_btn = wx.Button(self, label='Generate Problem')
        self.generate_btn.Bind(wx.EVT_BUTTON, self.OnGenerate)
        vbox.Add(self.generate_btn, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        self.SetSizer(vbox)

    def OnGenerate(self, event):
        # Generate the problem and update other tabs
        num_customers = self.num_customers.GetValue()
        num_contractors = self.num_contractors.GetValue()
        
        # Generate problem instance
        customers, contractors = generate_problem(num_customers, num_contractors)
        
        # Update other tabs
        main_frame = wx.GetApp().GetTopWindow()
        main_frame.generated_problem.UpdateContent(customers, contractors)
        main_frame.greedy_solution.UpdateContent(customers, contractors)
        main_frame.optimized_solution.UpdateContent(customers, contractors)
        main_frame.visualization.UpdateContent(customers, contractors)