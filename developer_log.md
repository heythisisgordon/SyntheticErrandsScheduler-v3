# Developer Log

## Instructions for use:
As you work on the Synthetic Errands Scheduler v3, use this file to keep 
a diary of your development process. For each significant task or milestone 
you complete, add an entry to this log. Include the date, a brief description 
of what you accomplished, any challenges you faced, and any decisions you made.

Example entry format:

[YYYY-MM-DD] Task: Brief description
- Details of what was accomplished
- Challenges faced
- Decisions made
- Next steps or todos

This log will help track the development process and provide insights into 
the evolution of the project. It can be valuable for future reference or 
for onboarding other developers to the project.

Remember to commit this file along with your code changes regularly.

## Project History Summary

- Implemented modular structure with separate directories for models, utils, and algorithms
- Developed basic optimization algorithm and visualization component
- Implemented unit tests for all major components
- Set up test runner and updated README with comprehensive project information
- Implemented GUI with scrolling functionality and Manhattan distance visualization
- Updated travel time calculation to use road-based routing
- Fixed initial scheduler to account for actual errand and travel times
- Adjusted errand prices to ensure reasonable profitability
- Implemented new errand types and characteristics
- Integrated Google OR-Tools for advanced optimization
- Updated project documentation to reflect recent changes
- Implemented centralized constants and capped same-day incentives

## Recent Development Log

[2023-09-30] Task: Implement New Errand Types and Characteristics
- Accomplished:
  - Updated main.py to include new errand types: Delivery, Dog Walk, Cut Grass, Detail Car, Outing, and Moving
  - Modified Errand class to handle new properties like incentives and disincentives
  - Updated initial_scheduler.py and optimizer.py to account for specific requirements of each errand type
  - Updated GUI to display new errand types and their characteristics
- Challenges:
  - Integrating new errand types into the existing system
  - Balancing complexity of different errand types with a unified scheduling approach
  - Implementing incentives and disincentives while maintaining system performance
- Decisions:
  - Implemented flexible structure for errand types to allow easy addition of new types
  - Handled errand-specific logic in the Errand class to keep scheduler and optimizer more generic
  - Used dictionary structure for disincentives to accommodate percentage and fixed-value penalties
- Next steps:
  - Thoroughly test the system with new errand types
  - Update unit tests to cover new errand types and characteristics
  - Refine optimization algorithm for diverse errand types
  - Update visualization component to clearly display different errand types
  - Consider implementing more sophisticated scheduling strategies for complex errand types
  - Update project documentation

[2023-10-01] Task: Resolve Circular Import and Fix Visualization Error
- Accomplished:
  - Resolved circular import issue between models/schedule.py and algorithms/initial_scheduler.py
  - Created utils/errand_utils.py to house the calculate_errand_time function
  - Updated models/schedule.py and algorithms/initial_scheduler.py to import from utils/errand_utils.py
  - Modified utils/visualization.py to handle both axes objects and filenames in visualize_schedule function
  - Updated main.py to use new visualize_schedule function signature
- Challenges:
  - Identifying root cause of circular import issue
  - Ensuring changes didn't introduce new issues in other parts of the codebase
- Decisions:
  - Created new utility file for shared functions to break circular dependency
  - Made visualize_schedule function more flexible by accepting either axes object or filename
- Next steps:
  - Thoroughly test the entire system
  - Update unit tests for new utils/errand_utils.py and modified visualization function
  - Review codebase for potential circular imports or similar issues
  - Update project documentation
  - Consider implementing more robust dependency management system

[2023-10-02] Task: Refactor Initial Scheduler and Update Test Suite
- Accomplished:
  - Modified algorithms/initial_scheduler.py to implement a strictly greedy algorithm
  - Removed considerations for travel time between errands in initial scheduling process
  - Updated tests/test_initial_scheduler.py to align with new greedy approach
  - Removed tests checking for travel time and dynamic scheduling
  - Added new test to ensure customer order preservation in schedule
- Challenges:
  - Balancing between implementing strictly greedy algorithm and maintaining schedule efficiency
  - Ensuring removal of travel time considerations doesn't negatively impact overall system
  - Updating tests to reflect new greedy approach while maintaining comprehensive coverage
- Decisions:
  - Prioritized order of customers in input list over factors like travel time or contractor availability
  - Kept working hours constraint (8:00 AM to 5:00 PM) in initial scheduler
  - Moved more complex scheduling logic to optimization phase
- Next steps:
  - Thoroughly test new initial scheduler with various input scenarios
  - Update optimizer to handle potentially less efficient initial schedules
  - Review and update visualization component to accurately represent new scheduling approach
  - Update project documentation to reflect changes in initial scheduling algorithm
  - Consider implementing separate "smart" initial scheduler for comparison purposes

[2023-10-03] Task: Implement Strictly Greedy Initial Scheduler
- Accomplished:
  - Modified algorithms/initial_scheduler.py to implement a strictly greedy approach
  - Updated the initial_schedule function to schedule errands in the order they appear in the customers list
  - Removed all considerations of travel time and contractor location from the initial scheduling process
  - Updated tests/test_initial_scheduler.py to align with the new strictly greedy approach
  - Added a new test to verify that errands are scheduled at the earliest possible time for each contractor
- Challenges:
  - Ensuring the new approach maintains the working hours constraint (8:00 AM to 5:00 PM)
  - Balancing simplicity of the greedy approach with the need for a functional initial schedule
  - Updating test cases to properly validate the new scheduling behavior
- Decisions:
  - Removed all optimization logic from the initial scheduler, focusing solely on order-based assignment
  - Kept the working hours constraint to ensure schedules remain within operational bounds
  - Updated test suite to focus on order preservation and earliest possible scheduling
- Next steps:
  - Thoroughly test the new initial scheduler with various input scenarios
  - Update the optimizer to handle potentially less efficient initial schedules
  - Review and update the visualization component to accurately represent the new scheduling approach
  - Update project documentation to reflect changes in the initial scheduling algorithm
  - Consider implementing a separate "smart" initial scheduler for comparison purposes
  - Evaluate the impact of the strictly greedy approach on overall system performance and optimization potential

[2023-10-04] Task: Integrate Google OR-Tools for Advanced Optimization
- Accomplished:
  - Integrated Google OR-Tools library into the project for advanced optimization
  - Refactored algorithms/optimizer.py to use OR-Tools for schedule optimization
  - Updated the optimize_schedule function to create and solve a constraint programming model
  - Modified the Schedule class to work with the new optimization approach
  - Updated readme.md to include OR-Tools as a project dependency
- Challenges:
  - Learning and implementing OR-Tools effectively within the existing project structure
  - Translating the scheduling problem into a constraint programming model
  - Ensuring the new optimization approach respects all existing constraints and objectives
- Decisions:
  - Kept the initial greedy scheduler as a starting point for the OR-Tools optimizer
  - Implemented a basic constraint model with room for future refinement and complexity
  - Updated project documentation to reflect the integration of OR-Tools
- Next steps:
  - Thoroughly test the new optimization approach with various problem instances
  - Fine-tune the OR-Tools model parameters for better performance
  - Update unit tests to cover the new optimization logic
  - Evaluate the improvement in schedule quality and profit compared to the previous approach
  - Consider implementing more complex constraints and objectives in the OR-Tools model
  - Update the GUI to reflect any new information or options related to the advanced optimization

[2023-10-05] Task: Update Project Documentation and Refine OR-Tools Integration
- Accomplished:
  - Updated readme.md to reflect the current state of the project, including OR-Tools integration
  - Revised project_scope.md to include new features and adjust project constraints
  - Updated ux_overview.md to describe the new GUI functionality and CLI options
  - Refined the OR-Tools optimization model in algorithms/optimizer.py
  - Updated test cases in tests/test_optimizer.py to cover new optimization scenarios
- Challenges:
  - Ensuring all documentation accurately reflects the current state of the project
  - Balancing the complexity of the OR-Tools model with the need for efficient solving times
  - Designing test cases that effectively validate the new optimization approach
- Decisions:
  - Kept both GUI and CLI modes in the project scope to cater to different user needs
  - Implemented a more detailed constraint model in the OR-Tools optimizer, focusing on time windows and travel times
  - Updated the project's future improvements section to reflect new possibilities with OR-Tools
- Next steps:
  - Conduct comprehensive testing of the entire system, including edge cases
  - Gather user feedback on the new GUI and optimization results
  - Explore additional OR-Tools features that could further improve scheduling efficiency
  - Consider implementing a benchmark system to compare different optimization approaches
  - Investigate potential performance optimizations for larger problem instances

[2023-10-06] Task: Implement Centralized Constants and Cap Same-Day Incentives
- Accomplished:
  - Created a new constants.py file to store centralized constants for errand types, incentives, and other configuration parameters
  - Updated main.py to use the centralized constants for errand types and incentives
  - Modified models/errand.py to cap same-day incentives at 1.5x the base rate
  - Updated gui/problem_definition_tab.py to display capped incentives in the GUI
  - Revised project_scope.md, ux_overview.md, and developer_log.md to reflect these changes
- Challenges:
  - Ensuring consistency across the application when implementing centralized constants
  - Balancing between flexibility and maintainability in constant definitions
  - Updating the GUI to accurately display the capped incentives
- Decisions:
  - Created a separate constants.py file for better organization and easier future modifications
  - Implemented a MAX_INCENTIVE_MULTIPLIER constant to enforce the 1.5x cap consistently
  - Updated the GUI to display both the original incentive and the capped value for clarity
- Next steps:
  - Thoroughly test the system to ensure the capped incentives are correctly applied in all scenarios
  - Update unit tests to cover the new capped incentive logic
  - Review the entire codebase to ensure consistent use of centralized constants
  - Consider implementing a configuration file for easy adjustment of constants without code changes
  - Evaluate the impact of capped incentives on overall system profitability and optimization

[2023-10-07] Task: Improve Maintainability by Integrating New Constants
- Accomplished:
  - Updated constants.py with new constants for errand rates, additional time for specific errand types, working hours, default problem generation parameters, and scheduling period
  - Modified models/errand.py to use ERRAND_RATES and SCHEDULING_DAYS constants
  - Updated utils/errand_utils.py to use DELIVERY_ADDITIONAL_TIME constant
  - Refactored algorithms/initial_scheduler.py and algorithms/optimizer.py to use SCHEDULING_DAYS, WORK_START_TIME, and WORK_END_TIME constants
  - Updated main.py to use DEFAULT_NUM_CUSTOMERS, DEFAULT_NUM_CONTRACTORS, SCHEDULING_DAYS, WORK_START_TIME, and WORK_END_TIME constants
- Challenges:
  - Ensuring all relevant parts of the codebase were updated to use the new constants
  - Maintaining consistency across different modules while introducing centralized constants
  - Balancing between hardcoding values and using constants for better readability and maintainability
- Decisions:
  - Centralized all major configuration values in constants.py for easier maintenance and future modifications
  - Used descriptive names for constants to improve code readability
  - Kept some minor, context-specific values as local variables where appropriate
- Next steps:
  - Thoroughly test the entire system to ensure the new constants are correctly applied and don't introduce any bugs
  - Update unit tests to reflect the use of new constants
  - Review the codebase for any remaining hardcoded values that could be replaced with constants
  - Consider implementing a configuration file or environment variables for dynamic constant setting
  - Update project documentation to reflect the new centralized constants approach

[2023-10-08] Task: Update Test Files to Use New Constants
- Accomplished:
  - Updated tests/test_models.py to use constants for errand types, working hours, and incentive multipliers
  - Modified tests/test_utils.py to incorporate new constants and added a test for calculate_errand_time function
  - Refactored tests/test_initial_scheduler.py to use constants for scheduling days, working hours, and errand types
  - Updated tests/test_optimizer.py to use constants for problem generation and scheduling parameters
- Challenges:
  - Ensuring test cases still cover all necessary scenarios while using centralized constants
  - Maintaining the integrity of existing tests while updating them to use new constants
  - Balancing between using constants and keeping tests readable and easy to understand
- Decisions:
  - Used constants for all major parameters in test cases to ensure consistency with the main codebase
  - Added new test cases where necessary to cover scenarios related to the newly introduced constants
  - Kept some hard-coded values in tests where they serve as specific test inputs or expected outputs
- Next steps:
  - Run the entire test suite to ensure all tests pass with the new changes
  - Review test coverage to identify any gaps introduced by the recent changes
  - Update test documentation to reflect the use of centralized constants
  - Consider adding more edge case tests related to the constants (e.g., boundary conditions for working hours)
  - Evaluate the need for additional integration tests to ensure different components work correctly with the new constants

[2023-10-09] Task: Update Project Documentation and Finalize Constant Integration
- Accomplished:
  - Updated readme.md to include information about centralized constants and their benefits
  - Revised project_scope.md to emphasize the use of centralized constants for improved maintainability
  - Updated ux_overview.md to reflect how centralized constants affect the user experience and system consistency
  - Reviewed and updated all major components to ensure consistent use of centralized constants
  - Added a new section in the developer documentation about working with and modifying constants
- Challenges:
  - Ensuring all documentation accurately reflects the current state of the project after constant integration
  - Balancing between providing detailed information and maintaining readability in documentation
  - Identifying all areas in the documentation that needed updates related to constant usage
- Decisions:
  - Added a dedicated section about centralized constants in readme.md to highlight their importance
  - Updated the project scope to include maintainability through centralized constants as a key feature
  - Emphasized the benefits of centralized constants for both users and developers in ux_overview.md
  - Created a new developer guide section specifically for working with constants
- Next steps:
  - Conduct a final review of all project files to ensure consistent use of centralized constants
  - Consider creating a separate configuration file for easy modification of constants in production
  - Plan for potential future enhancements, such as allowing certain constants to be user-configurable
  - Gather feedback from team members on the new constant-based approach and documentation updates
  - Prepare for the next phase of development, potentially focusing on performance optimizations or new features

[2023-10-10] Task: Fix Visualization Issue in GUI
- Accomplished:
  - Identified and resolved the visualization error in the GUI's visualization tab
  - Updated gui/visualization_tab.py to use the correct parameter name when calling visualize_schedule function
  - Changed 'ax' parameter to 'ax_or_filename' in the visualize_schedule function call
- Challenges:
  - Identifying the root cause of the visualization error
  - Ensuring the fix doesn't introduce new issues in other parts of the application
- Decisions:
  - Kept the flexible design of the visualize_schedule function, allowing it to accept either an axes object or a filename
  - Updated only the necessary part of the code to minimize potential side effects
- Next steps:
  - Thoroughly test the visualization functionality in both GUI and CLI modes
  - Update any relevant documentation or comments related to the visualization function
  - Review other parts of the codebase that might be calling the visualize_schedule function to ensure consistency
  - Consider adding more robust error handling and user feedback in the GUI for visualization-related issues

[2023-10-11] Task: Improve Visibility of Routes in Visualization
- Accomplished:
  - Updated utils/visualization.py to enhance the visibility of routes in the schedule visualization
  - Increased the line width of the routes from 2 to 3
  - Increased the opacity of the routes to 1 (fully opaque)
  - Added a slight offset (0.15) to the routes to prevent them from aligning perfectly with grid lines
  - Reduced the opacity of the city grid from 0.3 to 0.2
  - Increased the size of customer and contractor markers for better visibility
  - Updated the color scheme to use plt.cm.Set1 for better contrast between different contractors
- Challenges:
  - Balancing the visibility of routes with the clarity of other elements in the visualization
  - Ensuring the changes don't negatively impact the overall aesthetics of the visualization
  - Maintaining compatibility with both GUI and CLI visualization outputs
- Decisions:
  - Used a combination of color, opacity, and line width adjustments to improve route visibility
  - Implemented a small offset for routes to prevent them from being hidden by grid lines
  - Kept the city grid visible but with reduced opacity to maintain context while emphasizing routes
- Next steps:
  - Test the updated visualization with various schedule scenarios to ensure consistent improvement
  - Gather user feedback on the new visualization style
  - Consider adding a legend or color coding for different contractors' routes
  - Explore options for interactive visualization features in the GUI (e.g., hover information, zooming)
  - Update relevant documentation to reflect the changes in the visualization component

[2023-10-14] Task: Improve Scheduling Algorithms and Add Detailed Logging
- Accomplished:
  - Updated algorithms/initial_scheduler.py to include travel time considerations and more accurate profit calculations
  - Modified algorithms/optimizer.py to improve the OR-Tools model, including better handling of travel times and more accurate profit calculations in the objective function
  - Implemented detailed logging in both initial_scheduler.py and optimizer.py to provide insights into scheduling decisions and profit calculations
  - Added a schedule comparison feature in optimizer.py to allow side-by-side analysis of initial and optimized schedules
  - Updated main.py to utilize the new logging and comparison features
  - Modified constants.py to include additional parameters needed for the improved algorithms
- Challenges:
  - Balancing the complexity of the initial scheduler while maintaining its greedy nature
  - Ensuring the OR-Tools model accurately represents all constraints and objectives
  - Implementing detailed logging without significantly impacting performance
  - Designing a clear and informative schedule comparison output
- Decisions:
  - Kept the initial scheduler greedy but included travel time considerations for more realistic scheduling
  - Enhanced the OR-Tools model to include travel times between errands and more accurate profit calculations
  - Implemented logging at key decision points in both scheduling algorithms
  - Created a separate function for schedule comparison to keep the code organized
- Next steps:
  - Thoroughly test the updated algorithms with various problem instances to ensure correctness and performance
  - Analyze the logs and comparison outputs to identify any remaining discrepancies between initial and optimized schedules
  - Consider adding visualization improvements to better represent the differences between schedules
  - Update unit tests to cover the new features and ensure they handle edge cases
  - Gather user feedback on the new logging and comparison features
  - Explore options for further optimizing the OR-Tools model, possibly by adjusting solver parameters or adding more sophisticated constraints

# Add your log entries here as you work on the project