import wx
from typing import List, Tuple
from gui.problem_definition_tab import ProblemDefinitionTab
from gui.problem_generation_tab import ProblemGenerationTab
from gui.greedy_solution_tab import GreedySolutionTab
from gui.optimized_solution_tab import OptimizedSolutionTab
from gui.visualization_tab import VisualizationTab

class SyntheticErrandsSchedulerGUI(wx.Frame):
    def __init__(self) -> None:
        super().__init__(parent=None, title='Synthetic Errands Scheduler')
        self.InitUI()

    def InitUI(self) -> None:
        panel: wx.Panel = wx.Panel(self)
        self.notebook: wx.Notebook = wx.Notebook(panel)

        self.tab1: wx.ScrolledWindow = wx.ScrolledWindow(self.notebook)
        self.tab2: wx.ScrolledWindow = wx.ScrolledWindow(self.notebook)
        self.tab3: wx.ScrolledWindow = wx.ScrolledWindow(self.notebook)
        self.tab4: wx.ScrolledWindow = wx.ScrolledWindow(self.notebook)
        self.tab5: wx.ScrolledWindow = wx.ScrolledWindow(self.notebook)

        self.problem_definition: ProblemDefinitionTab = ProblemDefinitionTab(self.tab1, self)
        self.problem_generation: ProblemGenerationTab = ProblemGenerationTab(self.tab2, self)
        self.greedy_solution: GreedySolutionTab = GreedySolutionTab(self.tab3, self)
        self.optimized_solution: OptimizedSolutionTab = OptimizedSolutionTab(self.tab4, self)
        self.visualization: VisualizationTab = VisualizationTab(self.tab5)

        tabs_and_contents: List[Tuple[wx.ScrolledWindow, wx.Window]] = [
            (self.tab1, self.problem_definition),
            (self.tab2, self.problem_generation),
            (self.tab3, self.greedy_solution),
            (self.tab4, self.optimized_solution),
            (self.tab5, self.visualization)
        ]

        for tab, content in tabs_and_contents:
            sizer: wx.BoxSizer = wx.BoxSizer(wx.VERTICAL)
            sizer.Add(content, 1, wx.EXPAND | wx.ALL, 10)
            tab.SetSizer(sizer)
            tab.SetScrollRate(5, 5)
            tab.EnableScrolling(True, True)
            tab.SetMinSize((780, 500))  # Set a minimum size for the scrolled window
            
            # Bind the size event to adjust the scroll bars
            tab.Bind(wx.EVT_SIZE, self.OnTabSize)

        self.notebook.AddPage(self.tab1, "Problem Definition")
        self.notebook.AddPage(self.tab2, "Problem Generation")
        self.notebook.AddPage(self.tab3, "Greedy Solution")
        self.notebook.AddPage(self.tab4, "Optimized Solution")
        self.notebook.AddPage(self.tab5, "Visualization")

        sizer: wx.BoxSizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.notebook, 1, wx.EXPAND)
        panel.SetSizer(sizer)

        self.SetSize((800, 600))
        self.Centre()

        # Bind the notebook page change event
        self.notebook.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)

    def OnTabSize(self, event: wx.SizeEvent) -> None:
        # Adjust the virtual size of the scrolled window when its size changes
        tab: wx.ScrolledWindow = event.GetEventObject()
        size: wx.Size = tab.GetSize()
        tab.SetVirtualSize(size)
        tab.FitInside()
        event.Skip()

    def enable_greedy_solution(self) -> None:
        self.greedy_solution.enable_generate_button()

    def enable_optimized_solution(self) -> None:
        self.optimized_solution.enable_optimize_button()

    def update_visualization(self, customers, contractors, optimized_schedule) -> None:
        self.visualization.UpdateContent(customers, contractors, optimized_schedule)

    def OnPageChanged(self, event: wx.BookCtrlEvent) -> None:
        new = event.GetSelection()
        event.Skip()

        # Provide warnings when necessary, but allow users to proceed
        if new == 2 and not self.greedy_solution.generate_button.IsEnabled():
            wx.MessageBox("Warning: A problem has not been generated yet. Some features may not be available.", "Warning", wx.OK | wx.ICON_WARNING)
        elif new == 3 and not self.optimized_solution.optimize_button.IsEnabled():
            wx.MessageBox("Warning: A greedy solution has not been generated yet. Some features may not be available.", "Warning", wx.OK | wx.ICON_WARNING)
        elif new == 4 and not hasattr(self.visualization, 'optimized_schedule'):
            wx.MessageBox("Warning: An optimized solution has not been generated yet. The visualization may be incomplete.", "Warning", wx.OK | wx.ICON_WARNING)

def main() -> None:
    app: wx.App = wx.App()
    ex: SyntheticErrandsSchedulerGUI = SyntheticErrandsSchedulerGUI()
    ex.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()