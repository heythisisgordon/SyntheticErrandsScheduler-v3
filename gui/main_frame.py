import wx
from typing import List, Tuple
from gui.problem_definition_tab import ProblemDefinitionTab
from gui.generated_problem_tab import GeneratedProblemTab
from gui.greedy_solution_tab import GreedySolutionTab
from gui.optimized_solution_tab import OptimizedSolutionTab
from gui.visualization_tab import VisualizationTab

class SyntheticErrandsSchedulerGUI(wx.Frame):
    def __init__(self) -> None:
        super().__init__(parent=None, title='Synthetic Errands Scheduler')
        self.InitUI()

    def InitUI(self) -> None:
        panel: wx.Panel = wx.Panel(self)
        notebook: wx.Notebook = wx.Notebook(panel)

        self.tab1: wx.ScrolledWindow = wx.ScrolledWindow(notebook)
        self.tab2: wx.ScrolledWindow = wx.ScrolledWindow(notebook)
        self.tab3: wx.ScrolledWindow = wx.ScrolledWindow(notebook)
        self.tab4: wx.ScrolledWindow = wx.ScrolledWindow(notebook)
        self.tab5: wx.ScrolledWindow = wx.ScrolledWindow(notebook)

        self.problem_definition: ProblemDefinitionTab = ProblemDefinitionTab(self.tab1)
        self.generated_problem: GeneratedProblemTab = GeneratedProblemTab(self.tab2)
        self.greedy_solution: GreedySolutionTab = GreedySolutionTab(self.tab3)
        self.optimized_solution: OptimizedSolutionTab = OptimizedSolutionTab(self.tab4)
        self.visualization: VisualizationTab = VisualizationTab(self.tab5)

        tabs_and_contents: List[Tuple[wx.ScrolledWindow, wx.Window]] = [
            (self.tab1, self.problem_definition),
            (self.tab2, self.generated_problem),
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

        notebook.AddPage(self.tab1, "Problem Definition")
        notebook.AddPage(self.tab2, "Generated Problem")
        notebook.AddPage(self.tab3, "Greedy Solution")
        notebook.AddPage(self.tab4, "Optimized Solution")
        notebook.AddPage(self.tab5, "Visualization")

        sizer: wx.BoxSizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(notebook, 1, wx.EXPAND)
        panel.SetSizer(sizer)

        self.SetSize((800, 600))
        self.Centre()

    def OnTabSize(self, event: wx.SizeEvent) -> None:
        # Adjust the virtual size of the scrolled window when its size changes
        tab: wx.ScrolledWindow = event.GetEventObject()
        size: wx.Size = tab.GetSize()
        tab.SetVirtualSize(size)
        tab.FitInside()
        event.Skip()

def main() -> None:
    app: wx.App = wx.App()
    ex: SyntheticErrandsSchedulerGUI = SyntheticErrandsSchedulerGUI()
    ex.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()