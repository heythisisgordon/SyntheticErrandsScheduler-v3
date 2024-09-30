# Traceability Matrix

This document provides a mapping between the requirements specified in the Requirements Specification Document (RSD) and the components described in the System Architecture Document.

| Requirement ID | Requirement Description | Architectural Component | Implementation Module |
|----------------|-------------------------|-------------------------|------------------------|
| FR-PR-1 | Represent Busyville as a 100x100 grid | Utility Functions | utils/city_map.py |
| FR-PR-2 | Generate random problem instances | Problem Generation | utils/problem_generator.py |
| FR-PR-3 | Represent errands with specific attributes | Data Models | models/errand.py |
| FR-PR-4 | Represent contractors with specific attributes | Data Models | models/contractor.py |
| FR-SA-1 | Implement initial greedy scheduling algorithm | Scheduling Algorithms | algorithms/initial_greedy_scheduler.py |
| FR-SA-2 | Implement modular optimizer capability | Scheduling Algorithms | algorithms/optimizer.py |
| FR-SA-3 | Support integration of multiple optimizer algorithms | Scheduling Algorithms | algorithms/optimizer.py |
| FR-SA-4 | Provide interface for selecting optimizers | User Interfaces | gui/problem_definition_tab.py, cli_interface.py |
| FR-SA-5 | Allow easy addition of new optimizer algorithms | Scheduling Algorithms | algorithms/optimizer.py |
| FR-TC-1 | Calculate travel times using road-based routing | Utility Functions | utils/travel_time.py |
| FR-TC-2 | Apply same-day incentives | Utility Functions | utils/errand_utils.py |
| FR-TC-3 | Apply disincentives for errand types | Utility Functions | utils/errand_utils.py |
| FR-TC-4 | Calculate final charge for each errand | Utility Functions | utils/errand_utils.py |
| FR-UI-1 | Provide GUI with multiple tabs | User Interfaces | gui/main_frame.py |
| FR-UI-2 | Provide CLI for quick testing | User Interfaces | cli_interface.py |
| FR-UI-3 | Allow setting parameters for problem generation | User Interfaces | gui/problem_definition_tab.py |
| FR-UI-4 | Display randomly generated problem instance | User Interfaces | gui/generated_problem_tab.py |
| FR-UI-5 | Display initial and optimized schedules | User Interfaces | gui/greedy_solution_tab.py, gui/optimized_solution_tab.py |
| FR-UI-6 | Provide visualization of schedules and city layout | Visualization | gui/visualization_tab.py |
| FR-UI-7 | Allow free navigation between tabs with warnings | User Interfaces | gui/main_frame.py |
| FR-UI-8 | Allow setting Base Time values up to 480 minutes | User Interfaces | gui/problem_definition_tab.py |
| FR-UI-9 | Provide Disincentive fields for all errand types | User Interfaces | gui/problem_definition_tab.py |
| FR-UI-10 | Include "Commit Changes Temporarily" button | User Interfaces | gui/problem_definition_tab.py |
| FR-UI-11 | Provide interface for selecting optimizers | User Interfaces | gui/problem_definition_tab.py |
| FR-DM-1 | Use centralized configuration system | Configuration Management | utils/config_manager.py |
| FR-DM-2 | Support loading/saving problem instances and solutions | Data Management | TBD |
| FR-RL-1 | Provide detailed logging of scheduling decisions | Reporting and Logging | various modules |
| FR-RL-2 | Generate visualizations of schedules | Visualization | utils/visualization.py |
| NFR-P-1 | Generate initial schedule within 5 seconds | Scheduling Algorithms | algorithms/initial_greedy_scheduler.py |
| NFR-P-2 | Optimize schedule within 60 seconds | Scheduling Algorithms | algorithms/optimizer.py |
| NFR-U-1 | Intuitive and easy to navigate GUI | User Interfaces | gui/* |
| NFR-U-2 | Provide clear error messages and warnings | User Interfaces, Error Handling | gui/*, cli_interface.py |
| NFR-R-1 | Handle invalid input gracefully | Error Handling | various modules |
| NFR-R-2 | Maintain data integrity | Data Models, Scheduling Algorithms | models/*, algorithms/* |
| NFR-M-1 | Use modular code structure | System Architecture | all modules |
| NFR-M-2 | Implement comprehensive type hinting | System Architecture | all modules |
| NFR-M-3 | Comprehensive unit test suite | Testing | tests/* |
| NFR-PT-1 | Run on Windows, macOS, and Linux | System Architecture | all modules |
| NFR-PT-2 | Compatible with Python 3.7 and higher | System Architecture | all modules |
| NFR-S-1 | Handle problems with up to 100 customers and 20 contractors | Scheduling Algorithms, Data Models | algorithms/*, models/* |
| NFR-S-2 | Allow future expansion of features and algorithms | System Architecture | all modules |

This traceability matrix helps ensure that all requirements are addressed by specific components in the system architecture and provides a clear link between requirements, architectural components, and implementation modules.