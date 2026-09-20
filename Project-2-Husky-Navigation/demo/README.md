# Project 2 — Husky Autonomous Navigation Demo

## Demo Video

[Watch the full autonomous navigation demo here](PASTE_GOOGLE_DRIVE_LINK_HERE)

The video demonstrates the complete custom navigation pipeline:

**Goal → Custom A* Planner → Planned Path → Pure Pursuit Controller → Husky Motion**

The A* planner generates a collision-free path through the warehouse occupancy grid, and the Pure Pursuit controller follows the generated path by publishing velocity commands to the simulated Husky robot.

