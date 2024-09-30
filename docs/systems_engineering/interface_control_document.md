# Interface Control Document (ICD) for Synthetic Errands Scheduler

## 1. Introduction

This Interface Control Document (ICD) defines the interfaces between the major components of the Synthetic Errands Scheduler system and any external systems. It specifies the data exchanged, formats, and protocols for each interface to ensure proper integration and communication between components.

## 2. System Components

The Synthetic Errands Scheduler consists of the following main components:

1. User Interfaces (GUI and CLI)
2. Problem Generation
3. Scheduling Algorithms
4. Data Models
5. Utility Functions
6. Configuration Management
7. Visualization

## 3. Interface Definitions

### 3.1 User Interfaces to Backend

#### 3.1.1 GUI to Backend

- **Description**: Interface between the GUI components and the backend systems.
- **Data Exchanged**:
  - Input: User parameters for problem generation and optimization
  - Output: Problem instance data, schedules, visualization data
- **Format**: Python objects (dictionaries, lists, custom classes)
- **Protocol**: Direct function calls

#### 3.1.2 CLI to Backend

- **Description**: Interface between the CLI and the backend systems.
- **Data Exchanged**:
  - Input: Command-line arguments for problem generation and optimization
  - Output: Text-based representation of problem instances, schedules, and results
- **Format**: String arguments, formatted text output
- **Protocol**: Command-line argument parsing, stdout for output

### 3.2 Problem Generation to Data Models

- **Description**: Interface for creating problem instances using data models.
- **Data Exchanged**: Customer, Contractor, and Errand objects
- **Format**: Python objects (instances of Customer, Contractor, and Errand classes)
- **Protocol**: Direct function calls

### 3.3 Scheduling Algorithms to Data Models

- **Description**: Interface for algorithms to access and modify schedule data.
- **Data Exchanged**: Schedule objects, Customer objects, Contractor objects, Errand objects
- **Format**: Python objects (instances of Schedule, Customer, Contractor, and Errand classes)
- **Protocol**: Direct function calls, object methods

### 3.4 Scheduling Algorithms to Utility Functions

- **Description**: Interface for algorithms to use utility functions for calculations.
- **Data Exchanged**: Input parameters for calculations, calculation results
- **Format**: Python primitive types (int, float, tuple, list, dict)
- **Protocol**: Function calls

### 3.5 Visualization to Data Models and Utility Functions

- **Description**: Interface for accessing data to generate visualizations.
- **Data Exchanged**: Schedule data, city map data, calculation results
- **Format**: Python objects and primitive types
- **Protocol**: Function calls

### 3.6 Configuration Management to Other Components

- **Description**: Interface for accessing configuration settings across the system.
- **Data Exchanged**: Configuration parameters
- **Format**: Python dictionary
- **Protocol**: Function calls to get/set configuration values

## 4. External Interfaces

### 4.1 System to File System

- **Description**: Interface for reading/writing files (e.g., configuration, problem instances, results).
- **Data Exchanged**: File contents (configuration data, problem data, results)
- **Format**: YAML for configuration, custom format for problem instances and results
- **Protocol**: File I/O operations

### 4.2 System to Google OR-Tools

- **Description**: Interface to the external Google OR-Tools library for optimization.
- **Data Exchanged**: Optimization model parameters, constraints, and results
- **Format**: OR-Tools specific objects and methods
- **Protocol**: Library function calls

## 5. Interface Constraints and Assumptions

1. All internal interfaces assume in-memory data transfer and are not designed for distributed systems.
2. The GUI and CLI interfaces assume single-user interaction and are not designed for concurrent multi-user access.
3. File I/O operations are assumed to have necessary read/write permissions in the operating system.
4. The Google OR-Tools library is assumed to be installed and accessible in the Python environment.

## 6. Data Formats

### 6.1 Configuration File (config.yaml)

```yaml
working_hours:
  start: 480  # minutes from midnight
  end: 1020   # minutes from midnight

scheduling_period: 14  # days

errand_types:
  - name: "Shopping"
    base_time: 60
    base_charge: 50
  # ... other errand types ...

# ... other configuration parameters ...
```

### 6.2 Problem Instance Format

```python
{
    "customers": [
        {"id": 1, "location": (x, y), "errands": [...]},
        # ... other customers ...
    ],
    "contractors": [
        {"id": 1, "location": (x, y)},
        # ... other contractors ...
    ],
    "errands": [
        {"id": 1, "type": "Shopping", "location": (x, y), "customer_id": 1},
        # ... other errands ...
    ]
}
```

### 6.3 Schedule Format

```python
{
    "contractor_id": 1,
    "schedule": {
        1: [  # Day 1
            {"errand_id": 1, "start_time": 480, "end_time": 540},
            # ... other errands ...
        ],
        # ... other days ...
    }
}
```

## 7. Error Handling

1. All interfaces should include appropriate error handling and reporting mechanisms.
2. Invalid inputs should result in meaningful error messages propagated to the user interface.
3. External system failures (e.g., file system errors, OR-Tools errors) should be caught and reported clearly.

## 8. Future Considerations

1. Design interfaces with extensibility in mind to accommodate future additional optimizer algorithms.
2. Consider defining a standardized API for optimizer plugins to facilitate easy integration of new algorithms.
3. Plan for potential future interfaces with external data sources or web services for real-world scheduling scenarios.

This Interface Control Document serves as a reference for developers working on different components of the Synthetic Errands Scheduler. It should be updated as the system evolves to ensure it remains an accurate representation of the system's interfaces.