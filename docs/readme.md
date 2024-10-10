# Synthetic Errands Scheduler

This project implements a scheduling system for Synthetic Errands Inc., a company that runs errands for clients in the city of Busyville.

## Project Structure

The project follows a modular structure to ensure maintainability and scalability:

```
SyntheticErrandsScheduler/
│
├── main.py                 # Main entry point of the application
├── constants.py            # Centralized constants for the project
├── config.yaml             # Configuration file for the project
│
├── models/                 # Data models
│   ├── customer.py
│   ├── contractor.py
│   ├── errand.py
│   ├── schedule.py
│   └── contractor_calendar.py
│
├── utils/                  # Utility functions
│   ├── city_map.py
│   ├── travel_time.py
│   ├── errand_utils.py
│   ├── scheduling_utils.py
│   └── config_manager.py   # Configuration management module
│
├── algorithms/             # Scheduling algorithms
│   ├── initial_greedy_scheduler.py
│   └── CP_SAT_optimizer.py
│
├── gui/                    # GUI components
│   ├── main_frame.py
│   ├── problem_definition_tab.py
│   ├── problem_generation_tab.py
│   ├── greedy_solution_tab.py
│   ├── optimized_solution_tab.py
│   └── contractor_schedule_tab.py
│
└── docs/                   # Documentation
    ├── readme.md
    ├── project_scope.md
    ├── developer_log.md
    └── ux_overview.md
```

## Key Features

- Representation of Busyville as a 100x100 grid
- Generation of random problem instances with customizable number of customers and contractors
- Initial scheduling algorithm using a simple greedy approach
- Modular optimizer capability for advanced scheduling optimization using CP-SAT
- Detailed logging of scheduling decisions and profit calculations
- Side-by-side comparison of initial greedy and optimized schedules
- Graphical User Interface (GUI) for easy interaction
- Centralized configuration management for improved maintainability
- Contractor calendar functionality for managing contractor availability and assignments
- Efficient management of individual contractor calendars for scheduling

## Getting Started

1. Ensure you have Python 3.7+ installed
2. Clone this repository
3. Install required packages:
   ```
   pip install numpy ortools pyyaml
   pip install -U wxPython
   ```
   Note: If you encounter issues installing wxPython, please refer to the official wxPython installation guide for your specific operating system: https://wxpython.org/pages/downloads/

## Configuration

The project uses a centralized configuration system. The main configuration file is `config.yaml`. This file contains all the configurable parameters for the project, including:

- Errand types and their characteristics
- Working hours
- Scheduling period
- Default problem generation parameters
- Optimization parameters

## Running the Application

To run the application with the graphical user interface:

```
python main.py
```

The application includes several tabs for different functionalities:

- Problem Definition: Define the parameters for problem generation
- Problem Generation: Generate a random problem instance
- Greedy Solution: View the initial greedy schedule
- Optimized Solution: View and compare the optimized schedule
- Contractor Schedules: View a tabular representation of each contractor's schedule

## Optimization

The project uses the CP-SAT solver from Google OR-Tools for schedule optimization. This allows for sophisticated optimization techniques, potentially leading to better schedules and higher profits. The optimizer includes:

- Detailed logging of optimization decisions
- Consideration of travel time between errands
- Improved profit calculation in the objective function
- Integration with contractor calendars to respect availability constraints

## Logging

The application uses Python's built-in logging module to provide detailed information about its operations. Log messages are displayed in the console, which can be useful for debugging or understanding the application's behavior. The logging level and format can be configured in the `setup_logging()` function in `main.py`.

For more details on the project scope and development process, please refer to `project_scope.md` and `developer_log.md`.
