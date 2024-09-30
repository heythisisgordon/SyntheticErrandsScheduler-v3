Project Overview:
Synthetic Errands Inc. is a company that runs errands for clients in a city called Busyville. They need a program to schedule these errands efficiently to maximize profit. Here are the key points:

- Busyville is represented as a 100x100 grid.
- There are 10 errands to be scheduled and 2 contractors available.
- Errands must be completed within a 14-day period.
- Contractors work from 8am to 5pm each day.
- The main goal is to maximize profit.

I've prepared several Python files to guide your work:

readme.py: Provides an overview of the project and its key features.
ux_overview.py: Describes the intended user experience for this version.
project_scope.py: Outlines what's in and out of scope for this project.
developer_log.py: Instructions for maintaining a log of your development process.

Please start by reading through these files to understand the project requirements and constraints. As you work, use the developer_log.py file to keep track of your progress, decisions, and any challenges you face.

Remember, this is a basic version, so focus on implementing the core functionality first. Keep your solution simple and straightforward.

Project: SyntheticErrandsScheduler

Project Structure:

- Directory: SyntheticErrandsScheduler
  - main.py: Main script to generate problem instances, schedule errands, and optimize.
  - algorithms/: Contains algorithms used for initial solving and optimization.
  - models/: Contains data structure definitions (Errand, Contractor, Customer, Schedule).
  - utils/: Contains utility functions (city map representation, travel time calculations, visualization).
  - tests/: Contains unit tests for core functionalities.

Key System Requirements:

- SR1: The system must be modular.
- SR2: The system must represent errands, contractors, and customers with their respective attributes.
- SR3: The system must represent Busyville as a 100x100 grid with roads and non-road areas.
- SR4: The system must calculate travel times based on Manhattan distance.
- SR5: The system must generate problem instances with random customers and contractors.
- SR6: The system must create an initial schedule based on customer availability and contractor proximity.
- SR7: The system must optimize the schedule to maximize profit, respecting all constraints.
- SR8: The system must generate, schedule, and optimize a problem instance in a single execution.
- SR9: The system must output and visualize the final schedule and city layout.
- SR10: The system must calculate and report the total profit.
- SR11: The system must include tests to verify the correctness of core functionalities.
- SR12: The system must have a GUI to facilitate user interaction.

General Instructions:

The project is built around a simple modular structure. Errands, customers, and contractors are represented with basic attributes. The city map is a grid with roads, and travel times are calculated using Manhattan distance. The initial scheduling is handled by a greedy algorithm, and an optimization step is added to improve profit through hill climbing. The system provides detailed output and a visual representation of the schedule. A suite of unit tests ensures the correctness of key components.

This framework adheres to the principle of modularity, allowing for easy maintenance and extension in the future. Be sure to document your changes in the developer_log.md file. Maintain the following files as systems engineering artifacts: initial_instructions.md, project_scope.md, readme.md, and ux_overview.md.
