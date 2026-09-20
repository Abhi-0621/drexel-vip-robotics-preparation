# Project 2 — Husky Autonomous Navigation Demo

## Main Demo Video

[Watch the full Project 2 autonomous navigation demo](https://drive.google.com/file/d/1w5UR_dih85ygnY3_0fE0fwkmEjGzYcJV/view?usp=drivesdk)

The demo shows the complete custom navigation pipeline:

**Goal → Custom A* Planner → Planned Path → Pure Pursuit Controller → Husky Motion**

The A* planner generates a collision-free path through the warehouse occupancy grid, and the Pure Pursuit controller follows the generated path by publishing velocity commands to the simulated Husky robot.


