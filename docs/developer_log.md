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
