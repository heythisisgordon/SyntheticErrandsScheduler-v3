"""
ProblemDefinitionTab: Provides the UI for defining problem parameters and calculating costs.
"""

import wx
from typing import List, Tuple
from models.schedule import Schedule
from constants import ERRAND_TYPES, MAX_INCENTIVE_MULTIPLIER, ErrandType

class ProblemDefinitionTab(wx.Panel):
    def __init__(self, parent: wx.Window):
        super().__init__(parent)
        self.num_customers: wx.SpinCtrl
        self.num_contractors: wx.SpinCtrl
        self.contractor_rate: wx.SpinCtrlDouble
        self.commit_temp_button: wx.Button
        self.commit_perm_button: wx.Button
        self.errand_params: List[Tuple[str, List[Tuple[str, wx.SpinCtrlDouble]]]] = []
        self.cost_texts: List[Tuple[str, List[Tuple[str, wx.StaticText]]]] = []
        self.total_base_cost_text: wx.StaticText
        self.total_max_cost_text: wx.StaticText
        self.InitUI()

    def InitUI(self) -> None:
        main_sizer: wx.BoxSizer = wx.BoxSizer(wx.VERTICAL)

        # Problem Parameters Section
        problem_params_box = wx.StaticBox(self, label="Problem Parameters")
        problem_params_sizer = wx.StaticBoxSizer(problem_params_box, wx.VERTICAL)

        grid_sizer = wx.FlexGridSizer(3, 2, 10, 10)
        grid_sizer.AddGrowableCol(1, 1)

        self.num_customers = wx.SpinCtrl(self, value="10", min=1, max=100, size=(60, -1))
        grid_sizer.Add(wx.StaticText(self, label="Number of Customers:"), flag=wx.ALIGN_CENTER_VERTICAL)
        grid_sizer.Add(self.num_customers)

        self.num_contractors = wx.SpinCtrl(self, value="3", min=1, max=10, size=(60, -1))
        grid_sizer.Add(wx.StaticText(self, label="Number of Contractors:"), flag=wx.ALIGN_CENTER_VERTICAL)
        grid_sizer.Add(self.num_contractors)

        self.contractor_rate = wx.SpinCtrlDouble(self, value="0.50", min=0.01, max=10.00, inc=0.01, size=(60, -1))
        self.contractor_rate.SetDigits(2)
        grid_sizer.Add(wx.StaticText(self, label="Contractor Labor Rate ($/minute):"), flag=wx.ALIGN_CENTER_VERTICAL)
        grid_sizer.Add(self.contractor_rate)

        problem_params_sizer.Add(grid_sizer, flag=wx.EXPAND|wx.ALL, border=10)
        main_sizer.Add(problem_params_sizer, flag=wx.EXPAND|wx.ALL, border=10)

        # Errand Types Section
        errand_types_box = wx.StaticBox(self, label="Errand Types")
        errand_types_sizer = wx.StaticBoxSizer(errand_types_box, wx.VERTICAL)

        for errand_type, base_time, incentive, disincentive in ERRAND_TYPES:
            errand_name = errand_type.name
            errand_box = wx.StaticBox(self, label=errand_name.replace('_', ' ').title())
            errand_sizer = wx.StaticBoxSizer(errand_box, wx.VERTICAL)
            
            param_grid = wx.FlexGridSizer(5, 3, 5, 5)
            param_grid.AddGrowableCol(1, 1)
            errand_params_list = []
            cost_texts_list = []

            # Base Time
            base_time_ctrl = wx.SpinCtrl(self, value=str(base_time), min=1, max=480, size=(60, -1))
            errand_params_list.append(('base_time', base_time_ctrl))
            param_grid.Add(wx.StaticText(self, label="Base Time:"), flag=wx.ALIGN_CENTER_VERTICAL)
            base_time_sizer = wx.BoxSizer(wx.HORIZONTAL)
            base_time_sizer.Add(base_time_ctrl, flag=wx.RIGHT, border=5)
            base_time_sizer.Add(wx.StaticText(self, label="minutes"), flag=wx.ALIGN_CENTER_VERTICAL)
            param_grid.Add(base_time_sizer, flag=wx.EXPAND)
            param_grid.Add(wx.StaticText(self, label=""))

            # Same-Day Incentive
            incentive_ctrl = wx.SpinCtrlDouble(self, value=str(incentive), min=1.0, max=1.5, inc=0.1, size=(60, -1))
            incentive_ctrl.SetDigits(1)
            errand_params_list.append(('incentive', incentive_ctrl))
            param_grid.Add(wx.StaticText(self, label="Same-Day Incentive:"), flag=wx.ALIGN_CENTER_VERTICAL)
            incentive_sizer = wx.BoxSizer(wx.HORIZONTAL)
            incentive_sizer.Add(incentive_ctrl, flag=wx.RIGHT, border=5)
            incentive_sizer.Add(wx.StaticText(self, label="multiplier"), flag=wx.ALIGN_CENTER_VERTICAL)
            param_grid.Add(incentive_sizer, flag=wx.EXPAND)
            param_grid.Add(wx.StaticText(self, label=""))

            # Disincentive
            disincentive_value = disincentive['value'] if isinstance(disincentive, dict) else 0.0
            disincentive_ctrl = wx.SpinCtrlDouble(self, value=str(disincentive_value), min=0.0, max=100.0, inc=1.0, size=(60, -1))
            disincentive_ctrl.SetDigits(1)
            errand_params_list.append(('disincentive', disincentive_ctrl))
            param_grid.Add(wx.StaticText(self, label="Disincentive:"), flag=wx.ALIGN_CENTER_VERTICAL)
            disincentive_sizer = wx.BoxSizer(wx.HORIZONTAL)
            disincentive_sizer.Add(disincentive_ctrl, flag=wx.RIGHT, border=5)
            disincentive_sizer.Add(wx.StaticText(self, label="% per day"), flag=wx.ALIGN_CENTER_VERTICAL)
            param_grid.Add(disincentive_sizer, flag=wx.EXPAND)
            param_grid.Add(wx.StaticText(self, label=""))

            # Base Cost
            base_cost_text = wx.StaticText(self, label="$0.00")
            cost_texts_list.append(('base_cost', base_cost_text))
            param_grid.Add(wx.StaticText(self, label="Base Cost:"), flag=wx.ALIGN_CENTER_VERTICAL)
            param_grid.Add(base_cost_text, flag=wx.ALIGN_CENTER_VERTICAL)
            param_grid.Add(wx.StaticText(self, label=""))

            # Max Cost
            max_cost_text = wx.StaticText(self, label="$0.00")
            cost_texts_list.append(('max_cost', max_cost_text))
            param_grid.Add(wx.StaticText(self, label="Max Cost:"), flag=wx.ALIGN_CENTER_VERTICAL)
            param_grid.Add(max_cost_text, flag=wx.ALIGN_CENTER_VERTICAL)
            param_grid.Add(wx.StaticText(self, label=""))

            errand_sizer.Add(param_grid, flag=wx.EXPAND|wx.ALL, border=5)
            errand_types_sizer.Add(errand_sizer, flag=wx.EXPAND|wx.ALL, border=5)

            # Bind events to update costs
            base_time_ctrl.Bind(wx.EVT_SPINCTRL, self.OnParamChange)
            incentive_ctrl.Bind(wx.EVT_SPINCTRLDOUBLE, self.OnParamChange)
            disincentive_ctrl.Bind(wx.EVT_SPINCTRLDOUBLE, self.OnParamChange)

            self.errand_params.append((errand_name, errand_params_list))
            self.cost_texts.append((errand_name, cost_texts_list))

        main_sizer.Add(errand_types_sizer, flag=wx.EXPAND|wx.ALL, border=10)

        # Total Costs Section
        total_costs_box = wx.StaticBox(self, label="Total Costs")
        total_costs_sizer = wx.StaticBoxSizer(total_costs_box, wx.VERTICAL)

        total_grid = wx.FlexGridSizer(2, 2, 5, 5)
        total_grid.AddGrowableCol(1, 1)

        self.total_base_cost_text = wx.StaticText(self, label="$0.00")
        total_grid.Add(wx.StaticText(self, label="Total Base Cost:"), flag=wx.ALIGN_CENTER_VERTICAL)
        total_grid.Add(self.total_base_cost_text, flag=wx.ALIGN_CENTER_VERTICAL)

        self.total_max_cost_text = wx.StaticText(self, label="$0.00")
        total_grid.Add(wx.StaticText(self, label="Total Max Cost:"), flag=wx.ALIGN_CENTER_VERTICAL)
        total_grid.Add(self.total_max_cost_text, flag=wx.ALIGN_CENTER_VERTICAL)

        total_costs_sizer.Add(total_grid, flag=wx.EXPAND|wx.ALL, border=5)
        main_sizer.Add(total_costs_sizer, flag=wx.EXPAND|wx.ALL, border=10)

        # Commit Changes Buttons and Note
        bottom_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.commit_temp_button = wx.Button(self, label="Commit Changes Temporarily")
        self.commit_temp_button.Bind(wx.EVT_BUTTON, self.OnCommitTemporary)
        bottom_sizer.Add(self.commit_temp_button, flag=wx.RIGHT, border=10)

        self.commit_perm_button = wx.Button(self, label="Commit Changes Permanently")
        self.commit_perm_button.Bind(wx.EVT_BUTTON, self.OnCommitPermanent)
        bottom_sizer.Add(self.commit_perm_button, flag=wx.RIGHT, border=10)

        note = wx.StaticText(self, label="Problem will be generated with these parameters. Click 'Commit Changes Temporarily' to use these parameters for the current session, or 'Commit Changes Permanently' to save these parameters as the default for future runs.")
        note.Wrap(400)
        bottom_sizer.Add(note, flag=wx.EXPAND|wx.LEFT, border=10)

        main_sizer.Add(bottom_sizer, flag=wx.EXPAND|wx.ALL, border=10)

        self.SetSizer(main_sizer)

    def OnParamChange(self, event: wx.Event) -> None:
        wx.PostEvent(self, wx.PyCommandEvent(wx.EVT_BUTTON.typeId, self.commit_temp_button.GetId()))

    def populate_fields(self, problem_params, errand_params):
        self.num_customers.SetValue(next(param[1] for param in problem_params if param[0] == 'num_customers'))
        self.num_contractors.SetValue(next(param[1] for param in problem_params if param[0] == 'num_contractors'))
        self.contractor_rate.SetValue(next(param[1] for param in problem_params if param[0] == 'contractor_rate'))

        for errand_type, params in errand_params:
            errand_params_list = next(ep for et, ep in self.errand_params if et == errand_type)
            for param_name, value in params:
                param_control = next(p[1] for p in errand_params_list if p[0] == param_name)
                param_control.SetValue(value)

    def update_cost_display(self, costs, total_costs):
        for errand_type, cost in costs:
            base_cost_text = next(text for name, text in next(ct for et, ct in self.cost_texts if et == errand_type) if name == 'base_cost')
            max_cost_text = next(text for name, text in next(ct for et, ct in self.cost_texts if et == errand_type) if name == 'max_cost')
            base_cost_text.SetLabel(f"${next(c[1] for c in cost if c[0] == 'base_cost'):.2f}")
            max_cost_text.SetLabel(f"${next(c[1] for c in cost if c[0] == 'max_cost'):.2f}")

        self.total_base_cost_text.SetLabel(f"${next(c[1] for c in total_costs if c[0] == 'total_base_cost'):.2f}")
        self.total_max_cost_text.SetLabel(f"${next(c[1] for c in total_costs if c[0] == 'total_max_cost'):.2f}")

    def OnCommitTemporary(self, event: wx.CommandEvent) -> None:
        wx.PostEvent(self.GetParent(), wx.PyCommandEvent(wx.EVT_BUTTON.typeId, self.commit_temp_button.GetId()))

    def OnCommitPermanent(self, event: wx.CommandEvent) -> None:
        wx.PostEvent(self.GetParent(), wx.PyCommandEvent(wx.EVT_BUTTON.typeId, self.commit_perm_button.GetId()))

    def get_num_customers(self) -> int:
        return self.num_customers.GetValue()

    def get_num_contractors(self) -> int:
        return self.num_contractors.GetValue()

    def get_contractor_rate(self) -> float:
        return self.contractor_rate.GetValue()

    def get_errand_params(self) -> List[Tuple[str, List[Tuple[str, float]]]]:
        return [(errand_type, [(param, value.GetValue()) for param, value in params])
                for errand_type, params in self.errand_params]

    def show_error(self, message: str):
        wx.MessageBox(message, "Error", wx.OK | wx.ICON_ERROR)
