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
│   ├── schedule.py
│   ├── contractor_calendar.py
│   └── master_contractor_calendar.py
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
│   ├── visualization_tab.py
│   ├── greedy_schedule_visualizer_tab.py
│   └── contractor_schedule_tab.py
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
- Contractor calendar functionality for managing contractor availability and assignments
- MasterContractorCalendar for centralized management of all contractor calendars

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

The project uses a centralized configuration system. The main configuration file is `config.yaml`. This file contains all the configurable parameters for the project, including:

- Errand types and their characteristics
- Working hours
- Scheduling period
- Default problem generation parameters
- Optimization parameters
- Visualization colors

## Running the Application

### GUI Mode (Default)

To run the application with the graphical user interface:

```
python main.py
```

In GUI mode, you can select the optimization algorithm using the dropdown menu in the Problem Definition tab. The application includes several tabs for different functionalities:

- Problem Definition: Define the parameters for problem generation
- Problem Generation: Generate a random problem instance
- Greedy Solution: View the initial greedy schedule
- Optimized Solution: View and compare the optimized schedule
- Contractor Schedules: View a tabular representation of each contractor's schedule
- Greedy Schedule Visualization: Visualize the greedy schedule
- Visualization: Visualize the city layout and routes


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

The program includes visualization of the city layout and route:

- In CLI mode, generates `initial_greedy_schedule.png` and `optimized_schedule.png`
- In GUI mode, displayed in the "Visualization" tab and the "Greedy Schedule Visualization" tab
- Shows the city layout, customer and contractor locations, and the routes for each day
- The greedy schedule visualizer now accurately represents travel time between errands

## Optimization

The project uses a modular optimizer capability for schedule optimization. This allows for sophisticated optimization techniques, potentially leading to better schedules and higher profits. The optimizer includes:

- Support for multiple optimization algorithms
- Ability to select between optimization algorithms in both GUI and CLI modes
- General optimizer call implementation for easy switching between optimizers
- Detailed logging of optimization decisions
- Consideration of travel time between errands
- Improved profit calculation in the objective function
- Integration with contractor calendars to respect availability constraints

Users can choose the most appropriate solver based on their specific needs and problem characteristics.

## Logging

The application uses Python's built-in logging module to provide detailed information about its operations. Log messages are displayed in the console, which can be useful for debugging or understanding the application's behavior. The logging level and format can be configured in the `setup_logging()` function in `main.py`.

For more details on the project scope and development process, please refer to `project_scope.md` and `developer_log.md`.