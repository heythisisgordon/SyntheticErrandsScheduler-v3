# User Experience Overview

The Synthetic Errands Scheduler v3 is designed with both simplicity and functionality in mind. It features a graphical user interface (GUI) for easy interaction, underpinned by a robust and modular architecture. The system uses centralized constants and utility managers for various functionalities, ensuring consistency across the application and enabling maintainability.

## User Interaction

### GUI Mode:
   - The user runs the program by executing the main.py file.
   - A graphical interface appears with multiple tabs:
     a. Problem Definition: Allows users to set parameters for problem generation and displays errand types with their characteristics, including capped same-day incentives and disincentives for all errand types.
     b. Problem Generation: Displays the randomly generated problem instance.
     c. Greedy Solution: Shows the initial schedule created by the greedy algorithm.
     d. Contractor Schedules: Displays a tabular representation of each contractor's schedule, showing their assigned errands, travel times, and availability based on their calendar.
   - Users can interact with each tab, adjusting parameters and viewing results in real-time.
   - Users can freely navigate between tabs, with informative warnings instead of restrictive error messages.

## Key Features

- Interactive GUI for easy problem definition and result analysis
- Real-time visualization of schedules and city layout
- Detailed output of schedules and profits
- Contractor Schedules tab providing a tabular view of each contractor's assignments, travel times, and availability

This design allows for intuitive interaction through the GUI. It caters to users who prefer visual interaction for scheduling and analysis.

- Problem Definition: Define the parameters for problem generation
The Problem Definition tab in the GUI displays all errand types with their base times (up to 480 minutes), same-day incentives (capped at 1.5x), and disincentives for all errand types.
Users can easily understand and modify the pricing structure for each errand type.
The centralized constants ensure that any future changes to errand types or incentives will be consistently reflected across the entire application.

### Problem Generation Tab
- Generates a random problem instance based on the parameters set in the Problem Definition tab.
- Displays the generated customers and contractors with their respective details.

### Greedy Solution Tab
- Shows the initial schedule created by the greedy algorithm.
- Provides a detailed view of the assignments, including start times, end times, and profits.

### Contractor Schedules Tab
- Provides a tabular representation of each contractor's schedule.
- Contractors are listed in columns with days and hours as rows.
- Clearly displays assigned errands with their start and end times.
- Indicates travel times between errands.
- Offers an easy-to-read format for quick analysis of individual contractor workloads.

## Architecture and User Experience

The refactored architecture, following the MVC pattern, provides several benefits to the user experience:

1. Responsiveness: By separating the UI logic from the business logic, the application remains responsive even during complex calculations.
2. Consistency: The use of centralized managers (UIManager, EventManager, etc.) ensures a consistent user experience across all parts of the application.
3. Reliability: The clear separation of concerns allows for better error handling and logging, reducing the likelihood of unexpected behavior.
4. Flexibility: The modular structure makes it easier to add new features or modify existing ones without disrupting the user experience.

## Visualization

The application provides visualization of the city layout and routes, enhancing the user's understanding of the scheduling problem and solutions.

By implementing a robust and flexible scheduling system with a user-friendly GUI, comprehensive type hinting, and enhanced navigation and visualization options, we've created a foundation that can easily adapt to future requirements while providing a consistent and reliable user experience. The addition of the contractor calendar functionality improves the system's ability to generate realistic and efficient schedules by managing individual contractor availability, especially for large-scale operations.
