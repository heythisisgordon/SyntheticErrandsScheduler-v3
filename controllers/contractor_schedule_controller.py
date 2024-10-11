from typing import List, Tuple
from models.schedule import Schedule
from utils.contractor_schedule_manager import ContractorScheduleManager

class ContractorScheduleController:
    @staticmethod
    def prepare_grid_data(schedule: Schedule) -> Tuple[List[str], List[str], List[List[str]], List[List[str]]]:
        return ContractorScheduleManager.prepare_grid_data(schedule)

    @staticmethod
    def setup_grid(grid, col_labels: List[str], row_labels: List[str]) -> None:
        ContractorScheduleManager.setup_grid(grid, col_labels, row_labels)

    @staticmethod
    def fill_grid(grid, grid_data: List[List[str]], grid_colors: List[List[str]]) -> None:
        ContractorScheduleManager.fill_grid(grid, grid_data, grid_colors)
