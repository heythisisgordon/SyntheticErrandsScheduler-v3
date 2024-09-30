# System Requirements Verification Matrix

This matrix outlines the verification methods and criteria for each requirement of the Synthetic Errands Scheduler system. It serves as a tool to ensure that all requirements are properly verified and validated throughout the development process.

## Functional Requirements

| Req ID | Description | Verification Method | Verification Criteria | Status |
|--------|-------------|---------------------|----------------------|--------|
| FR-PR-1 | Represent Busyville as a 100x100 grid | Unit Testing | Test case in test_city_map.py verifies grid dimensions | TBV |
| FR-PR-2 | Generate random problem instances | Unit Testing, Integration Testing | test_problem_generator.py verifies customizable customer and contractor numbers | TBV |
| FR-PR-3 | Represent errands with specific attributes | Unit Testing | test_models.py verifies errand attributes | TBV |
| FR-PR-4 | Represent contractors with specific attributes | Unit Testing | test_models.py verifies contractor attributes | TBV |
| FR-SA-1 | Implement initial greedy scheduling algorithm | Unit Testing, Integration Testing | test_initial_scheduler.py verifies algorithm functionality | TBV |
| FR-SA-2 | Implement modular optimizer capability | Unit Testing, Integration Testing | test_optimizer.py verifies optimizer functionality | TBV |
| FR-SA-3 | Support multiple optimizer algorithms | Integration Testing, System Testing | Verify multiple optimizers can be integrated and used | TBV |
| FR-SA-4 | Provide interface for optimizer selection | Manual Testing, System Testing | Verify optimizer selection in GUI and CLI | TBV |
| FR-SA-5 | Allow easy addition of new optimizers | Code Review | Review optimizer.py for extensibility | TBV |
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
| FR-DM-1 | Use centralized configuration system | Unit Testing, Integration Testing | test_config_manager.py verifies config management | TBV |
| FR-DM-2 | Support loading/saving problem instances and solutions | System Testing | Verify load/save functionality for problems and solutions | TBV |
| FR-RL-1 | Provide detailed logging of scheduling decisions | Manual Testing, System Testing | Verify presence and accuracy of logs | TBV |
| FR-RL-2 | Generate visualizations of schedules | Unit Testing, Manual Testing | test_visualization.py and manual verification of visualizations | TBV |

## Non-Functional Requirements

| Req ID | Description | Verification Method | Verification Criteria | Status |
|--------|-------------|---------------------|----------------------|--------|
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

This System Requirements Verification Matrix should be used throughout the development process to track the verification status of each requirement. Regular updates and reviews of this matrix will help ensure that all requirements are properly addressed and verified before the system is considered complete.