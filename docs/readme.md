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
│   ├── initial_greedy_scheduler.py
│   ├── CP_SAT_optimizer.py
│   └── vehicle_routing_optimizer.py
│
├── gui/                    # GUI components
│   ├── main_frame.py
│   ├── problem_definition_tab.py
│   ├── generated_problem_tab.py
│   ├── greedy_solution_tab.py
│   ├── optimized_solution_tab.py
│   └── visualization_tab.py
│
├── tests/                  # Unit tests
│   ├── test_models.py
│   ├── test_utils.py
│   ├── test_initial_scheduler.py
│   ├── test_optimizer.py
│   └── test_visualization.py
│
└── docs/                   # Documentation
    ├── readme.md
    ├── project_scope.md
    ├── developer_log.md
    ├── ux_overview.md
    └── systems_engineering/
        ├── requirements_specification_document.md
        ├── system_architecture_document.md
        ├── traceability_matrix.md
        ├── test_plan.md
        ├── interface_control_document.md
        ├── data_flow_diagram.md
        ├── use_case_diagram_and_descriptions.md
        ├── sequence_diagrams.md
        ├── risk_management_plan.md
        └── project_plan.md
```

## Key Features

- Representation of Busyville as a 100x100 grid
- Generation of random problem instances with customizable number of customers and contractors
- Initial scheduling algorithm using a simple greedy approach
- Modular optimizer capability for advanced scheduling optimization
- Ability to select between optimization algorithms in both GUI and CLI modes
- General optimizer call implementation for easy switching between optimizers
- Detailed logging of scheduling decisions and profit calculations
- Side-by-side comparison of initial greedy and optimized schedules
- Visualization of schedules and city layout
- Comprehensive unit test suite
- Graphical User Interface (GUI) for easy interaction
- Centralized configuration management for improved maintainability
- Type hints implemented throughout the codebase for improved readability and maintainability
- Improved GUI navigation with informative warnings instead of restrictive error messages
- Ability to set longer Base Time values (up to 480 minutes) for errand types
- Disincentive fields added for all errand types
- New "Commit Changes Temporarily" button in the Problem Definition tab

## Systems Engineering Documentation

The project now includes comprehensive systems engineering documentation:

1. Requirements Specification Document (RSD): Located at `docs/systems_engineering/requirements_specification_document.md`. This document outlines the functional and non-functional requirements for the system.

2. System Architecture Document: Located at `docs/systems_engineering/system_architecture_document.md`. This document provides an overview of the system's structure, key components, and their interactions.

3. Traceability Matrix: Located at `docs/systems_engineering/traceability_matrix.md`. This document maps the requirements from the RSD to the components described in the System Architecture Document.

4. Test Plan: Located at `docs/systems_engineering/test_plan.md`. This document outlines the strategy for verifying and validating the system requirements, including both automated and manual testing approaches.

5. Interface Control Document (ICD): Located at `docs/systems_engineering/interface_control_document.md`. This document defines the interfaces between system components and with external systems.

6. Data Flow Diagram (DFD): Located at `docs/systems_engineering/data_flow_diagram.md`. This document provides a visual representation of how data moves through the system.

7. Use Case Diagram and Descriptions: Located at `docs/systems_engineering/use_case_diagram_and_descriptions.md`. This document illustrates the system actors and their interactions with the system.

8. Sequence Diagrams: Located at `docs/systems_engineering/sequence_diagrams.md`. This document shows the interactions between objects in the system over time for key operations.

9. Risk Management Plan: Located at `docs/systems_engineering/risk_management_plan.md`. This document identifies potential risks, assesses their impact, and outlines mitigation strategies.

10. Project Plan: Located at `docs/systems_engineering/project_plan.md`. This document outlines the approach for developing the Synthetic Errands Scheduler System, including timelines, milestones, and resource allocation.

These documents provide a robust framework for understanding, developing, and maintaining the Synthetic Errands Scheduler system. They ensure a systematic approach to the project, facilitating better communication among team members and stakeholders, and supporting traceability, testing, and risk management throughout the project lifecycle.

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

In GUI mode, you can select the optimization algorithm using the dropdown menu in the Problem Definition tab.

### CLI Mode

To run the application in command-line interface mode:

```
python main.py --cli
```

To specify the optimizer, use the `--optimizer` option:

```
python main.py --cli --optimizer [optimizer_name]
```

In CLI mode, the program provides detailed logging of the scheduling process, including profit calculations for each errand and a side-by-side comparison of the initial greedy and optimized schedules.

## Running Tests

To run all unit tests:

```
python run_tests.py
```

This will discover and run all tests in the `tests` directory.

## Visualization

The program generates two visualization files when run in CLI mode:
- `initial_greedy_schedule.png`: Visualization of the initial greedy schedule
- `optimized_schedule.png`: Visualization of the optimized schedule

These files show the city layout, customer and contractor locations, and the routes for each day.

In GUI mode, the visualization is displayed in the "Visualization" tab.

## Optimization

The project uses a modular optimizer capability for schedule optimization. This allows for sophisticated optimization techniques, potentially leading to better schedules and higher profits. The optimizer includes:

- Support for multiple optimization algorithms
- Ability to select between optimization algorithms in both GUI and CLI modes
- General optimizer call implementation for easy switching between optimizers
- Detailed logging of optimization decisions
- Consideration of travel time between errands
- Improved profit calculation in the objective function

Users can choose the most appropriate solver based on their specific needs and problem characteristics.

## Logging

The application uses Python's built-in logging module to provide detailed information about its operations. Log messages are displayed in the console and can be useful for debugging or understanding the application's behavior.

## Future Improvements

- Fine-tune optimization parameters for better results
- Implement more complex constraints and objectives in the optimization models
- Add real-time updates and dynamic rescheduling
- Enhance visualization with more detailed information
- Implement more comprehensive error handling
- Add option to save logs to a file
- Investigate and resolve any discrepancies between initial greedy and optimized schedule profits
- Implement static type checking using mypy as part of the development workflow
- Conduct performance comparisons between different optimization algorithms for various problem sizes and characteristics
- Implement a hybrid optimization approach combining multiple optimization strategies

For more details on the project scope and development process, please refer to `project_scope.md` and `developer_log.md`.

## Contributing

Contributions to this project are welcome. Please ensure that you update the `config.yaml` file if you add any new configurable parameters, and update the relevant documentation. Also, make sure to maintain the type hinting standards established in the project when making contributions.