import wx
import wx.lib.scrolledpanel as scrolled
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
from algorithms.initial_scheduler import initial_schedule
from algorithms.optimizer import optimize_schedule
from utils.visualization import visualize_schedule

class VisualizationTab(scrolled.ScrolledPanel):
    def __init__(self, parent):
        super().__init__(parent, -1, style=wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER)
        self.InitUI()

    def InitUI(self):
        self.figure = Figure(figsize=(8, 8))
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.SetSizer(self.sizer)
        self.SetupScrolling(scroll_x=True, scroll_y=True, rate_y=20)
        self.SetMinSize((780, 500))  # Set a minimum size for the panel

    def UpdateContent(self, customers, contractors):
        if not self.figure.axes:
            ax = self.figure.add_subplot(111)
        else:
            ax = self.figure.axes[0]
        ax.clear()
        
        try:
            # Generate initial schedule and optimize it
            initial_sched = initial_schedule(customers, contractors)
            optimized_sched = optimize_schedule(initial_sched)
            
            # Create the visualization
            visualize_schedule(optimized_sched, ax_or_filename=ax)
            
            # Adjust the plot
            ax.set_title("Optimized Schedule Visualization")
            ax.set_xlabel("X coordinate")
            ax.set_ylabel("Y coordinate")
            self.figure.tight_layout()
            
        except Exception as e:
            ax.text(0.5, 0.5, f"Error generating visualization:\n{str(e)}", 
                    ha='center', va='center', wrap=True)
        
        self.canvas.draw()
        self.SetupScrolling(scroll_x=True, scroll_y=True, rate_y=20)
        self.Refresh()
        self.Update()

    def OnSize(self, event):
        self.SetupScrolling(scroll_x=True, scroll_y=True, rate_y=20)
        event.Skip()