"""
ContractorScheduleTab: Displays the schedule for contractors in a grid format.
"""

import wx
import wx.grid
from typing import List, Dict, Any
from models.schedule import Schedule
from utils.config_manager import ConfigManager
from utils.contractor_schedule_manager import ContractorScheduleManager
import logging

logger = logging.getLogger(__name__)

class ContractorScheduleTab(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.config = ConfigManager()
        self.contractor_schedule_manager = ContractorScheduleManager()
        self.init_ui()

    def init_ui(self):
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.grid = wx.grid.Grid(self)
        self.grid.CreateGrid(0, 0)
        self.grid.EnableEditing(False)
        self.grid.EnableDragGridSize(False)
        self.grid.SetScrollbars(20, 20, 50, 50)
        self.sizer.Add(self.grid, 1, wx.EXPAND | wx.ALL, 10)
        self.SetSizer(self.sizer)

        # Enable tooltips
        self.grid.SetToolTip(wx.ToolTip(""))
        self.grid.GetGridWindow().Bind(wx.EVT_MOTION, self.on_mouse_over)

    def update_schedule(self, col_labels: List[str], row_labels: List[str], grid_data: List[List[str]], grid_colors: List[List[str]]):
        self.setup_grid(col_labels, row_labels)
        self.fill_grid(grid_data, grid_colors)
        self.contractor_schedule_manager.merge_day_cells(self.grid)
        self.grid.AutoSizeColumns()
        self.adjust_row_heights()

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
        light_blue = wx.Colour(173, 216, 230)  # RGB values for light blue
        light_green = wx.Colour(144, 238, 144)  # RGB values for light green
        for row in range(len(grid_data)):
            for col in range(len(grid_data[row])):
                self.grid.SetCellValue(row, col, grid_data[row][col])
                if grid_colors[row][col] == 'LIGHT_GREEN':
                    self.grid.SetCellBackgroundColour(row, col, light_green)
                elif grid_colors[row][col] == 'LIGHT_BLUE':
                    self.grid.SetCellBackgroundColour(row, col, light_blue)
                else:
                    self.grid.SetCellBackgroundColour(row, col, wx.WHITE)
                
                # Enable word wrap for all cells
                self.grid.SetCellRenderer(row, col, wx.grid.GridCellAutoWrapStringRenderer())

    def adjust_row_heights(self):
        for row in range(self.grid.GetNumberRows()):
            max_height = 0
            for col in range(self.grid.GetNumberCols()):
                cell_content = self.grid.GetCellValue(row, col)
                if cell_content:
                    # Calculate required height based on content
                    dc = wx.ClientDC(self.grid)
                    dc.SetFont(self.grid.GetCellFont(row, col))
                    width, height = dc.GetMultiLineTextExtent(cell_content)
                    required_height = height + 4  # Add a small buffer
                    max_height = max(max_height, required_height)
            
            if max_height > self.grid.GetRowSize(row):
                self.grid.SetRowSize(row, max_height)

    def on_mouse_over(self, event):
        x, y = self.grid.CalcUnscrolledPosition(event.GetPosition())
        row, col = self.grid.XYToCell(x, y)
        if row >= 0 and col >= 0:
            cell_content = self.grid.GetCellValue(row, col)
            self.grid.GetGridWindow().SetToolTip(cell_content)
        event.Skip()

    def show_error(self, message: str):
        wx.MessageBox(message, "Error", wx.OK | wx.ICON_ERROR)
