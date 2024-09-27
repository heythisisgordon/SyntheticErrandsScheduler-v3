# Synthetic Errands Scheduler

This project implements a scheduling system for Synthetic Errands Inc., a company that runs errands for clients in the city of Busyville.

## Project Structure

The project follows a modular structure to ensure maintainability and scalability:

```
SyntheticErrandsScheduler/
│
├── main.py                 # Main entry point of the application
├── run_tests.py            # Script to run all unit tests
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
│   └── visualization.py
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
- Optimization algorithm to maximize profit
- Visualization of schedules and city layout
- Comprehensive unit test suite
- Graphical User Interface (GUI) for easy interaction

## Getting Started

1. Ensure you have Python 3.7+ installed
2. Clone this repository
3. Install required packages:
   ```
   pip install numpy matplotlib
   pip install -U wxPython
   ```
   Note: If you encounter issues installing wxPython, please refer to the official wxPython installation guide for your specific operating system: https://wxpython.org/pages/downloads/

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

## Future Improvements

- Implement more sophisticated optimization algorithms
- Add real-time updates and dynamic rescheduling
- Enhance visualization with more detailed information
- Implement error handling and logging throughout the application

For more details on the project scope and development process, please refer to `project_scope.md` and `developer_log.md`.