import wx
from gui.problem_definition_tab import ProblemDefinitionTab
from gui.generated_problem_tab import GeneratedProblemTab
from gui.greedy_solution_tab import GreedySolutionTab
from gui.optimized_solution_tab import OptimizedSolutionTab
from gui.visualization_tab import VisualizationTab

class SyntheticErrandsSchedulerGUI(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Synthetic Errands Scheduler')
        self.InitUI()

    def InitUI(self):
        panel = wx.Panel(self)
        notebook = wx.Notebook(panel)

        self.tab1 = wx.ScrolledWindow(notebook)
        self.tab2 = wx.ScrolledWindow(notebook)
        self.tab3 = wx.ScrolledWindow(notebook)
        self.tab4 = wx.ScrolledWindow(notebook)
        self.tab5 = wx.ScrolledWindow(notebook)

        self.problem_definition = ProblemDefinitionTab(self.tab1)
        self.generated_problem = GeneratedProblemTab(self.tab2)
        self.greedy_solution = GreedySolutionTab(self.tab3)
        self.optimized_solution = OptimizedSolutionTab(self.tab4)
        self.visualization = VisualizationTab(self.tab5)

        for tab, content in [
            (self.tab1, self.problem_definition),
            (self.tab2, self.generated_problem),
            (self.tab3, self.greedy_solution),
            (self.tab4, self.optimized_solution),
            (self.tab5, self.visualization)
        ]:
            sizer = wx.BoxSizer(wx.VERTICAL)
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

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(notebook, 1, wx.EXPAND)
        panel.SetSizer(sizer)

        self.SetSize((800, 600))
        self.Centre()

    def OnTabSize(self, event):
        # Adjust the virtual size of the scrolled window when its size changes
        tab = event.GetEventObject()
        size = tab.GetSize()
        tab.SetVirtualSize(size)
        tab.FitInside()
        event.Skip()

def main():
    app = wx.App()
    ex = SyntheticErrandsSchedulerGUI()
    ex.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()