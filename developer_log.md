# Developer Log

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

[2023-10-22] Task: Implement Type Hinting in Schedule Model
- Updated models/schedule.py to include type hints for all attributes, method parameters, and return values
- Added necessary imports from typing module (List, Dict, Tuple, Any)
- Updated method signatures to include type annotations
- Challenges: Ensuring correct type annotations for complex data structures like self.assignments
- Decisions: Used Dict[int, List[Tuple[Customer, Contractor, int]]] for self.assignments to accurately represent its structure
- Next: Continue adding type hints to other core modules, run mypy for static type checking, and update related files as needed

[2023-10-23] Task: Review and Document Existing Type Hints in Errand Model
- Discovered that models/errand.py already has comprehensive type hinting implemented
- Reviewed the existing type hints in the Errand class for correctness and completeness
- Noted the use of Union[Dict[str, Union[str, int, float]], None] for the disincentive attribute, which accurately represents its possible types
- Challenges: None, as the type hinting was already well-implemented
- Decisions: No changes needed to the existing type hints in models/errand.py
- Next: Continue with type hinting in other core modules, focusing on those that haven't been updated yet, such as models/customer.py and models/contractor.py

[2023-10-24] Task: Implement Type Hinting in Customer Model
- Updated models/customer.py to include type hints for all attributes, method parameters, and return values
- Added necessary imports from typing module (Dict, List, Tuple)
- Updated class and method signatures to include type annotations
- Added docstrings to the Customer class and its methods to improve documentation
- Challenges: Determining the most appropriate type hint for the availability attribute
- Decisions: Used Dict[int, List[int]] for availability to represent days mapped to lists of available time slots
- Next: Implement type hinting in the Contractor model and continue with other core modules as needed

[2023-10-25] Task: Implement Type Hinting in Contractor Model
- Updated models/contractor.py to include type hints for all attributes, method parameters, and return values
- Added necessary imports from typing module (Dict, List, Tuple)
- Updated class and method signatures to include type annotations
- Added docstrings to the Contractor class and its methods to improve documentation
- Challenges: Determining the most appropriate type hint for the schedule attribute
- Decisions: Used Dict[int, List] for schedule to represent days mapped to lists of assignments (kept as List for flexibility)
- Next: Continue implementing type hinting in other core modules, focusing on utility functions and algorithm files

[2023-10-26] Task: Review and Document Existing Type Hints in Errand Utils
- Discovered that utils/errand_utils.py already has comprehensive type hinting implemented
- Reviewed the existing type hints in the calculate_errand_time function for correctness and completeness
- Noted the use of Tuple[int, int] for location parameters and int for the return type
- Challenges: None, as the type hinting was already well-implemented
- Decisions: No changes needed to the existing type hints in utils/errand_utils.py
- Next: Continue with type hinting in other utility functions and algorithm files, focusing on those that haven't been updated yet, such as utils/travel_time.py and algorithms/initial_scheduler.py

[2023-10-27] Task: Complete Type Hinting Implementation Across the Project
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

[2023-10-28] Task: Update Project Documentation
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

[2023-10-29] Task: Refactor optimizer.py for Improved Code Organization
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

[2023-10-30] Task: Improve Modularity of main.py and Create Separate CLI Interface
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

[2023-10-31] Task: Remove Static Type Checking Implementation and Update Improvement Plan
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

[2023-11-01] Task: Implement Consistent Time Representation
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

[2023-11-02] Task: Fix Time Representation Issues and Improve Error Handling
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

[2023-11-03] Task: Fix Date and Time Handling in Errand Model
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

[2023-11-04] Task: Update GUI Components to Handle Both Integer and Datetime-based Day Representations
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

# Add your log entries here as you work on the project