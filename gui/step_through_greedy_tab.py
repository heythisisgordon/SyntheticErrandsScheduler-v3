import wx
from typing import Dict, Any
from algorithms.greedy_stepper import greedy_step_through

class StepThroughGreedyTab(wx.Panel):
    def __init__(self, parent, main_frame):
        super().__init__(parent)
        self.main_frame = main_frame
        self.problem_generation_tab = main_frame.problem_generation
        self.greedy_stepper = None
        self.create_widgets()

    def create_widgets(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.step_button = wx.Button(self, label="Step")
        self.step_button.Bind(wx.EVT_BUTTON, self.step_through)
        button_sizer.Add(self.step_button, 0, wx.ALL, 5)

        self.reset_button = wx.Button(self, label="Reset")
        self.reset_button.Bind(wx.EVT_BUTTON, self.reset_stepper)
        button_sizer.Add(self.reset_button, 0, wx.ALL, 5)

        main_sizer.Add(button_sizer, 0, wx.EXPAND)

        self.variables_text = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL)
        main_sizer.Add(self.variables_text, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(main_sizer)

    def initialize_stepper(self):
        customers = self.problem_generation_tab.customers
        contractors = self.problem_generation_tab.contractors
        contractor_calendars = self.main_frame.imcs.contractor_calendars
        if not customers or not contractors or not contractor_calendars:
            self.variables_text.AppendText("Please generate a problem and initialize calendars first.\n")
            return False
        self.greedy_stepper = greedy_step_through(customers, contractors, contractor_calendars)
        return True

    def reset_stepper(self, event=None):
        if self.initialize_stepper():
            self.variables_text.Clear()
            self.variables_text.AppendText("Stepper reset. Ready to step through.\n")
            self.step_button.Enable()

    def step_through(self, event=None):
        if not self.greedy_stepper:
            if not self.initialize_stepper():
                return

        step_result = self.greedy_stepper.step()
        if step_result:
            self.update_variables_display(step_result)
            if step_result['step_name'] == 'log_results':
                self.variables_text.AppendText("Scheduling complete.\n")
                self.step_button.Disable()
        else:
            self.variables_text.AppendText("Scheduling complete.\n")
            self.step_button.Disable()

    def update_variables_display(self, step_result: Dict[str, Any]):
        self.variables_text.AppendText(f"\n{'='*50}\n")
        self.variables_text.AppendText(f"Method: {step_result['step_name']}\n")
        self.variables_text.AppendText(f"{'-'*50}\n")
        for key, value in step_result['variables'].items():
            self.variables_text.AppendText(f"{key}: {value}\n")
        self.variables_text.AppendText(f"{'='*50}\n")
        self.variables_text.ShowPosition(self.variables_text.GetLastPosition())

    def on_tab_selected(self):
        if not self.greedy_stepper:
            self.reset_stepper()
