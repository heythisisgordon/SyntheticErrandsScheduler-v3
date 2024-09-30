# Developer Log

New entries must be appended to the end of the log. Do not edit or delete previous entries without specific instructions. Do not use placeholders for old entries when editing the developer log; the code has no way to know what data the placeholder represents.

## Project History Summary

- Implemented modular structure with separate directories for models, utils, and algorithms
- Developed basic optimization algorithm, visualization component, and unit tests
- Implemented GUI with scrolling functionality and Manhattan distance visualization
- Updated travel time calculation to use road-based routing
- Implemented new errand types and characteristics
- Integrated Google OR-Tools for advanced optimization
- Implemented centralized constants and capped same-day incentives
- Improved scheduling algorithms and added detailed logging
- Implemented configuration management system
- Added proper logging throughout the application
- Implemented ErrandType enum for improved type safety and maintainability
- Updated test suite to use ErrandType enum
- Implemented consistent logging in key algorithm files
- Enhanced error handling in main module
- Improved error handling in initial scheduler while maintaining greedy approach
- Implemented comprehensive type hinting throughout the entire project

## Recent Development Log

1. Task: Implement Type Hinting in Schedule Model
- Updated models/schedule.py to include type hints for all attributes, method parameters, and return values
- Added necessary imports from typing module (List, Dict, Tuple, Any)
- Updated method signatures to include type annotations
- Challenges: Ensuring correct type annotations for complex data structures like self.assignments
- Decisions: Used Dict[int, List[Tuple[Customer, Contractor, int]]] for self.assignments to accurately represent its structure
- Next: Continue adding type hints to other core modules, run mypy for static type checking, and update related files as needed

2. Task: Review and Document Existing Type Hints in Errand Model
- Discovered that models/errand.py already has comprehensive type hinting implemented
- Reviewed the existing type hints in the Errand class for correctness and completeness
- Noted the use of Union[Dict[str, Union[str, int, float]], None] for the disincentive attribute, which accurately represents its possible types
- Challenges: None, as the type hinting was already well-implemented
- Decisions: No changes needed to the existing type hints in models/errand.py
- Next: Continue with type hinting in other core modules, focusing on those that haven't been updated yet, such as models/customer.py and models/contractor.py

3. Task: Implement Type Hinting in Customer Model
- Updated models/customer.py to include type hints for all attributes, method parameters, and return values
- Added necessary imports from typing module (Dict, List, Tuple)
- Updated class and method signatures to include type annotations
- Added docstrings to the Customer class and its methods to improve documentation
- Challenges: Determining the most appropriate type hint for the availability attribute
- Decisions: Used Dict[int, List[int]] for availability to represent days mapped to lists of available time slots
- Next: Implement type hinting in the Contractor model and continue with other core modules as needed

4. Task: Implement Type Hinting in Contractor Model
- Updated models/contractor.py to include type hints for all attributes, method parameters, and return values
- Added necessary imports from typing module (Dict, List, Tuple)
- Updated class and method signatures to include type annotations
- Added docstrings to the Contractor class and its methods to improve documentation
- Challenges: Determining the most appropriate type hint for the schedule attribute
- Decisions: Used Dict[int, List] for schedule to represent days mapped to lists of assignments (kept as List for flexibility)
- Next: Continue implementing type hinting in other core modules, focusing on utility functions and algorithm files

5. Task: Review and Document Existing Type Hints in Errand Utils
- Discovered that utils/errand_utils.py already has comprehensive type hinting implemented
- Reviewed the existing type hints in the calculate_errand_time function for correctness and completeness
- Noted the use of Tuple[int, int] for location parameters and int for the return type
- Challenges: None, as the type hinting was already well-implemented
- Decisions: No changes needed to the existing type hints in utils/errand_utils.py
- Next: Continue with type hinting in other utility functions and algorithm files, focusing on those that haven't been updated yet, such as utils/travel_time.py and algorithms/initial_scheduler.py

6. Task: Complete Type Hinting Implementation Across the Project
- Implemented type hints in remaining files:
  - utils/travel_time.py
  - utils/city_map.py
  - utils/visualization.py
  - utils/config_manager.py
  - algorithms/initial_scheduler.py
  - algorithms/optimizer.py
  - main.py
  - run_tests.py
  - All files in the gui/ directory
  - All test files in the tests/ directory
- Updated import statements to include necessary types from the typing module
- Added type hints to function parameters, return values, and local variables where appropriate
- Challenges: 
  - Ensuring consistency in type hints across interconnected modules
  - Determining appropriate type hints for complex data structures and function signatures
  - Balancing specificity and flexibility in type hints, especially for functions with multiple possible return types
- Decisions:
  - Used Union types where functions could return different types based on conditions
  - Implemented TypedDict for complex dictionary structures to provide more detailed type information
  - Used Optional types for parameters and return values that could be None
  - Added type hints to test files to maintain consistency across the entire codebase
- Next steps:
  - Run mypy or a similar static type checker to identify any remaining type-related issues
  - Update project documentation to reflect the completion of type hinting implementation
  - Consider implementing static type checking as part of the development workflow

7. Task: Update Project Documentation
- Updated the following documentation files to reflect the implementation of type hints:
  - readme.md: Added information about type hinting in the "Key Features" section and updated the "Contributing" guidelines
  - project_scope.md: Included type hinting implementation in the "In-Scope" and "Deliverables" sections
  - improvement_plan.md: Moved "Use Type Hinting" from "Remaining Tasks" to "Completed Tasks" and updated "Next Steps"
  - ux_overview.md: Added a section on "Type Hinting and Code Quality" to explain the indirect benefits to user experience
- Challenges: Ensuring that the documentation accurately reflects the current state of the project while maintaining readability
- Decisions: 
  - Emphasized the benefits of type hinting for code quality, maintainability, and reliability
  - Updated the "Future Enhancements" section to include static type checking implementation
- Next steps:
  - Continue to monitor and update type hints as the project evolves
  - Consider implementing static type checking as part of the continuous integration process

8. Task: Refactor optimizer.py for Improved Code Organization
- Broke down the large optimize_schedule function into smaller, more focused functions:
  - setup_model_and_variables: Sets up the CP model and variables
  - add_constraints: Adds constraints to the model
  - setup_objective: Sets up the objective function
  - solve_model_and_extract_solution: Solves the model and extracts the solution
- Updated the main optimize_schedule function to use these new functions
- Challenges:
  - Ensuring that the refactored code maintains the same functionality as the original
  - Deciding on the appropriate level of granularity for the new functions
- Decisions:
  - Kept the overall structure of the optimization process while improving readability and maintainability
  - Used type hints consistently in the new functions to maintain code quality
- Next steps:
  - Update the test suite to reflect the changes in the optimizer module
  - Consider similar refactoring for other complex modules in the project

9. Task: Improve Modularity of main.py and Create Separate CLI Interface
- Created a new file cli_interface.py to handle CLI-specific functionality
- Moved problem generation logic to a new file utils/problem_generator.py
- Updated main.py to focus on setting up the application and delegating to the appropriate interface (CLI or GUI)
- Refactored main.py to improve its structure and readability
- Updated cli_interface.py to use the new problem_generator module
- Challenges:
  - Ensuring that the separation of concerns is maintained while keeping the codebase cohesive
  - Deciding on the appropriate level of abstraction for each module
- Decisions:
  - Kept main.py as lean as possible, focusing on high-level application flow
  - Moved CLI-specific logic to cli_interface.py to improve modularity
  - Created a separate problem_generator.py to encapsulate problem generation logic
- Next steps:
  - Update the test suite to reflect the changes in the project structure
  - Review and update import statements across the project to ensure they're using the new module structure
  - Consider creating a similar interface module for GUI functionality if it becomes more complex

10. Task: Remove Static Type Checking Implementation and Update Improvement Plan
- Removed mypy.ini file and __init__.py files created for static type checking
- Updated improvement_plan.md to remove the task related to implementing static type checking
- Adjusted the next steps in the improvement plan to focus on:
  1. Consistent Time Representation
  2. Performance Optimization
  3. Further Error Handling Enhancement
- Challenges:
  - Ensuring all references to static type checking were removed from the project
  - Deciding on the most important next steps for the project
- Decisions:
  - Focused on improving existing functionality and performance rather than adding new tools
  - Prioritized tasks that would have the most immediate impact on the project's usability and efficiency
- Next steps:
  - Begin work on updating time representations to use datetime objects
  - Investigate performance bottlenecks and implement caching where appropriate
  - Review and enhance error handling across all modules

11. Task: Implement Consistent Time Representation
- Updated utils/errand_utils.py to use datetime and timedelta objects
- Modified utils/travel_time.py to return timedelta objects for travel times
- Updated models/schedule.py to use datetime objects for assignments and calculations
- Modified models/customer.py to use datetime and time objects for availability
- Updated models/contractor.py to use datetime objects for scheduling
- Adjusted models/errand.py to work with datetime objects for charge calculations
- Updated algorithms/initial_scheduler.py to use datetime objects consistently
- Modified algorithms/optimizer.py to work with datetime objects in constraints and objective function
- Challenges:
  - Ensuring consistency across all modules when changing time representation
  - Adapting the optimization model to work with datetime objects while maintaining integer constraints
- Decisions:
  - Used datetime.combine() to create full datetime objects when necessary
  - Converted time representations to minutes since midnight for optimization constraints
  - Updated profit calculations to use timedelta.total_seconds() for accurate time-based costs
- Next steps:
  - Update the test suite to reflect the changes in time representation
  - Review and update the GUI components to work with the new datetime representations
  - Investigate potential performance optimizations now that we're using datetime objects

12. Task: Fix Time Representation Issues and Improve Error Handling
- Updated algorithms/initial_scheduler.py to convert WORK_START_TIME and WORK_END_TIME to datetime.time objects
- Modified algorithms/optimizer.py to use the new time objects consistently
- Added error handling for cases where time conversion might fail
- Updated gui/problem_definition_tab.py to import generate_problem from utils/problem_generator.py instead of main.py
- Challenges:
  - Ensuring that all parts of the codebase use the new time representation consistently
  - Identifying and updating all occurrences of the old time representation
- Decisions:
  - Created WORK_START_TIME_OBJ and WORK_END_TIME_OBJ in both initial_scheduler.py and optimizer.py for consistency
  - Used these new time objects throughout the scheduling and optimization processes
- Next steps:
  - Run comprehensive tests to ensure that the time representation changes haven't introduced new bugs
  - Update the documentation to reflect the new time representation approach
  - Continue to optimize performance, focusing on areas where datetime operations might be expensive

13. Task: Fix Date and Time Handling in Errand Model
- Updated models/errand.py to handle both datetime and date objects in apply_incentive, apply_disincentive, and calculate_final_charge methods
- Modified type hints to use Union[datetime, date] for scheduled_date and request_date parameters
- Added logic to extract date from datetime objects when necessary
- Updated docstrings to reflect the changes in accepted types
- Challenges:
  - Ensuring backward compatibility with existing code that might pass either datetime or date objects
  - Maintaining consistency in date comparisons across different methods
- Decisions:
  - Used isinstance checks to handle both datetime and date objects
  - Extracted date from datetime objects to ensure consistent comparisons
  - Updated type hints to clearly indicate that both datetime and date objects are accepted
- Next steps:
  - Update test cases for the Errand model to cover both datetime and date inputs
  - Review other parts of the codebase that interact with the Errand model to ensure compatibility
  - Consider adding similar date/time flexibility to other models if necessary

14. Task: Update GUI Components to Handle Both Integer and Datetime-based Day Representations
- Modified gui/greedy_solution_tab.py and gui/optimized_solution_tab.py to handle both integer-based and datetime.date-based day representations
- Updated the UpdateContent method in both files to use isinstance checks for determining the type of day representation
- Added logic to format the day display string based on the type of day representation (integer or date)
- Modified the start time handling to work with both integer minutes and datetime objects
- Challenges:
  - Ensuring backward compatibility with existing code that might use integer-based day representations
  - Maintaining consistency in day and time displays across different parts of the GUI
- Decisions:
  - Used conditional statements to handle both integer and date-based day representations
  - Implemented a flexible approach to displaying start times, accommodating both integer minutes and datetime objects
  - Kept the changes localized to the GUI components to minimize impact on other parts of the system
- Next steps:
  - Test the GUI thoroughly with both integer-based and date-based schedules to ensure correct display
  - Update the visualization component if necessary to handle the new date representations
  - Consider updating other parts of the system to consistently use datetime objects for improved time handling

15. Task: Implement Vehicle Routing Problem (VRP) Solver and Optimizer Selection
- Created a new file algorithms/vehicle_routing_optimizer.py to implement the VRP solver using Google OR-Tools
- Updated gui/problem_definition_tab.py to include a dropdown for selecting the optimizer (CP-SAT or VRP)
- Modified gui/main_frame.py to store the selected optimizer and pass it to the optimized solution tab
- Updated gui/optimized_solution_tab.py to use the selected optimizer when generating the optimized schedule
- Updated docs/readme.md to include information about the new VRP solver and optimizer selection feature
- Challenges:
  - Integrating the VRP solver with the existing project structure and data models
  - Ensuring that both optimizers (CP-SAT and VRP) can work with the same input data and produce compatible output
- Decisions:
  - Kept the VRP solver implementation separate from the existing CP-SAT solver for modularity
  - Used a strategy pattern to allow easy switching between optimizers in the GUI
  - Updated the Schedule model to accommodate both integer-based and datetime-based representations for compatibility
- Next steps:
  - Implement comprehensive unit tests for the new VRP solver
  - Conduct performance comparisons between the CP-SAT and VRP solvers for various problem sizes
  - Update the CLI interface to allow optimizer selection in command-line mode
  - Consider implementing a hybrid approach that combines both solvers for potentially better results

16. Task: Implement Optimizer Selection in CLI Mode
- Updated main.py to add command-line arguments for selecting the optimizer (CP-SAT or VRP)
- Modified cli_interface.py to accept the optimizer choice as an argument
- Updated the cli_main function in cli_interface.py to use the selected optimizer
- Added error handling for invalid optimizer selections
- Updated the documentation in main.py and cli_interface.py to reflect the new CLI options
- Challenges:
  - Ensuring consistency between GUI and CLI optimizer selection mechanisms
  - Maintaining backward compatibility with existing CLI usage
- Decisions:
  - Used argparse in main.py to handle command-line arguments, including the new --optimizer option
  - Set CP-SAT as the default optimizer to maintain compatibility with existing usage
  - Updated the cli_main function signature to accept the optimizer choice
- Next steps:
  - Update the project documentation (readme.md, ux_overview.md) to include information about CLI optimizer selection
  - Create test cases for CLI optimizer selection
  - Consider adding more detailed output in CLI mode to show which optimizer is being used

17. Task: Rename Initial Scheduler to Initial Greedy Scheduler
- Renamed algorithms/initial_scheduler.py to algorithms/initial_greedy_scheduler.py
- Updated all references to initial_scheduler.py across the project:
  - Modified imports in cli_interface.py, gui/optimized_solution_tab.py, gui/greedy_solution_tab.py, and gui/visualization_tab.py
  - Updated function names from initial_schedule to initial_greedy_schedule
- Updated tests/test_initial_scheduler.py to reflect the new naming convention
- Modified relevant documentation files (readme.md, project_scope.md) to mention the "initial greedy scheduler" instead of just "initial scheduler"
- Challenges:
  - Ensuring all references to the initial scheduler were updated consistently across the project
  - Maintaining backward compatibility with existing code and tests
- Decisions:
  - Kept the basic functionality of the initial greedy scheduler unchanged
  - Updated documentation to emphasize the greedy nature of the initial scheduling algorithm
  - Retained the InitialSchedulingError exception name for consistency
- Next steps:
  - Run comprehensive tests to ensure the renaming didn't introduce any bugs
  - Review the initial greedy scheduler implementation to ensure it adheres to a true greedy approach
  - Consider adding more detailed comments in the initial_greedy_scheduler.py file to explain the greedy algorithm

18. Task: Implement General Optimizer Call and Rename CP-SAT Optimizer
- Renamed 'optimizer.py' to 'CP_SAT_optimizer.py'
- Updated import statements in all relevant files to use the new filename
- Modified main.py to pass the optimizer parameter to both CLI and GUI modes
- Updated gui/main_frame.py to accept and use the optimizer parameter
- Ensured that gui/problem_definition_tab.py correctly updates the selected optimizer
- Verified that gui/optimized_solution_tab.py uses the selected optimizer correctly
- Challenges:
  - Ensuring consistent optimizer selection across both GUI and CLI modes
  - Maintaining backward compatibility with existing code and tests
- Decisions:
  - Used a string parameter ('cp-sat' or 'vrp') to represent the chosen optimizer
  - Implemented conditional logic in relevant parts of the code to use the appropriate optimizer based on the selection
  - Kept the existing optimizer implementations (CP-SAT and VRP) separate for modularity
- Next steps:
  - Update the project documentation (readme.md, ux_overview.md) to reflect the new optimizer selection feature
  - Create additional test cases to ensure proper functioning of both optimizers in various scenarios
  - Consider implementing a factory pattern or dependency injection for more flexible optimizer selection in the future

# Add your log entries here as you work on the project