import wx
from typing import List, Tuple
from gui.problem_definition_tab import ProblemDefinitionTab
from gui.problem_generation_tab import ProblemGenerationTab
from gui.greedy_solution_tab import GreedySolutionTab
from gui.contractor_schedule_tab import ContractorScheduleTab

class UIManager:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.notebook = None
        self.tabs = {}

    def create_notebook(self, panel):
        self.notebook = wx.Notebook(panel)

    def create_tabs(self):
        tab_classes = [
            ("Problem Definition", ProblemDefinitionTab),
            ("Problem Generation", ProblemGenerationTab),
            ("Greedy Solution", GreedySolutionTab),
            ("Contractor Schedules", ContractorScheduleTab)
        ]

        for tab_name, tab_class in tab_classes:
            scrolled_window = wx.ScrolledWindow(self.notebook)
            if tab_class == ContractorScheduleTab:
                tab_content = tab_class(scrolled_window)
            elif tab_class == ProblemGenerationTab:
                tab_content = tab_class(scrolled_window, self.parent_frame, self)
            else:
                tab_content = tab_class(scrolled_window, self.parent_frame)
            self.setup_tab(scrolled_window, tab_content)
            self.notebook.AddPage(scrolled_window, tab_name)
            self.tabs[tab_name] = tab_content

    def setup_tab(self, tab, content):
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(content, 1, wx.EXPAND | wx.ALL, 10)
        tab.SetSizer(sizer)
        tab.SetScrollRate(5, 5)
        tab.EnableScrolling(True, True)
        tab.SetMinSize((780, 500))
        tab.Bind(wx.EVT_SIZE, self.on_tab_size)

    def on_tab_size(self, event):
        tab = event.GetEventObject()
        size = tab.GetSize()
        tab.SetVirtualSize(size)
        tab.FitInside()
        event.Skip()

    def get_tab(self, tab_name):
        return self.tabs.get(tab_name)
