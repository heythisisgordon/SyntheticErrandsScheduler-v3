"""
ApplicationController: Manages the overall application flow and coordinates between different components of the Synthetic Errands Scheduler.
"""

import wx
from gui.main_frame import MainFrame
from utils.event_manager import EventManager
from controllers.problem_definition_controller import ProblemDefinitionController
from controllers.problem_generation_controller import ProblemGenerationController
from controllers.greedy_solution_controller import GreedySolutionController
from utils.ui_manager import UIManager
from utils.contractor_schedule_manager import ContractorScheduleManager

class ApplicationController:
    def __init__(self):
        self.app = wx.App()
        self.main_frame = MainFrame(None, title="Synthetic Errands Scheduler")
        self.ui_manager = UIManager(self.main_frame)
        self.event_manager = EventManager(self.main_frame, self.ui_manager)
        self.contractor_schedule_manager = ContractorScheduleManager()

        self.initialize_ui()

        # Initialize controllers
        self.problem_definition_controller = ProblemDefinitionController(self.main_frame.problem_definition_tab, self.event_manager)
        self.problem_generation_controller = ProblemGenerationController(self.main_frame.problem_generation_tab, self.event_manager)
        self.greedy_solution_controller = GreedySolutionController(self.main_frame.greedy_solution_tab, self.event_manager)

        # Bind events after initializing controllers
        self.bind_events()

        self.customers = None
        self.contractors = None

    def initialize_ui(self):
        self.ui_manager.initialize_ui()
        self.main_frame.Show()

    def bind_events(self):
        self.event_manager.bind(EventManager.PROBLEM_DEFINED, self.on_problem_defined)
        self.event_manager.bind(EventManager.PROBLEM_GENERATED, self.on_problem_generated)
        self.event_manager.bind(EventManager.SOLUTION_GENERATED, self.on_solution_generated)
        self.event_manager.bind_ui_events()

        # Bind the "Generate Problem" button event
        self.main_frame.problem_generation_tab.generate_button.Bind(
            wx.EVT_BUTTON, self.on_generate_problem
        )

        # Bind the "Generate Greedy Solution" button event
        self.main_frame.greedy_solution_tab.generate_button.Bind(
            wx.EVT_BUTTON, self.on_generate_greedy_solution
        )

    def on_problem_defined(self, event):
        self.ui_manager.enable_tab(self.main_frame.problem_generation_tab)

    def on_generate_problem(self, event):
        num_customers = self.main_frame.problem_definition_tab.get_num_customers()
        num_contractors = self.main_frame.problem_definition_tab.get_num_contractors()
        contractor_rate = self.main_frame.problem_definition_tab.get_contractor_rate()
        
        self.problem_generation_controller.set_problem_params(num_customers, num_contractors, contractor_rate)
        self.problem_generation_controller.on_generate_problem(event)

    def on_problem_generated(self, event):
        self.customers = event.customers
        self.contractors = event.contractors
        self.ui_manager.enable_tab(self.main_frame.greedy_solution_tab)
        self.main_frame.greedy_solution_tab.enable_generate_button()

    def on_generate_greedy_solution(self, event):
        if self.event_manager.problem_generated:
            self.greedy_solution_controller.on_generate_solution(self.customers, self.contractors)
        else:
            self.main_frame.greedy_solution_tab.show_error("No problem has been generated yet. Please generate a problem first.")

    def on_solution_generated(self, event):
        schedule = event.schedule if hasattr(event, 'schedule') else None
        if schedule:
            self.display_contractor_schedule(schedule)
        self.ui_manager.enable_tab(self.main_frame.contractor_schedule_tab)

    def display_contractor_schedule(self, schedule):
        col_labels, row_labels, grid_data, grid_colors = self.contractor_schedule_manager.prepare_grid_data(schedule)
        self.main_frame.contractor_schedule_tab.update_schedule(col_labels, row_labels, grid_data, grid_colors)

    def run(self):
        self.app.MainLoop()
