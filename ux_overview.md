User Experience Overview

The Synthetic Errands Scheduler v3 is designed with both simplicity and functionality in mind. It features a graphical user interface (GUI) for easy interaction, while still maintaining a command-line interface (CLI) option for advanced users. The system now uses centralized constants for errand types, incentives, and other configuration parameters, ensuring consistency across the application and enabling maintainability.

User Interaction:

1. GUI Mode (Default):
   - The user runs the program by executing the main.py file.
   - A graphical interface appears with multiple tabs:
     a. Problem Definition: Allows users to set parameters for problem generation and displays errand types with their characteristics, including capped same-day incentives.
     b. Generated Problem: Displays the randomly generated problem instance.
     c. Greedy Solution: Shows the initial schedule created by the greedy algorithm.
     d. Optimized Solution: Presents the optimized schedule using Google OR-Tools.
     e. Visualization: Provides a visual representation of the schedules and city layout.
   - Users can interact with each tab, adjusting parameters and viewing results in real-time.
   - The visualization tab allows for easy comparison between the initial and optimized schedules.

2. CLI Mode:
   - The user runs the program by executing "python main.py --cli".
   - The program automatically generates a problem instance, creates an initial schedule, and optimizes it.
   - Results are displayed in the console, showing:
     - The initial and optimized schedules for each day
     - Total profit achieved for both schedules
   - Two visualization files are saved: "initial_schedule.png" and "optimized_schedule.png"

Key Features:
- Interactive GUI for easy problem definition and result analysis
- Real-time visualization of schedules and city layout
- Ability to compare initial (greedy) and optimized solutions
- Option to run in CLI mode for quick testing and integration into other workflows
- Detailed output of schedules and profits
- Centralized constants for easy configuration and maintenance
- Same-day incentives capped at 1.5x the base rate for fair pricing

This design allows for both intuitive interaction through the GUI and quick, scriptable execution through the CLI. It caters to users who prefer visual interaction as well as those who need programmatic access to the scheduler's functionality.

Errand Types and Incentives:
- The Problem Definition tab in the GUI now displays all errand types with their base times, same-day incentives (capped at 1.5x), and disincentives.
- Users can easily understand the pricing structure for each errand type.
- The centralized constants ensure that any future changes to errand types or incentives will be consistently reflected across the entire application.

Benefits of Centralized Constants:
- Consistent User Experience: All parts of the application use the same values for critical parameters, ensuring a consistent experience across different features.
- Easier Maintenance: Developers can quickly update key parameters in one place, reducing the risk of inconsistencies and making it easier to modify the system's behavior.
- Improved Reliability: By using centralized constants, the chance of errors due to mismatched values in different parts of the code is significantly reduced.
- Flexibility for Future Enhancements: The centralized constants structure makes it easier to implement future features like user-configurable settings or loading configurations from external files.

Working Hours and Scheduling:
- The application now uses centralized constants for working hours (8:00 AM to 5:00 PM) and the scheduling period (14 days).
- These constants are consistently applied across the initial scheduling, optimization, and visualization components.
- Users can be confident that all generated schedules adhere to these predefined constraints.

Future enhancements may include:
- More advanced problem definition options in the GUI
- Real-time optimization progress display
- Ability to save and load problem instances and solutions
- Integration with external data sources for real-world scheduling scenarios
- Performance optimizations for handling larger-scale problems
- User-configurable errand types and incentives through the GUI
- Option to modify key constants (like working hours or scheduling period) through the GUI or configuration files

By centralizing constants and improving maintainability, we've created a foundation for a more robust and flexible scheduling system that can easily adapt to future requirements while providing a consistent and reliable user experience.