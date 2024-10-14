"""
MainFrame: Defines the main window of the Synthetic Errands Scheduler application.
"""

import wx
import logging

logger = logging.getLogger(__name__)

class MainFrame(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent=parent, title=title)
        self.panel = wx.Panel(self)
        
        self.problem_definition_tab = None
        self.problem_generation_tab = None
        self.greedy_solution_tab = None
        self.contractor_schedule_tab = None

        self.init_ui()

    def init_ui(self):
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel.SetSizer(self.main_sizer)

        self.SetSize((800, 600))
        self.Centre()

    def set_notebook(self, notebook):
        self.main_sizer.Add(notebook, 1, wx.EXPAND)
        self.panel.Layout()

def main():
    app = wx.App()
    frame = MainFrame(None, "Synthetic Errands Scheduler")
    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()
