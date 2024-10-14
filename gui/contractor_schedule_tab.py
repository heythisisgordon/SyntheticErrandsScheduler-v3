"""
ContractorScheduleTab: Displays the schedule for contractors in a grid format.
"""

import wx
import wx.grid
from typing import List, Dict, Any
from models.schedule import Schedule
from utils.config_manager import ConfigManager
import logging

logger = logging.getLogger(__name__)

class ContractorScheduleTab(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.config = ConfigManager()
        self.init_ui()

    def init_ui(self):
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.grid = wx.grid.Grid(self)
        self.grid.CreateGrid(0, 0)
        self.grid.EnableScrolling(False, True)
        self.grid.ShowScrollbars(wx.SHOW_SB_NEVER, wx.SHOW_SB_ALWAYS)
        self.sizer.Add(self.grid, 1, wx.EXPAND | wx.ALL, 10)
        self.SetSizer(self.sizer)

    def update_schedule(self, col_labels: List[str], row_labels: List[str], grid_data: List[List[str]], grid_colors: List[List[str]]):
        self.setup_grid(col_labels, row_labels)
        self.fill_grid(grid_data, grid_colors)
        self.grid.AutoSize()

    def setup_grid(self, col_labels: List[str], row_labels: List[str]):
        self.grid.ClearGrid()
        if self.grid.GetNumberRows() > 0:
            self.grid.DeleteRows(0, self.grid.GetNumberRows())
        if self.grid.GetNumberCols() > 0:
            self.grid.DeleteCols(0, self.grid.GetNumberCols())
        
        self.grid.AppendRows(len(row_labels))
        self.grid.AppendCols(len(col_labels))

        for i, label in enumerate(col_labels):
            self.grid.SetColLabelValue(i, label)
        for i, label in enumerate(row_labels):
            self.grid.SetRowLabelValue(i, label)

    def fill_grid(self, grid_data: List[List[str]], grid_colors: List[List[str]]):
        for row in range(len(grid_data)):
            for col in range(len(grid_data[row])):
                self.grid.SetCellValue(row, col, grid_data[row][col])
                self.grid.SetCellBackgroundColour(row, col, grid_colors[row][col])

    def show_error(self, message: str):
        wx.MessageBox(message, "Error", wx.OK | wx.ICON_ERROR)
