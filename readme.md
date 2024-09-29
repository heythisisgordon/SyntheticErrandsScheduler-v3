# Synthetic Errands Scheduler

This project implements a scheduling system for Synthetic Errands Inc., a company that runs errands for clients in the city of Busyville.

## Project Structure

The project follows a modular structure to ensure maintainability and scalability:

```
SyntheticErrandsScheduler/
│
├── main.py                 # Main entry point of the application
├── run_tests.py            # Script to run all unit tests
├── constants.py            # Centralized constants for the project
├── config.yaml             # Configuration file for the project
│
├── models/                 # Data models
│   ├── customer.py
│   ├── contractor.py
│   ├── errand.py
│   └── schedule.py
│
├── utils/                  # Utility functions
│   ├── city_map.py
│   ├── travel_time.py
│   ├── errand_utils.py
│   ├── visualization.py
│   └── config_manager.py   # Configuration management module
│
├── algorithms/             # Scheduling algorithms
│   ├── initial_scheduler.py
│   └── optimizer.py
│
├── gui/                    # GUI components
│   ├── main_frame.py
│   ├── problem_definition_tab.py
│   ├── generated_problem_tab.py
│   ├── greedy_solution_tab.py
│   ├── optimized_solution_tab.py
│   └── visualization_tab.py
│
└── tests/                  # Unit tests
    ├── test_models.py
    ├── test_utils.py
    ├── test_initial_scheduler.py
    ├── test_optimizer.py
    └── test_visualization.py
```

## Key Features

- Representation of Busyville as a 100x100 grid
- Generation of random problem instances with customizable number of customers and contractors
- Initial scheduling algorithm using a greedy approach
- Optimization algorithm using Google OR-Tools to maximize profit
- Detailed logging of scheduling decisions and profit calculations
- Side-by-side comparison of initial and optimized schedules
- Visualization of schedules and city layout
- Comprehensive unit test suite
- Graphical User Interface (GUI) for easy interaction
- Centralized configuration management for improved maintainability
- Type hints implemented throughout the codebase for improved readability and maintainability

## Type Hinting

The entire codebase has been updated with comprehensive type hints. This includes:

- Type annotations for all function parameters and return values
- Type hints for class attributes and local variables
- Use of complex types from the `typing` module (e.g., List, Dict, Tuple, Optional) where appropriate

These type hints improve code readability, catch potential type-related bugs earlier, and make the codebase more maintainable. They also provide better support for IDEs and static type checkers like mypy.

## Getting Started

1. Ensure you have Python 3.7+ installed
2. Clone this repository
3. Install required packages:
   ```
   pip install numpy matplotlib ortools pyyaml
   pip install -U wxPython
   ```
   Note: If you encounter issues installing wxPython, please refer to the official wxPython installation guide for your specific operating system: https://wxpython.org/pages/downloads/

## Configuration

The project now uses a centralized configuration system. The main configuration file is `config.yaml`. This file contains all the configurable parameters for the project, including:

- Errand types and their characteristics
- Working hours
- Scheduling period
- Default problem generation parameters
- Optimization parameters

To modify any of these settings, edit the `config.yaml` file. The changes will be automatically reflected in the application without needing to modify the code.

## Running the Application

### GUI Mode (Default)

To run the application with the graphical user interface:

```
python main.py
```

### CLI Mode

To run the application in command-line interface mode:

```
python main.py --cli
```

In CLI mode, the program now provides detailed logging of the scheduling process, including profit calculations for each errand and a side-by-side comparison of the initial and optimized schedules.

## Running Tests

To run all unit tests:

```
python run_tests.py
```

This will discover and run all tests in the `tests` directory.

## Visualization

The program generates two visualization files when run in CLI mode:
- `initial_schedule.png`: Visualization of the initial schedule
- `optimized_schedule.png`: Visualization of the optimized schedule

These files show the city layout, customer and contractor locations, and the routes for each day.

In GUI mode, the visualization is displayed in the "Visualization" tab.

## Optimization

The project uses Google OR-Tools for schedule optimization. This powerful library allows for sophisticated constraint programming and optimization techniques, potentially leading to better schedules and higher profits. The optimizer now includes:

- Detailed logging of optimization decisions
- Consideration of travel time between errands
- Improved profit calculation in the objective function

## Logging

The application now uses Python's built-in logging module to provide detailed information about its operations. Log messages are displayed in the console and can be useful for debugging or understanding the application's behavior.

## Future Improvements

- Fine-tune OR-Tools parameters for better optimization results
- Implement more complex constraints and objectives in the optimization model
- Add real-time updates and dynamic rescheduling
- Enhance visualization with more detailed information
- Implement more comprehensive error handling
- Add option to save logs to a file
- Investigate and resolve any discrepancies between initial and optimized schedule profits
- Implement static type checking using mypy as part of the development workflow

For more details on the project scope and development process, please refer to `project_scope.md` and `developer_log.md`.

## Contributing

Contributions to this project are welcome. Please ensure that you update the `config.yaml` file if you add any new configurable parameters, and update the relevant documentation. Also, make sure to maintain the type hinting standards established in the project when making contributions.