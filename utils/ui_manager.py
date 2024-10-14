"""
UIManager: Manages the creation and organization of UI components.
"""

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

    def initialize_ui(self):
        self.create_notebook()
        self.create_tabs()
        self.parent_frame.set_notebook(self.notebook)

    def create_notebook(self):
        self.notebook = wx.Notebook(self.parent_frame.panel)

    def create_tabs(self):
        tab_classes = [
            ("Problem Definition", ProblemDefinitionTab),
            ("Problem Generation", ProblemGenerationTab),
            ("Greedy Solution", GreedySolutionTab),
            ("Contractor Schedules", ContractorScheduleTab)
        ]

        for tab_name, tab_class in tab_classes:
            scrolled_window = wx.ScrolledWindow(self.notebook)
            tab_content = tab_class(scrolled_window)
            self.setup_tab(scrolled_window, tab_content)
            self.notebook.AddPage(scrolled_window, tab_name)
            self.tabs[tab_name] = tab_content

        self.parent_frame.problem_definition_tab = self.tabs["Problem Definition"]
        self.parent_frame.problem_generation_tab = self.tabs["Problem Generation"]
        self.parent_frame.greedy_solution_tab = self.tabs["Greedy Solution"]
        self.parent_frame.contractor_schedule_tab = self.tabs["Contractor Schedules"]

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

    def enable_tab(self, tab):
        index = self.notebook.FindPage(tab)
        if index != wx.NOT_FOUND:
            self.notebook.EnablePage(index, True)

    def disable_tab(self, tab):
        index = self.notebook.FindPage(tab)
        if index != wx.NOT_FOUND:
            self.notebook.EnablePage(index, False)
