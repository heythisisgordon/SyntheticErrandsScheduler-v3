import wx
from typing import List, Tuple, Dict
from models.schedule import Schedule
from constants import ERRAND_TYPES, MAX_INCENTIVE_MULTIPLIER, ErrandType
from utils.config_manager import ConfigManager

class ProblemDefinitionTab(wx.Panel):
    def __init__(self, parent: wx.Window, main_frame) -> None:
        super().__init__(parent)
        self.main_frame = main_frame
        self.config_manager = ConfigManager()
        self.num_customers: wx.SpinCtrl
        self.num_contractors: wx.SpinCtrl
        self.contractor_rate: wx.SpinCtrlDouble
        self.commit_temp_button: wx.Button
        self.commit_perm_button: wx.Button
        self.errand_params: Dict[str, Dict[str, wx.SpinCtrlDouble]] = {}
        self.cost_texts: Dict[str, Dict[str, wx.StaticText]] = {}
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

        self.num_customers = wx.SpinCtrl(self, value=str(self.config_manager.get('num_customers', 10)), min=1, max=100, size=(60, -1))
        grid_sizer.Add(wx.StaticText(self, label="Number of Customers:"), flag=wx.ALIGN_CENTER_VERTICAL)
        grid_sizer.Add(self.num_customers)

        self.num_contractors = wx.SpinCtrl(self, value=str(self.config_manager.get('num_contractors', 2)), min=1, max=10, size=(60, -1))
        grid_sizer.Add(wx.StaticText(self, label="Number of Contractors:"), flag=wx.ALIGN_CENTER_VERTICAL)
        grid_sizer.Add(self.num_contractors)

        self.contractor_rate = wx.SpinCtrlDouble(self, value=str(self.config_manager.get('contractor_rate', 0.50)), min=0.01, max=10.00, inc=0.01, size=(60, -1))
        self.contractor_rate.SetDigits(2)
        grid_sizer.Add(wx.StaticText(self, label="Contractor Labor Rate ($/minute):"), flag=wx.ALIGN_CENTER_VERTICAL)
        grid_sizer.Add(self.contractor_rate)

        problem_params_sizer.Add(grid_sizer, flag=wx.EXPAND|wx.ALL, border=10)
        main_sizer.Add(problem_params_sizer, flag=wx.EXPAND|wx.ALL, border=10)

        # Errand Types Section
        errand_types_box = wx.StaticBox(self, label="Errand Types")
        errand_types_sizer = wx.StaticBoxSizer(errand_types_box, wx.VERTICAL)

        for errand_type, base_time, incentive, disincentive in ERRAND_TYPES:
            errand_box = wx.StaticBox(self, label=errand_type.name.replace('_', ' ').title())
            errand_sizer = wx.StaticBoxSizer(errand_box, wx.VERTICAL)
            
            param_grid = wx.FlexGridSizer(5, 3, 5, 5)
            param_grid.AddGrowableCol(1, 1)
            self.errand_params[errand_type.name] = {}
            self.cost_texts[errand_type.name] = {}

            # Base Time
            self.errand_params[errand_type.name]['base_time'] = wx.SpinCtrl(self, value=str(base_time), min=1, max=480, size=(60, -1))
            param_grid.Add(wx.StaticText(self, label="Base Time:"), flag=wx.ALIGN_CENTER_VERTICAL)
            base_time_sizer = wx.BoxSizer(wx.HORIZONTAL)
            base_time_sizer.Add(self.errand_params[errand_type.name]['base_time'], flag=wx.RIGHT, border=5)
            base_time_sizer.Add(wx.StaticText(self, label="minutes"), flag=wx.ALIGN_CENTER_VERTICAL)
            param_grid.Add(base_time_sizer, flag=wx.EXPAND)
            param_grid.Add(wx.StaticText(self, label=""))

            # Same-Day Incentive
            self.errand_params[errand_type.name]['incentive'] = wx.SpinCtrlDouble(self, value=str(incentive), min=1.0, max=1.5, inc=0.1, size=(60, -1))
            self.errand_params[errand_type.name]['incentive'].SetDigits(1)
            param_grid.Add(wx.StaticText(self, label="Same-Day Incentive:"), flag=wx.ALIGN_CENTER_VERTICAL)
            incentive_sizer = wx.BoxSizer(wx.HORIZONTAL)
            incentive_sizer.Add(self.errand_params[errand_type.name]['incentive'], flag=wx.RIGHT, border=5)
            incentive_sizer.Add(wx.StaticText(self, label="multiplier"), flag=wx.ALIGN_CENTER_VERTICAL)
            param_grid.Add(incentive_sizer, flag=wx.EXPAND)
            param_grid.Add(wx.StaticText(self, label=""))

            # Disincentive (added for all errand types)
            self.errand_params[errand_type.name]['disincentive'] = wx.SpinCtrlDouble(self, value=str(disincentive['value'] if disincentive else 0.0), min=0.0, max=100.0, inc=1.0, size=(60, -1))
            self.errand_params[errand_type.name]['disincentive'].SetDigits(1)
            param_grid.Add(wx.StaticText(self, label="Disincentive:"), flag=wx.ALIGN_CENTER_VERTICAL)
            disincentive_sizer = wx.BoxSizer(wx.HORIZONTAL)
            disincentive_sizer.Add(self.errand_params[errand_type.name]['disincentive'], flag=wx.RIGHT, border=5)
            disincentive_sizer.Add(wx.StaticText(self, label="% per day"), flag=wx.ALIGN_CENTER_VERTICAL)
            param_grid.Add(disincentive_sizer, flag=wx.EXPAND)
            param_grid.Add(wx.StaticText(self, label=""))

            # Base Cost
            self.cost_texts[errand_type.name]['base_cost'] = wx.StaticText(self, label="$0.00")
            param_grid.Add(wx.StaticText(self, label="Base Cost:"), flag=wx.ALIGN_CENTER_VERTICAL)
            param_grid.Add(self.cost_texts[errand_type.name]['base_cost'], flag=wx.ALIGN_CENTER_VERTICAL)
            param_grid.Add(wx.StaticText(self, label=""))

            # Max Cost
            self.cost_texts[errand_type.name]['max_cost'] = wx.StaticText(self, label="$0.00")
            param_grid.Add(wx.StaticText(self, label="Max Cost:"), flag=wx.ALIGN_CENTER_VERTICAL)
            param_grid.Add(self.cost_texts[errand_type.name]['max_cost'], flag=wx.ALIGN_CENTER_VERTICAL)
            param_grid.Add(wx.StaticText(self, label=""))

            errand_sizer.Add(param_grid, flag=wx.EXPAND|wx.ALL, border=5)
            errand_types_sizer.Add(errand_sizer, flag=wx.EXPAND|wx.ALL, border=5)

            # Bind events to update costs
            self.errand_params[errand_type.name]['base_time'].Bind(wx.EVT_SPINCTRL, self.OnParamChange)
            self.errand_params[errand_type.name]['incentive'].Bind(wx.EVT_SPINCTRLDOUBLE, self.OnParamChange)
            self.errand_params[errand_type.name]['disincentive'].Bind(wx.EVT_SPINCTRLDOUBLE, self.OnParamChange)

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

        # Initial cost calculation
        self.UpdateAllCosts()

    def OnParamChange(self, event: wx.Event) -> None:
        self.UpdateAllCosts()

    def UpdateAllCosts(self) -> None:
        total_base_cost = 0
        total_max_cost = 0

        for errand_type, params in self.errand_params.items():
            base_time = params['base_time'].GetValue()
            incentive = params['incentive'].GetValue()
            contractor_rate = self.contractor_rate.GetValue()

            base_cost = base_time * contractor_rate
            max_cost = base_cost * incentive

            self.cost_texts[errand_type]['base_cost'].SetLabel(f"${base_cost:.2f}")
            self.cost_texts[errand_type]['max_cost'].SetLabel(f"${max_cost:.2f}")

            total_base_cost += base_cost
            total_max_cost += max_cost

        self.total_base_cost_text.SetLabel(f"${total_base_cost:.2f}")
        self.total_max_cost_text.SetLabel(f"${total_max_cost:.2f}")

    def OnCommitTemporary(self, event: wx.CommandEvent) -> None:
        self.UpdateConfig(save_to_file=False)
        wx.MessageBox("Changes have been committed for the current session.", "Success", wx.OK | wx.ICON_INFORMATION)

    def OnCommitPermanent(self, event: wx.CommandEvent) -> None:
        self.UpdateConfig(save_to_file=True)
        wx.MessageBox("Changes have been committed and saved for future runs.", "Success", wx.OK | wx.ICON_INFORMATION)

    def UpdateConfig(self, save_to_file: bool) -> None:
        updated_config = {
            'num_customers': self.num_customers.GetValue(),
            'num_contractors': self.num_contractors.GetValue(),
            'contractor_rate': self.contractor_rate.GetValue()
        }

        # Update errand type parameters
        errand_types = []
        for errand_type, params in self.errand_params.items():
            errand_config = {
                'name': errand_type,
                'base_time': params['base_time'].GetValue(),
                'incentive': params['incentive'].GetValue(),
                'disincentive': {
                    'type': 'percentage',
                    'value': params['disincentive'].GetValue(),
                    'days': 14  # Assuming it's always 14 days
                }
            }
            errand_types.append(errand_config)

        updated_config['errand_types'] = errand_types

        self.config_manager.update(updated_config)
        if save_to_file:
            self.config_manager.save()

    def get_num_customers(self) -> int:
        return self.num_customers.GetValue()

    def get_num_contractors(self) -> int:
        return self.num_contractors.GetValue()

    def get_contractor_rate(self) -> float:
        return self.contractor_rate.GetValue()

    def get_errand_params(self) -> Dict[str, Dict[str, float]]:
        return {errand_type: {param: value.GetValue() for param, value in params.items()}
                for errand_type, params in self.errand_params.items()}