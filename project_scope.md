Project Scope: Synthetic Errands Scheduler v3

Objective:
Develop a modular and maintainable Synthetic Errands Scheduler that addresses the basic use case outlined in the Capstone Kickoff, incorporating advanced optimization techniques and centralized configuration for improved consistency and ease of modification.

In-Scope:
1. Modular project structure with separate directories for models, utils, algorithms, and GUI components
2. Representation of Busyville as a 100x100 grid with roads
3. Comprehensive data structures for errands, contractors, and customers
4. Travel time calculation using road-based routing
5. Generation of random problem instances with customizable number of customers and contractors
6. Greedy algorithm for initial scheduling in a separate module
7. Advanced optimization algorithm using Google OR-Tools to maximize profit
8. Console output and GUI display of the initial and optimized schedules and profits
9. Detailed visualization of the schedule and city layout
10. Comprehensive unit test suite for all major components
11. User input for problem parameters via GUI
12. Centralized constants file (constants.py) for improved maintainability, including:
    - Errand types and their characteristics
    - Working hours and scheduling period
    - Default problem generation parameters
    - Incentive and disincentive rules
13. Consistent use of centralized constants across all modules
14. Detailed logging of scheduling decisions and profit calculations
15. Side-by-side comparison of initial and optimized schedules
16. Improved travel time consideration in both initial and optimized scheduling
17. Enhanced profit calculation in the optimization objective function
18. Implementation of comprehensive type hints throughout the codebase for improved readability and maintainability

Out-of-Scope:
1. Real-time traffic considerations
2. Multiple optimization objectives (focus solely on profit)
3. Persistent data storage
4. Advanced error handling and logging
5. Performance optimizations for large-scale problems (>100 customers or >10 contractors)

Constraints:
- Must use Python 3.7 or higher
- Uses numpy and matplotlib for calculations and visualization
- Uses Google OR-Tools for advanced optimization
- Uses wxPython for GUI implementation
- Must complete scheduling within a 14-day period
- Must adhere to contractor working hours (8am to 5pm)
- Same-day incentives must be capped at 1.5x the base rate

Deliverables:
1. Functional Python program implementing the scheduler with a modular structure
2. Advanced visualization of the schedule and city layout
3. Comprehensive unit test suite
4. README file with instructions for running the program and explanation of the modular structure
5. Detailed documentation of the implemented algorithms and data structures
6. Graphical User Interface for easy interaction and visualization
7. Centralized constants file (constants.py) for easy configuration and maintenance
8. Detailed logging system for both initial and optimized scheduling processes
9. Schedule comparison feature for side-by-side analysis of initial and optimized schedules
10. Updated optimization algorithm with improved travel time consideration and profit calculation
11. Comprehensive type hints implemented throughout the codebase

Note: This version emphasizes a modular approach to software design, incorporates advanced optimization techniques, and provides a user-friendly interface, allowing for easier maintenance, testing, and future enhancements. The use of centralized constants ensures consistency across the application and simplifies future modifications to errand types, incentives, and other key parameters. This approach significantly improves the maintainability of the project by reducing the need for changes across multiple files when updating core business rules or configuration settings. The addition of detailed logging and schedule comparison features enhances the ability to analyze and improve the scheduling algorithms. The implementation of comprehensive type hints throughout the codebase further improves code readability, helps catch potential type-related bugs earlier, and enhances overall maintainability.