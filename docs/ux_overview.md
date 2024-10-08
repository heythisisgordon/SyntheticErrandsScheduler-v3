User Experience Overview

The Synthetic Errands Scheduler v3 is designed with both simplicity and functionality in mind. It features a graphical user interface (GUI) for easy interaction, while still maintaining a command-line interface (CLI) option for advanced users. The system now uses centralized constants for errand types, incentives, and other configuration parameters, ensuring consistency across the application and enabling maintainability.

User Interaction:

1. GUI Mode (Default):
   - The user runs the program by executing the main.py file.
   - A graphical interface appears with multiple tabs:
     a. Problem Definition: Allows users to set parameters for problem generation, select the optimization algorithm (CP-SAT or VRP), and displays errand types with their characteristics, including capped same-day incentives and disincentives for all errand types.
     b. Generated Problem: Displays the randomly generated problem instance.
     c. Greedy Solution: Shows the initial schedule created by the greedy algorithm.
     d. Optimized Solution: Presents the optimized schedule using the selected algorithm (CP-SAT or VRP) from Google OR-Tools.
     e. Visualization: Provides a visual representation of the schedules and city layout.
     f. Greedy Schedule Visualizer: Offers an interactive, detailed view of the greedy schedule solution with accurate travel time representation.
     g. Contractor Schedules: Displays a tabular representation of each contractor's schedule, showing their assigned errands, travel times, and availability based on their calendar.
   - Users can interact with each tab, adjusting parameters and viewing results in real-time.
   - The visualization tab allows for easy comparison between the initial and optimized schedules.
   - Users can now freely navigate between tabs, with informative warnings instead of restrictive error messages.

2. CLI Mode:
   - The user runs the program by executing "python main.py --cli".
   - The program automatically generates a problem instance, creates an initial schedule, and optimizes it using the default optimization algorithm.
   - Results are displayed in the console, showing:
     - The initial and optimized schedules for each day
     - Total profit achieved for both schedules
   - Two visualization files are saved: "initial_schedule.png" and "optimized_schedule.png"

Key Features:
- Interactive GUI for easy problem definition and result analysis
- Real-time visualization of schedules and city layout
- Ability to compare initial (greedy) and optimized solutions
- Option to select between CP-SAT and VRP optimization algorithms in the GUI
- Option to run in CLI mode for quick testing and integration into other workflows
- Detailed output of schedules and profits
- Interactive Greedy Schedule Visualizer with accurate travel time representation
- Contractor Schedules tab providing a tabular view of each contractor's assignments, travel times, and availability

This design allows for both intuitive interaction through the GUI and quick, scriptable execution through the CLI. It caters to users who prefer visual interaction as well as those who need programmatic access to the scheduler's functionality.

- Problem Definition: Define the parameters for problem generation
The Problem Definition tab in the GUI displays all errand types with their base times (up to 480 minutes), same-day incentives (capped at 1.5x), and disincentives for all errand types.
Users can easily understand and modify the pricing structure for each errand type.
The centralized constants ensure that any future changes to errand types or incentives will be consistently reflected across the entire application.

- Problem Generation: Generate a random problem instance
- Greedy Solution: View the initial greedy schedule
- Optimized Solution: Run the schedule optimizer and view the results
  - Users can choose between two optimization algorithms in the GUI:
    1. Constraint Programming (CP-SAT) Solver: Focuses on maximizing profit while respecting all constraints.
    2. Vehicle Routing Problem (VRP) Solver: Optimizes routes for contractors, potentially reducing travel time and increasing efficiency.
  - The selected algorithm is used to generate the optimized schedule, allowing users to compare the results of different approaches.
  - This feature provides flexibility in solving the scheduling problem and allows for performance comparisons between different approaches.

- Contractor Schedules: Provides a tabular representation of each contractor's schedule.
    - Contractors listed in columns with days and hours as rows
    - Clear display of assigned errands with their start and end times
    - Indication of travel times between errands
    - Easy-to-read format for quick analysis of individual contractor workloads
    - Direct implementation of code values allows verificatin of code functions
 
- Greedy Schedule Visualization: Provides a detailed visualization of the greedy schedule solution.
  - Features of the visualizer include:
    - Contractors displayed on the left side and days along the top
    - Errands placed in their corresponding contractor/date-time slots
    - Accurate representation of travel time between errands
    - Different colors used for travel time, errand performance time, and same-day incentive indicators
    - Interactive elements allowing users to hover over errands for more detailed information
  - Helps users verify scheduler functions, identify patterns, potential inefficiencies, and opportunities for optimization in the greedy solution.

- Visualization: Visualize the city layout and routes

By centralizing constants, improving maintainability, implementing comprehensive type hinting, providing multiple optimization strategies, and enhancing GUI navigation and visualization options, we've created a foundation for a more robust and flexible scheduling system that can easily adapt to future requirements while providing a consistent and reliable user experience. The addition of the contractor calendar functionality and the MasterContractorCalendar further improves the system's ability to generate realistic and efficient schedules, especially for large-scale operations.