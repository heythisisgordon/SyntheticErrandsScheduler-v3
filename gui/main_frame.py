import wx
from controllers.main_frame_controller import MainFrameController
import logging

logger = logging.getLogger(__name__)

class SyntheticErrandsSchedulerGUI(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Synthetic Errands Scheduler')
        self.panel = wx.Panel(self)
        self.controller = MainFrameController(self)
        self.init_ui()

    def init_ui(self):
        self.controller.initialize_ui()

        # Set up attributes for easy access to tabs
        self.problem_definition = self.controller.get_tab("Problem Definition")
        self.problem_generation = self.controller.get_tab("Problem Generation")
        self.greedy_solution = self.controller.get_tab("Greedy Solution")
        self.contractor_schedule = self.controller.get_tab("Contractor Schedules")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.controller.ui_manager.notebook, 1, wx.EXPAND)
        self.panel.SetSizer(sizer)

        self.SetSize((800, 600))
        self.Centre()

    def enable_greedy_solution(self):
        self.controller.enable_greedy_solution()

    def update_contractor_schedule(self, schedule):
        self.controller.update_contractor_schedule(schedule)

def main():
    app = wx.App()
    gui_window = SyntheticErrandsSchedulerGUI()
    gui_window.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()
