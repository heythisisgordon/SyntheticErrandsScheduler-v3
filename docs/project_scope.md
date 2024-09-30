Project Scope: Synthetic Errands Scheduler v3

Objective:
Develop a modular and maintainable Synthetic Errands Scheduler that addresses the basic use case outlined in the Capstone Kickoff, incorporating advanced optimization techniques and centralized configuration for improved consistency and ease of modification. Implement a robust systems engineering framework to ensure a comprehensive and well-documented approach to the project.

In-Scope:
1. Modular project structure with separate directories for models, utils, algorithms, and GUI components
2. Representation of Busyville as a 100x100 grid with roads
3. Comprehensive data structures for errands, contractors, and customers
4. Travel time calculation using road-based routing
5. Generation of random problem instances with customizable number of customers and contractors
6. Greedy algorithm for initial scheduling in a separate module
7. Advanced optimization algorithms:
   a. Constraint Programming (CP-SAT) solver using Google OR-Tools to maximize profit
   b. Vehicle Routing Problem (VRP) solver using Google OR-Tools for route optimization
8. User-selectable optimization algorithm in both GUI and CLI modes
9. Console output and GUI display of the initial and optimized schedules and profits
10. Detailed visualization of the schedule and city layout
11. Comprehensive unit test suite for all major components
12. User input for problem parameters via GUI
13. Centralized constants file (constants.py) for improved maintainability, including:
    - Errand types and their characteristics
    - Working hours and scheduling period
    - Default problem generation parameters
    - Incentive and disincentive rules
14. Consistent use of centralized constants across all modules
15. Detailed logging of scheduling decisions and profit calculations
16. Side-by-side comparison of initial and optimized schedules
17. Improved travel time consideration in both initial and optimized scheduling
18. Enhanced profit calculation in the optimization objective function
19. Implementation of comprehensive type hints throughout the codebase for improved readability and maintainability
20. Improved GUI navigation with informative warnings instead of restrictive error messages
21. Ability to set longer Base Time values (up to 480 minutes) for errand types
22. Disincentive fields added for all errand types
23. New "Commit Changes Temporarily" button in the Problem Definition tab
24. Implementation of a comprehensive systems engineering framework, including:
    - Requirements Specification Document (RSD)
    - System Architecture Document
    - Traceability Matrix
    - Test Plan
    - Interface Control Document (ICD)
    - Data Flow Diagram (DFD)
    - Use Case Diagram and Descriptions
    - Sequence Diagrams
    - Risk Management Plan
    - Project Plan

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
10. Updated optimization algorithms with improved travel time consideration and profit calculation
11. Comprehensive type hints implemented throughout the codebase
12. Multiple optimization strategies (CP-SAT and VRP) with user-selectable option in both GUI and CLI modes
13. Improved GUI navigation with informative warnings
14. Extended Base Time range for errand types (up to 480 minutes)
15. Disincentive fields for all errand types
16. Temporary changes functionality in the Problem Definition tab
17. Systems Engineering Framework documents:
    a. Requirements Specification Document (RSD)
    b. System Architecture Document
    c. Traceability Matrix
    d. Test Plan
    e. Interface Control Document (ICD)
    f. Data Flow Diagram (DFD)
    g. Use Case Diagram and Descriptions
    h. Sequence Diagrams
    i. Risk Management Plan
    j. Project Plan

Note: This version emphasizes a modular approach to software design, incorporates advanced optimization techniques, and provides a user-friendly interface, allowing for easier maintenance, testing, and future enhancements. The use of centralized constants ensures consistency across the application and simplifies future modifications to errand types, incentives, and other key parameters. This approach significantly improves the maintainability of the project by reducing the need for changes across multiple files when updating core business rules or configuration settings. The addition of detailed logging and schedule comparison features enhances the ability to analyze and improve the scheduling algorithms. The implementation of comprehensive type hints throughout the codebase further improves code readability, helps catch potential type-related bugs earlier, and enhances overall maintainability. The inclusion of multiple optimization strategies (CP-SAT and VRP) provides flexibility in solving different types of scheduling problems and allows for performance comparisons between different approaches. The improved GUI navigation, extended Base Time range, addition of disincentive fields for all errand types, and the new temporary changes functionality in the Problem Definition tab enhance the user experience and provide more flexibility in problem definition and exploration.

The implementation of a comprehensive systems engineering framework ensures a well-documented and structured approach to the project. This framework provides a solid foundation for understanding the system requirements, architecture, and interactions, facilitating better communication among team members and stakeholders. It also supports traceability, testing, and risk management throughout the project lifecycle, contributing to the overall quality and reliability of the Synthetic Errands Scheduler system.