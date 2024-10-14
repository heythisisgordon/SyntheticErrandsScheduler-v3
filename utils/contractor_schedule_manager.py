from typing import List, Tuple
from models.schedule import Schedule
from utils.contractor_schedule_formatter import ContractorScheduleFormatter
import wx
import wx.grid
import logging

logger = logging.getLogger(__name__)

class ContractorScheduleManager:
    @staticmethod
    def prepare_grid_data(schedule: Schedule) -> Tuple[List[str], List[str], List[List[str]], List[List[str]]]:
        return ContractorScheduleFormatter.format_grid(schedule)

    @staticmethod
    def setup_grid(grid: wx.grid.Grid, col_labels: List[str], row_labels: List[str]) -> None:
        grid.ClearGrid()
        if grid.GetNumberRows() > 0:
            grid.DeleteRows(0, grid.GetNumberRows())
        if grid.GetNumberCols() > 0:
            grid.DeleteCols(0, grid.GetNumberCols())

        grid.AppendCols(len(col_labels))
        grid.AppendRows(len(row_labels))

        for col, label in enumerate(col_labels):
            grid.SetColLabelValue(col, label)
        for row, label in enumerate(row_labels):
            grid.SetRowLabelValue(row, label)

    @staticmethod
    def fill_grid(grid: wx.grid.Grid, grid_data: List[List[str]], grid_colors: List[List[str]]) -> None:
        light_blue = wx.Colour(173, 216, 230)  # RGB values for light blue
        light_green = wx.Colour(144, 238, 144)  # RGB values for light green
        for row in range(len(grid_data)):
            for col in range(len(grid_data[row])):
                grid.SetCellValue(row, col, grid_data[row][col])
                if grid_colors[row][col] == 'LIGHT_GREEN':
                    grid.SetCellBackgroundColour(row, col, light_green)
                elif grid_colors[row][col] == 'LIGHT_BLUE':
                    grid.SetCellBackgroundColour(row, col, light_blue)
                else:
                    grid.SetCellBackgroundColour(row, col, wx.WHITE)

    @staticmethod
    def merge_day_cells(grid: wx.grid.Grid) -> None:
        current_day = None
        start_row = 0
        for row in range(grid.GetNumberRows()):
            day = grid.GetCellValue(row, 0)
            if day:
                if current_day and current_day != day:
                    grid.SetCellSize(start_row, 0, row - start_row, 1)
                    start_row = row
                current_day = day
        
        # Merge the last day's cells
        if current_day:
            grid.SetCellSize(start_row, 0, grid.GetNumberRows() - start_row, 1)
