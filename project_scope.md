Project Scope: Synthetic Errands Scheduler v3

Objective:
Develop a modular Synthetic Errands Scheduler that addresses the basic use case outlined in the Capstone Kickoff.

In-Scope:
1. Modular project structure with separate directories for models, utils, and algorithms
2. Representation of Busyville as a 100x100 grid with roads
3. Basic data structures for errands, contractors, and customers
4. Simple travel time calculation using Manhattan distance
5. Generation of random problem instances (10 errands, 2 contractors)
6. Greedy algorithm for initial scheduling in a separate module
7. Basic optimization algorithm to maximize profit (to be implemented)
8. Console output of the final schedule and profit
9. Basic visualization of the schedule and city layout (to be implemented)
10. Unit tests for core functionalities (to be implemented)
11. User input for problem parameters (to be implemented)

Out-of-Scope:
1. Advanced optimization techniques
2. Real-time traffic considerations
3. Multiple optimization objectives (focus solely on profit)
4. deprecated, ignore
5. Graphical user interface
6. Persistent data storage
7. Advanced error handling and logging
8. Performance optimizations for large-scale problems

Constraints:
- Must use Python 3.8 or higher
- Limited to basic Python libraries and numpy, matplotlib for visualization
- Must complete scheduling within a 14-day period
- Must adhere to contractor working hours (8am to 5pm)

Deliverables:
1. Functional Python program implementing the scheduler with a modular structure
2. Basic visualization of the schedule (to be implemented)
3. Unit test suite (to be implemented)
4. README file with instructions for running the program and explanation of the modular structure
5. Brief documentation of the implemented algorithms and data structures

Note: This version emphasizes a modular approach to software design, allowing for easier maintenance, testing, and future enhancements.