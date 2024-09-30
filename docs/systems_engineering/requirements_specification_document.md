# Requirements Specification Document (RSD) for Synthetic Errands Scheduler

## 1. Introduction

The Synthetic Errands Scheduler is a software system designed to optimize the scheduling of errands for Synthetic Errands Inc., a company that runs errands for clients in the city of Busyville. This document outlines the functional and non-functional requirements for the system.

## 2. Functional Requirements

### 2.1 Problem Representation (FR-PR)

FR-PR-1: The system shall represent Busyville as a 100x100 grid. [Priority: High]
FR-PR-2: The system shall support the generation of random problem instances with customizable numbers of customers and contractors. [Priority: High]
FR-PR-3: The system shall represent errands with specific types, locations, and time requirements. [Priority: High]
FR-PR-4: The system shall represent contractors with specific working hours and locations. [Priority: High]

### 2.2 Scheduling Algorithms (FR-SA)

FR-SA-1: The system shall implement an initial greedy scheduling algorithm. [Priority: High]
FR-SA-2: The system shall implement a modular optimizer capability for advanced scheduling optimization. [Priority: High]
FR-SA-3: The system shall support the integration of multiple optimizer algorithms. [Priority: High]
FR-SA-4: The system shall provide an interface for selecting and configuring different optimizer algorithms. [Priority: Medium]
FR-SA-5: The system shall allow for easy addition of new optimizer algorithms without modifying existing code. [Priority: Medium]

### 2.3 Time and Cost Calculations (FR-TC)

FR-TC-1: The system shall calculate travel times between locations using road-based routing. [Priority: High]
FR-TC-2: The system shall apply same-day incentives capped at 1.5x the base rate for eligible errands. [Priority: High]
FR-TC-3: The system shall apply disincentives for all errand types when applicable. [Priority: Medium]
FR-TC-4: The system shall calculate the final charge for each errand based on base rate, incentives, and disincentives. [Priority: High]

### 2.4 User Interface (FR-UI)

FR-UI-1: The system shall provide a Graphical User Interface (GUI) with multiple tabs for different functionalities. [Priority: High]
FR-UI-2: The system shall provide a Command-Line Interface (CLI) for quick testing and integration into other workflows. [Priority: Medium]
FR-UI-3: The GUI shall allow users to set parameters for problem generation. [Priority: High]
FR-UI-4: The GUI shall display the randomly generated problem instance. [Priority: Medium]
FR-UI-5: The GUI shall display the initial greedy schedule and the optimized schedule. [Priority: High]
FR-UI-6: The GUI shall provide a visualization of the schedules and city layout. [Priority: Medium]
FR-UI-7: The GUI shall allow users to navigate freely between tabs with informative warnings. [Priority: Low]
FR-UI-8: The GUI shall allow users to set Base Time values up to 480 minutes for errand types. [Priority: Medium]
FR-UI-9: The GUI shall provide Disincentive fields for all errand types. [Priority: Medium]
FR-UI-10: The GUI shall include a "Commit Changes Temporarily" button in the Problem Definition tab. [Priority: Low]
FR-UI-11: The GUI shall provide an interface for selecting and configuring optimizer algorithms. [Priority: Medium]

### 2.5 Data Management (FR-DM)

FR-DM-1: The system shall use a centralized configuration system for managing constants and parameters. [Priority: High]
FR-DM-2: The system shall support loading and saving of problem instances and solutions. [Priority: Low]

### 2.6 Reporting and Logging (FR-RL)

FR-RL-1: The system shall provide detailed logging of scheduling decisions and profit calculations. [Priority: Medium]
FR-RL-2: The system shall generate visualizations of initial and optimized schedules. [Priority: Medium]

## 3. Non-Functional Requirements

### 3.1 Performance (NFR-P)

NFR-P-1: The system shall generate an initial schedule for a problem with 50 customers and 5 contractors within 5 seconds on a standard desktop computer. [Priority: High]
NFR-P-2: The system shall optimize a schedule for a problem with 50 customers and 5 contractors within 60 seconds on a standard desktop computer. [Priority: High]

### 3.2 Usability (NFR-U)

NFR-U-1: The GUI shall be intuitive and easy to navigate for users with basic computer skills. [Priority: Medium]
NFR-U-2: The system shall provide clear error messages and warnings to guide users. [Priority: Medium]

### 3.3 Reliability (NFR-R)

NFR-R-1: The system shall handle invalid input gracefully without crashing. [Priority: High]
NFR-R-2: The system shall maintain data integrity throughout the scheduling process. [Priority: High]

### 3.4 Maintainability (NFR-M)

NFR-M-1: The system shall use a modular code structure to facilitate easy maintenance and updates. [Priority: High]
NFR-M-2: The system shall implement comprehensive type hinting throughout the codebase. [Priority: Medium]
NFR-M-3: The system shall have a comprehensive unit test suite with at least 80% code coverage. [Priority: Medium]

### 3.5 Portability (NFR-PT)

NFR-PT-1: The system shall run on Windows, macOS, and Linux operating systems. [Priority: Medium]
NFR-PT-2: The system shall be compatible with Python 3.7 and higher versions. [Priority: High]

### 3.6 Scalability (NFR-S)

NFR-S-1: The system shall be capable of handling problems with up to 100 customers and 20 contractors. [Priority: Medium]
NFR-S-2: The system architecture shall allow for future expansion of features and optimization algorithms. [Priority: Low]

## 4. Traceability Matrix

| Requirement ID | Verified By | Implemented In |
|----------------|-------------|----------------|
| FR-PR-1 | test_city_map.py | utils/city_map.py |
| FR-PR-2 | test_problem_generator.py | utils/problem_generator.py |
| FR-PR-3 | test_models.py | models/errand.py |
| FR-PR-4 | test_models.py | models/contractor.py |
| FR-SA-1 | test_initial_scheduler.py | algorithms/initial_greedy_scheduler.py |
| FR-SA-2 | test_optimizer.py | algorithms/optimizer.py |
| FR-SA-3 | test_optimizer.py | algorithms/optimizer.py |
| FR-SA-4 | test_main.py, test_cli_interface.py | main.py, cli_interface.py |
| FR-SA-5 | code review | algorithms/optimizer.py |
| FR-TC-1 | test_travel_time.py | utils/travel_time.py |
| FR-TC-2 | test_errand_utils.py | utils/errand_utils.py |
| FR-TC-3 | test_errand_utils.py | utils/errand_utils.py |
| FR-TC-4 | test_errand_utils.py | utils/errand_utils.py |
| FR-UI-1 | manual testing | gui/main_frame.py |
| FR-UI-2 | test_cli_interface.py | cli_interface.py |
| FR-UI-3 | manual testing | gui/problem_definition_tab.py |
| FR-UI-4 | manual testing | gui/generated_problem_tab.py |
| FR-UI-5 | manual testing | gui/greedy_solution_tab.py, gui/optimized_solution_tab.py |
| FR-UI-6 | manual testing | gui/visualization_tab.py |
| FR-UI-7 | manual testing | gui/main_frame.py |
| FR-UI-8 | manual testing | gui/problem_definition_tab.py |
| FR-UI-9 | manual testing | gui/problem_definition_tab.py |
| FR-UI-10 | manual testing | gui/problem_definition_tab.py |
| FR-UI-11 | manual testing | gui/problem_definition_tab.py |
| FR-DM-1 | test_config_manager.py | utils/config_manager.py |
| FR-DM-2 | TBD | TBD |
| FR-RL-1 | manual testing | various modules |
| FR-RL-2 | test_visualization.py | utils/visualization.py |

Note: Non-functional requirements are typically verified through a combination of testing, code review, and performance analysis across the entire system.

## 5. Verification Methods

- Unit Testing: Automated tests for individual components and functions.
- Integration Testing: Tests to ensure different parts of the system work together correctly.
- System Testing: End-to-end tests of the entire system.
- Performance Testing: Tests to measure system performance under various conditions.
- Manual Testing: Human-driven tests, especially for UI components and user experience.
- Code Review: Expert examination of the code for quality, maintainability, and adherence to requirements.
- Static Analysis: Automated tools to check code quality and identify potential issues.

## 6. Validation

The system will be considered valid when it meets all high-priority requirements and at least 80% of medium-priority requirements. Validation will involve:

1. Comprehensive testing using the methods outlined in Section 5.
2. User acceptance testing with representatives from Synthetic Errands Inc.
3. Performance benchmarking to ensure the system meets efficiency requirements.
4. Code quality assessment using static analysis tools and manual review.

## 7. Future Considerations

- Implementation of additional optimizer algorithms to enhance scheduling capabilities.
- Integration with external data sources for real-world scheduling scenarios.
- Development of a web-based interface for broader accessibility.
- Implementation of real-time updates and dynamic rescheduling capabilities.

This Requirements Specification Document serves as a foundation for the development and evaluation of the Synthetic Errands Scheduler. It should be reviewed and updated regularly as the project evolves.