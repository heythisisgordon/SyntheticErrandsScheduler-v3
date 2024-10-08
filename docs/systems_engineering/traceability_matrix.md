# Traceability and Verification Matrix

This document provides a mapping between the requirements specified in the Requirements Specification Document (RSD), the components described in the System Architecture Document, and the verification methods and criteria for each requirement.

## Traceability Matrix

| Requirement ID | Requirement Description | Architectural Component | Implementation Module |
|----------------|-------------------------|-------------------------|------------------------|
| FR-PR-1 | Represent Busyville as a 100x100 grid | Utility Functions | utils/city_map.py |
| FR-PR-2 | Generate random problem instances | Problem Generation | utils/problem_generator.py |
| FR-PR-3 | Represent errands with specific attributes | Data Models | models/errand.py |
| FR-PR-4 | Represent contractors with specific attributes and calendars | Data Models | models/contractor.py, models/contractor_calendar.py |
| FR-SA-1 | Implement initial greedy scheduling algorithm | Scheduling Algorithms | algorithms/initial_greedy_scheduler.py |
| FR-SA-2 | Implement modular optimizer capability | Scheduling Algorithms | algorithms/CP_SAT_optimizer.py, algorithms/vehicle_routing_optimizer.py |
| FR-SA-3 | Support integration of multiple optimizer algorithms | Scheduling Algorithms | algorithms/CP_SAT_optimizer.py, algorithms/vehicle_routing_optimizer.py |
| FR-SA-4 | Provide interface for selecting optimizers | User Interfaces | gui/problem_definition_tab.py, cli_interface.py |
| FR-SA-5 | Allow easy addition of new optimizer algorithms | Scheduling Algorithms | algorithms/CP_SAT_optimizer.py, algorithms/vehicle_routing_optimizer.py |
| FR-SA-6 | Respect contractor calendar availability in scheduling | Scheduling Algorithms | algorithms/initial_greedy_scheduler.py, algorithms/CP_SAT_optimizer.py, algorithms/vehicle_routing_optimizer.py |
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
| FR-UI-12 | Display contractor availability based on calendars | User Interfaces | gui/contractor_schedule_tab.py |
| FR-DM-1 | Use centralized configuration system | Configuration Management | utils/config_manager.py |
| FR-DM-2 | Support loading/saving problem instances and solutions | Data Management | TBD |
| FR-DM-3 | Manage and store contractor calendar data | Data Models | models/contractor_calendar.py |
| FR-RL-1 | Provide detailed logging of scheduling decisions | Reporting and Logging | various modules |
| FR-RL-2 | Generate visualizations of schedules | Visualization | utils/visualization.py |
| FR-CM-1 | Allow creation and management of contractor calendars | Data Models | models/contractor_calendar.py |
| FR-CM-2 | Support marking time slots as available/unavailable | Data Models | models/contractor_calendar.py |
| FR-CM-3 | Allow viewing of contractor calendars in GUI | User Interfaces | gui/contractor_schedule_tab.py |
| FR-CM-4 | Ensure scheduling algorithms respect contractor calendars | Scheduling Algorithms | algorithms/initial_greedy_scheduler.py, algorithms/CP_SAT_optimizer.py, algorithms/vehicle_routing_optimizer.py |
| NFR-P-1 | Generate initial schedule within 5 seconds | Scheduling Algorithms | algorithms/initial_greedy_scheduler.py |
| NFR-P-2 | Optimize schedule within 60 seconds | Scheduling Algorithms | algorithms/CP_SAT_optimizer.py, algorithms/vehicle_routing_optimizer.py |
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

## System Requirements Verification Matrix

| Req ID | Description | Verification Method | Verification Criteria | Status |
|--------|-------------|---------------------|----------------------|--------|
| FR-PR-1 | Represent Busyville as a 100x100 grid | Unit Testing | Test case in test_city_map.py verifies grid dimensions | TBV |
| FR-PR-2 | Generate random problem instances | Unit Testing, Integration Testing | test_problem_generator.py verifies customizable customer and contractor numbers | TBV |
| FR-PR-3 | Represent errands with specific attributes | Unit Testing | test_models.py verifies errand attributes | TBV |
| FR-PR-4 | Represent contractors with specific attributes and calendars | Unit Testing | test_models.py verifies contractor attributes and calendar functionality | TBV |
| FR-SA-1 | Implement initial greedy scheduling algorithm | Unit Testing, Integration Testing | test_initial_scheduler.py verifies algorithm functionality | TBV |
| FR-SA-2 | Implement modular optimizer capability | Unit Testing, Integration Testing | test_optimizer.py verifies optimizer functionality | TBV |
| FR-SA-3 | Support multiple optimizer algorithms | Integration Testing, System Testing | Verify multiple optimizers can be integrated and used | TBV |
| FR-SA-4 | Provide interface for optimizer selection | Manual Testing, System Testing | Verify optimizer selection in GUI and CLI | TBV |
| FR-SA-5 | Allow easy addition of new optimizers | Code Review | Review optimizer implementations for extensibility | TBV |
| FR-SA-6 | Respect contractor calendar availability in scheduling | Unit Testing, Integration Testing | Verify schedules respect contractor availability | TBV |
| FR-TC-1 | Calculate travel times using road-based routing | Unit Testing | test_travel_time.py verifies correct calculations | TBV |
| FR-TC-2 | Apply same-day incentives | Unit Testing | test_errand_utils.py verifies incentive calculations | TBV |
| FR-TC-3 | Apply disincentives for all errand types | Unit Testing | test_errand_utils.py verifies disincentive applications | TBV |
| FR-TC-4 | Calculate final charge for each errand | Unit Testing | test_errand_utils.py verifies charge calculations | TBV |
| FR-UI-1 | Provide GUI with multiple tabs | Manual Testing, System Testing | Verify presence and functionality of all GUI tabs | TBV |
| FR-UI-2 | Provide CLI for testing and integration | System Testing | Verify CLI functionality with various commands | TBV |
| FR-UI-3 | Allow setting parameters for problem generation in GUI | Manual Testing | Verify problem generation parameter inputs in GUI | TBV |
| FR-UI-4 | Display generated problem instance in GUI | Manual Testing | Verify problem instance display in GUI | TBV |
| FR-UI-5 | Display initial and optimized schedules in GUI | Manual Testing | Verify schedule displays in GUI | TBV |
| FR-UI-6 | Provide visualization of schedules and city layout | Manual Testing | Verify visualization functionality in GUI | TBV |
| FR-UI-7 | Allow free navigation between GUI tabs | Manual Testing | Verify tab navigation with informative warnings | TBV |
| FR-UI-8 | Allow setting Base Time up to 480 minutes | Manual Testing | Verify Base Time input allows up to 480 minutes | TBV |
| FR-UI-9 | Provide Disincentive fields for all errand types | Manual Testing | Verify presence of Disincentive fields for all types | TBV |
| FR-UI-10 | Include "Commit Changes Temporarily" button | Manual Testing | Verify button functionality in Problem Definition tab | TBV |
| FR-UI-11 | Provide interface for optimizer selection/config | Manual Testing | Verify optimizer selection/config in GUI | TBV |
| FR-UI-12 | Display contractor availability based on calendars | Manual Testing | Verify contractor calendar display in GUI | TBV |
| FR-DM-1 | Use centralized configuration system | Unit Testing, Integration Testing | test_config_manager.py verifies config management | TBV |
| FR-DM-2 | Support loading/saving problem instances and solutions | System Testing | Verify load/save functionality for problems and solutions | TBV |
| FR-DM-3 | Manage and store contractor calendar data | Unit Testing, Integration Testing | Verify contractor calendar data persistence | TBV |
| FR-RL-1 | Provide detailed logging of scheduling decisions | Manual Testing, System Testing | Verify presence and accuracy of logs | TBV |
| FR-RL-2 | Generate visualizations of schedules | Unit Testing, Manual Testing | test_visualization.py and manual verification of visualizations | TBV |
| FR-CM-1 | Allow creation and management of contractor calendars | Unit Testing, Manual Testing | Verify calendar creation and management functionality | TBV |
| FR-CM-2 | Support marking time slots as available/unavailable | Unit Testing, Manual Testing | Verify time slot marking functionality | TBV |
| FR-CM-3 | Allow viewing of contractor calendars in GUI | Manual Testing | Verify calendar display in Contractor Schedules tab | TBV |
| FR-CM-4 | Ensure scheduling algorithms respect contractor calendars | Unit Testing, Integration Testing | Verify schedules respect contractor availability | TBV |
| NFR-P-1 | Generate initial schedule within 5 seconds | Performance Testing | Measure time for 50 customers, 5 contractors | TBV |
| NFR-P-2 | Optimize schedule within 60 seconds | Performance Testing | Measure time for 50 customers, 5 contractors | TBV |
| NFR-U-1 | Provide intuitive and easy-to-navigate GUI | Manual Testing, User Acceptance Testing | User feedback and task completion rates | TBV |
| NFR-U-2 | Provide clear error messages and warnings | Manual Testing, System Testing | Verify clarity and helpfulness of messages | TBV |
| NFR-R-1 | Handle invalid input gracefully | System Testing | Verify system stability with various invalid inputs | TBV |
| NFR-R-2 | Maintain data integrity during scheduling | Integration Testing, System Testing | Verify data consistency throughout process | TBV |
| NFR-M-1 | Use modular code structure | Code Review, Static Analysis | Review of code organization and coupling | TBV |
| NFR-M-2 | Implement comprehensive type hinting | Static Analysis | Verify type hint coverage with mypy or similar tool | TBV |
| NFR-M-3 | Achieve 80% code coverage in unit tests | Unit Testing | Measure code coverage with coverage tool | TBV |
| NFR-PT-1 | Run on Windows, macOS, and Linux | System Testing | Verify functionality on all specified OS | TBV |
| NFR-PT-2 | Compatible with Python 3.7 and higher | System Testing | Verify functionality with Python 3.7+ versions | TBV |
| NFR-S-1 | Handle up to 100 customers and 20 contractors | Performance Testing, System Testing | Verify system performance with max load | TBV |
| NFR-S-2 | Allow future expansion of features and algorithms | Code Review | Review system architecture for extensibility | TBV |

## Verification Status Legend
- TBV: To Be Verified
- Pass: Requirement has been verified and met
- Fail: Requirement has been verified and not met
- N/A: Requirement is not applicable or has been removed

This combined Traceability and Verification Matrix helps ensure that all requirements are addressed by specific components in the system architecture, provides a clear link between requirements, architectural components, and implementation modules, and outlines the verification methods and criteria for each requirement. It should be used throughout the development process to track the implementation and verification status of each requirement. Regular updates and reviews of this matrix will help ensure that all requirements are properly addressed, implemented, and verified before the system is considered complete.