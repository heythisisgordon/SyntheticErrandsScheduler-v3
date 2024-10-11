from utils.ui_manager import UIManager
from utils.event_manager import EventManager
from models.schedule import Schedule

class MainFrameController:
    def __init__(self, main_frame):
        self.main_frame = main_frame
        self.ui_manager = UIManager(main_frame)
        self.event_manager = EventManager(main_frame, self.ui_manager)

    def initialize_ui(self):
        self.ui_manager.create_notebook(self.main_frame.panel)
        self.ui_manager.create_tabs()
        self.event_manager.bind_events()

    def get_tab(self, tab_name: str):
        return self.ui_manager.get_tab(tab_name)

    def enable_greedy_solution(self):
        self.event_manager.enable_greedy_solution()

    def update_contractor_schedule(self, schedule: Schedule):
        self.event_manager.update_contractor_schedule(schedule)
