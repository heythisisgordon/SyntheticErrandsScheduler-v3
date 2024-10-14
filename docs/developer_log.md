# Developer Log

Update this Developer Log with SHORT summaries of new work as changes are made to the code. New entries must be appended to the end of the log. Do not edit or delete previous entries without specific instructions.

## 
    GUI Refactorization - Single Responsibility Principle: Created ProblemManager, moved problem generation out of ProblemGenerationTab.

    Further SRP Application: Created ScheduleManager and ScheduleFormatter, moved scheduling logic out of GreedySolutionTab.

    SRP in ContractorScheduleTab: Created ContractorScheduleFormatter, moved formatting logic out of ContractorScheduleTab.

    Refactoring ProblemDefinitionTab: Created ProblemDefinitionManager, moved cost calculation and config logic.

    Refactoring GreedySolutionTab: Created GreedySolutionManager, moved greedy solution logic.

    Further Refactoring ContractorScheduleTab: Created ContractorScheduleManager, moved grid management logic.

    Refactoring MainFrame and GUI Structure: Created UIManager and EventManager for UI operations and event handling.

    Refactoring ProblemDefinitionTab - Controller-View Separation: Created ProblemDefinitionController, moved business logic out of ProblemDefinitionTab.

    Refactoring GreedySolutionTab - Controller-View Separation: Created GreedySolutionController, moved business logic out of GreedySolutionTab.

    Refactoring ContractorScheduleTab - Controller-View Separation: Created ContractorScheduleController, moved business logic out of ContractorScheduleTab.

    Refactoring ProblemGenerationTab - Controller-View Separation: Created ProblemGenerationController, moved business logic out of ProblemGenerationTab.

    Refactoring MainFrame - Controller-View Separation: Created MainFrameController, moved UI initialization and management logic from SyntheticErrandsSchedulerGUI to MainFrameController.

    Refactoring SchedulingUtilities: Created SchedulingUtilities class in scheduling_utils.py, encapsulating scheduling utility functions for better organization and potential state management.

    Refactoring for Consistent Use of SchedulingUtilities: Updated algorithms/initial_greedy_scheduler.py and models/schedule.py to use SchedulingUtilities class consistently. Confirmed other files are using SchedulingUtilities correctly or don't require changes.

    Removed Redundant Calendar Initialization: Deleted utils/calendar_initialization.py and updated related code in utils/schedule_manager.py and algorithms/initial_greedy_scheduler.py to use contractor calendars directly from Contractor objects.

    Major Controller Cleanup: Created ApplicationController to manage overall application flow. Updated all controllers (ProblemDefinitionController, ProblemGenerationController, GreedySolutionController) to focus on coordinating between UI and business logic. Removed ContractorScheduleController and integrated its functionality into ApplicationController. Updated main.py to use new ApplicationController. Refactored GUI components to remove direct controller dependencies, making them pure view components. Implemented dependency injection for services/managers in controllers. Ensured consistent naming conventions and improved type hinting across the codebase. Updated ProblemDefinitionManager for consistency with new structure.

    Removed ProblemManager: Deleted utils/problem_manager.py and updated ProblemGenerationController to use generate_problem function directly from utils/problem_generator.py. This simplifies the code structure by removing an unnecessary abstraction layer.

    Integrated Schedule and ContractorCalendar: Updated Schedule class to use ContractorCalendar instances internally. Modified GreedySolutionManager, ContractorScheduleFormatter, ScheduleFormatter, and visualization module to work with the updated Schedule class. This integration improves the management of assignments and contractor availability.

    Refactoring for Direct Travel Time Calculation: Removed utils/errand_utils.py and its calculate_total_errand_time function. Updated SchedulingUtilities, Schedule, and InitialGreedyScheduler to use calculate_travel_time directly from utils/travel_time.py. This simplifies the code structure and removes unnecessary abstraction. Modified relevant parts of the code to calculate total time by adding travel time and errand base time directly.

    Enhanced ErrandAssignment Structure: Updated ErrandAssignment class in ContractorCalendar to include more detailed time attributes (errand type, travel start/end time, task start/end time, travel duration, total duration). Modified Schedule, InitialGreedyScheduler, SchedulingUtilities, and visualization modules to work with the new ErrandAssignment structure. This change provides more granular information about each assigned errand and improves the overall scheduling process.

    Updated ScheduleFormatter: Modified the ScheduleFormatter class to work with the new ErrandAssignment structure. Updated the format_schedule and format_errand methods to use the new time attributes (travel start/end time, task start/end time, travel duration, total duration) from ErrandAssignment. This change ensures that the schedule formatting correctly reflects the more detailed errand assignment information.
