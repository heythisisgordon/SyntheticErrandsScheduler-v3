# Data Flow Diagram (DFD) for Synthetic Errands Scheduler

## Level 0 (Context) Diagram

```mermaid
graph LR
    %% Define styles for different node types
    classDef user fill:#90A4AE,stroke:#607D8B,color:#000000,stroke-width:2px
    classDef mainSystem fill:#1E88E5,stroke:#1565C0,color:#ffffff,stroke-width:2px
    classDef externalTool fill:#66BB6A,stroke:#43A047,color:#ffffff,stroke-width:2px
    classDef dataStore fill:#FFA726,stroke:#F57C00,color:#000000,stroke-width:2px

    %% Define nodes
    User((User)):::user
    SES[Synthetic Errands Scheduler]:::mainSystem
    ORT[Optimizer Module]:::externalTool
    Config[(Configuration File)]:::dataStore

    %% Define relationships with straight lines
    User -->|Input Parameters| SES
    SES -->|Schedules and Visualizations| User
    SES <-->|Read/Write Config| Config
    SES -->|Optimization Requests| ORT
    ORT -->|Optimization Results| SES

    %% Add title
    subgraph Title[" "]
        direction TB
        TITLE[High-Level System Overview]
        DESC[Synthetic Errands Scheduler System]
    end

    %% Style the title
    classDef title fill:none,stroke:none,color:#333,font-size:18px,font-weight:bold
    class TITLE,DESC title
```

## Level 1 Diagram

```mermaid
graph TD
    %% Define styles for different node types
    classDef user fill:#4A4A4A,stroke:#000000,color:#FFFFFF,stroke-width:2px
    classDef interface fill:#0056B3,stroke:#003A75,color:#FFFFFF,stroke-width:2px
    classDef process fill:#1A8F3C,stroke:#146E2E,color:#FFFFFF,stroke-width:2px
    classDef dataStore fill:#FF8C00,stroke:#CC7000,color:#000000,stroke-width:2px
    classDef utility fill:#8E44AD,stroke:#6C3483,color:#FFFFFF,stroke-width:2px

    %% Define nodes
    User((User)):::user
    Config[(Configuration File)]:::dataStore
    ProblemData[(Problem Data)]:::dataStore
    ScheduleData[(Schedule Data)]:::dataStore
    UI[User Interface]:::interface
    PG[Problem Generator]:::process
    IGS[Initial Greedy Scheduler]:::process
    MO[Modular Optimizer]:::process
    ORT[Optimizer Module]:::process
    VIS[Visualization]:::process

    %% Define relationships
    User -->|Input Parameters| UI
    UI -->|Problem Parameters| PG
    PG -->|Generated Problem| ProblemData
    PG -->|Read Config| Config

    UI -->|Scheduling Request| IGS
    IGS -->|Read Problem| ProblemData
    IGS -->|Initial Schedule| ScheduleData

    UI -->|Optimization Request| MO
    MO -->|Read Problem| ProblemData
    MO -->|Read Initial Schedule| ScheduleData
    MO -->|Optimization Request| ORT
    ORT -->|Optimization Results| MO
    MO -->|Optimized Schedule| ScheduleData

    UI -->|Visualization Request| VIS
    VIS -->|Read Schedule| ScheduleData
    VIS -->|Read Problem| ProblemData
    VIS -->|Visualizations| UI

    UI -->|Results and Visualizations| User

    subgraph Utility_Functions[Utility Functions]
        TT[Travel Time Calculator]:::utility
        CM[City Map]:::utility
        EU[Errand Utils]:::utility
    end

    IGS --> Utility_Functions
    MO --> Utility_Functions
    VIS --> Utility_Functions

    %% Style edge labels and lines
    linkStyle default stroke:#333,stroke-width:2px,fill:none
    
    %% Adjust layout
    Utility_Functions -->|Used by| IGS
    Utility_Functions -->|Used by| MO
    Utility_Functions -->|Used by| VIS
```

## Description

The Data Flow Diagram for the Synthetic Errands Scheduler illustrates how data moves through the system. At the highest level (Level 0), the system interacts with the User, who provides input parameters and receives schedules and visualizations. The system also interacts with a Configuration File for reading and writing settings, and with the Optimizer Module for optimization requests and results.

Diving deeper into Level 1, we can see the main processes and data stores within the system:

1. The User Interface (UI) serves as the primary point of interaction, receiving input from the user and presenting results.

2. The Problem Generator takes parameters from the UI and configuration from the Configuration File to create problem instances, which are stored in the Problem Data store.

3. The Initial Greedy Scheduler reads from the Problem Data store to create an initial schedule, which is then stored in the Schedule Data store.

4. The Modular Optimizer takes optimization requests from the UI, reads the problem and initial schedule data, and interacts with the Optimizer Module to produce an optimized schedule, which is then stored back in the Schedule Data store.

5. The Visualization component reads from both Problem Data and Schedule Data stores to create visualizations that are sent back to the UI for presentation to the user.

Throughout these processes, various Utility Functions (Travel Time Calculator, City Map, and Errand Utils) are used by different components to perform necessary calculations and data manipulations.

Data flows between these components primarily consist of problem parameters, generated problems, initial and optimized schedules, and visualization data. The system design allows for a clear separation of concerns, with distinct processes for problem generation, initial scheduling, optimization, and visualization, all orchestrated through the central User Interface component.

This data flow structure supports the modular nature of the system, allowing for easy updates or replacements of individual components (such as swapping out different optimizer algorithms) without affecting the overall data flow of the system.