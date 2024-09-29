import wx
import wx.lib.scrolledpanel as scrolled
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from typing import List, Optional
from algorithms.initial_scheduler import initial_schedule
from algorithms.optimizer import optimize_schedule
from utils.visualization import visualize_schedule
from models.customer import Customer
from models.contractor import Contractor
from models.schedule import Schedule

class VisualizationTab(scrolled.ScrolledPanel):
    def __init__(self, parent: wx.Window) -> None:
        super().__init__(parent, -1, style=wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER)
        self.figure: Figure
        self.canvas: FigureCanvas
        self.sizer: wx.BoxSizer
        self.InitUI()

    def InitUI(self) -> None:
        self.figure = Figure(figsize=(8, 8))
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.SetSizer(self.sizer)
        self.SetupScrolling(scroll_x=True, scroll_y=True, rate_y=20)
        self.SetMinSize((780, 500))  # Set a minimum size for the panel

    def UpdateContent(self, customers: List[Customer], contractors: List[Contractor]) -> None:
        if not self.figure.axes:
            ax: Axes = self.figure.add_subplot(111)
        else:
            ax: Axes = self.figure.axes[0]
        ax.clear()
        
        try:
            # Generate initial schedule and optimize it
            initial_sched: Optional[Schedule] = initial_schedule(customers, contractors)
            if initial_sched is None:
                raise ValueError("Failed to create initial schedule")
            optimized_sched: Optional[Schedule] = optimize_schedule(initial_sched)
            if optimized_sched is None:
                raise ValueError("Failed to optimize schedule")
            
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

    def OnSize(self, event: wx.SizeEvent) -> None:
        self.SetupScrolling(scroll_x=True, scroll_y=True, rate_y=20)
        event.Skip()