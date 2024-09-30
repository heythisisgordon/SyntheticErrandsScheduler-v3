# Sequence Diagrams for Synthetic Errands Scheduler

## Introduction

The sequence diagrams presented here are closely related to the overall system architecture described in the System Architecture Document. They provide a dynamic view of how the components identified in the architecture interact to fulfill the system's requirements. These diagrams complement the static view provided by the system architecture, offering insights into the temporal aspects of the system's behavior.

The following sequence diagrams cover four key system operations:

1. Problem Generation
2. Initial Schedule Creation
3. Schedule Optimization
4. Schedule Visualization

These operations were chosen based on their importance in the system's workflow and their representation of core functionalities. By examining these diagrams, developers and stakeholders can gain a deeper understanding of how the system's components work together to achieve its goals.

## 1. Problem Generation

```mermaid
sequenceDiagram
    participant User
    participant UI as User Interface
    participant PG as Problem Generator
    participant CM as Config Manager
    participant DM as Data Models

    User->>UI: Request problem generation
    UI->>PG: Generate problem(parameters)
    PG->>CM: Get configuration
    CM-->>PG: Configuration data
    PG->>DM: Create Customer objects
    PG->>DM: Create Contractor objects
    PG->>DM: Create Errand objects
    PG-->>UI: Generated problem instance
    UI-->>User: Display problem summary
```

**Description**: This diagram illustrates the process of generating a problem instance. The user initiates the process through the UI, which then calls the Problem Generator. The Problem Generator retrieves necessary configuration data and creates the required data model objects (Customers, Contractors, and Errands). The generated problem instance is then returned to the UI for display to the user.

## 2. Initial Schedule Creation

```mermaid
sequenceDiagram
    participant User
    participant UI as User Interface
    participant IGS as Initial Greedy Scheduler
    participant DM as Data Models
    participant UF as Utility Functions

    User->>UI: Request initial schedule
    UI->>IGS: Create initial schedule(problem)
    IGS->>DM: Get problem data
    DM-->>IGS: Problem data
    loop For each contractor
        IGS->>UF: Calculate travel times
        UF-->>IGS: Travel times
        IGS->>IGS: Assign errands
    end
    IGS->>DM: Create Schedule object
    IGS-->>UI: Initial schedule
    UI-->>User: Display initial schedule
```

**Description**: This sequence shows the creation of an initial schedule using the greedy algorithm. The Initial Greedy Scheduler retrieves the problem data and iterates through each contractor, calculating travel times and assigning errands. It then creates a Schedule object with the assignments and returns it to the UI for display.

## 3. Schedule Optimization

```mermaid
sequenceDiagram
    participant User
    participant UI as User Interface
    participant MO as Modular Optimizer
    participant OA as Optimizer Algorithm
    participant DM as Data Models
    participant UF as Utility Functions

    User->>UI: Request schedule optimization
    UI->>MO: Optimize schedule(initial schedule, algorithm)
    MO->>DM: Get problem and initial schedule data
    DM-->>MO: Problem and schedule data
    MO->>OA: Initialize optimization model
    loop Until optimization complete
        OA->>UF: Calculate objective function
        UF-->>OA: Objective value
        OA->>OA: Update model
    end
    OA-->>MO: Optimized solution
    MO->>DM: Create optimized Schedule object
    MO-->>UI: Optimized schedule
    UI-->>User: Display optimized schedule
```

**Description**: This diagram depicts the process of optimizing a schedule. The Modular Optimizer uses the selected Optimizer Algorithm to improve the initial schedule. The optimization process involves iterative calculations of the objective function and model updates. The final optimized schedule is created and returned to the UI for display.

## 4. Schedule Visualization

```mermaid
sequenceDiagram
    participant User
    participant UI as User Interface
    participant VIS as Visualizer
    participant DM as Data Models
    participant CM as City Map

    User->>UI: Request schedule visualization
    UI->>VIS: Visualize schedule(schedule)
    VIS->>DM: Get schedule data
    DM-->>VIS: Schedule data
    VIS->>CM: Get city layout
    CM-->>VIS: City layout data
    VIS->>VIS: Generate visualization
    VIS-->>UI: Visualization data
    UI-->>User: Display schedule visualization
```

**Description**: This sequence illustrates the process of visualizing a schedule. The Visualizer component retrieves the schedule data and city layout information, generates the visualization, and returns it to the UI for display to the user.

These sequence diagrams provide a detailed view of how different components of the Synthetic Errands Scheduler interact during key operations. They highlight the flow of control and data between various modules, helping developers understand the dynamic behavior of the system. This information is crucial for implementation, debugging, and future enhancements of the system.