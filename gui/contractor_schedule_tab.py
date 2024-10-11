import wx
import wx.grid
from typing import List, Dict, Any
from models.schedule import Schedule
from utils.config_manager import ConfigManager
from controllers.contractor_schedule_controller import ContractorScheduleController
import logging

logger = logging.getLogger(__name__)

class ContractorScheduleTab(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.config = ConfigManager()
        self.controller = ContractorScheduleController()
        self.init_ui()

    def init_ui(self):
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.grid = wx.grid.Grid(self)
        self.grid.CreateGrid(0, 0)
        self.grid.EnableScrolling(False, True)
        self.grid.ShowScrollbars(wx.SHOW_SB_NEVER, wx.SHOW_SB_ALWAYS)
        self.sizer.Add(self.grid, 1, wx.EXPAND | wx.ALL, 10)
        self.SetSizer(self.sizer)

    def update_schedule(self, schedule: Schedule):
        col_labels, row_labels, grid_data, grid_colors = self.controller.prepare_grid_data(schedule)
        
        self.controller.setup_grid(self.grid, col_labels, row_labels)
        self.controller.fill_grid(self.grid, grid_data, grid_colors)

        self.grid.AutoSize()
