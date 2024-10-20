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
