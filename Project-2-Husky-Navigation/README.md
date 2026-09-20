# Project 2 — Husky Autonomous Navigation

## Overview

This project implements autonomous navigation for a simulated Clearpath Husky robot using ROS 2 Humble and Gazebo.

Instead of relying on the built-in Nav2 planner and controller, I implemented two classical robotics algorithms:

* **A*** for global path planning
* **Pure Pursuit** for path tracking and robot control

The robot uses a 2D LiDAR and AMCL localization to navigate through a simulated warehouse environment.

## Objective

The goal of this project was to understand and implement the two major components of autonomous mobile robot navigation:

**Planning:** Determine a collision-free route from the robot's current position to a goal.

**Control:** Generate velocity commands that cause the robot to follow that route.

The final pipeline is:

`Occupancy Grid + Robot Pose + Goal → A* → Path → Pure Pursuit → cmd_vel → Husky`

## Simulation Environment

The project uses:

* ROS 2 Humble
* Clearpath Husky A200
* Gazebo simulation
* RViz
* 2D LiDAR
* AMCL localization
* Python
* `rclpy`

The simulated warehouse provides obstacles and free space for testing autonomous navigation.

## ROS 2 Inputs and Outputs

The custom planner uses:

`/a200_0000/map`

Provides the warehouse occupancy grid.

`/a200_0000/amcl_pose`

Provides the estimated position and orientation of the Husky.

`/goal_pose`

Provides the requested navigation destination.

The A* planner publishes:

`/a200_0000/custom_path`

The Pure Pursuit controller subscribes to this path and publishes:

`/a200_0000/cmd_vel`

These velocity commands control the Husky.

## Custom A* Planner

The A* planner is implemented in:

`src/astar_planner.py`

The algorithm first converts the robot's world coordinates and goal coordinates into occupancy-grid coordinates.

It then searches the map using an 8-connected grid, allowing horizontal, vertical, and diagonal movement.

For each candidate node, A* calculates:

`f(n) = g(n) + h(n)`

where:

`g(n)` is the cost traveled from the starting cell.

`h(n)` is the estimated Euclidean distance from the current cell to the goal.

The planner avoids occupied and unknown cells and prevents diagonal movement through obstacle corners.

After reaching the goal, the algorithm reconstructs the path by following the stored parent nodes back toward the starting position.

The resulting grid coordinates are converted back into world coordinates and published as a ROS 2 `nav_msgs/Path`.

## Pure Pursuit Controller

The path-following controller is implemented in:

`src/pure_pursuit_controller.py`

Pure Pursuit continuously selects a point ahead of the robot on the A* path.

The selected point is transformed from the map coordinate frame into the robot's local coordinate frame.

The controller then calculates the curvature required to reach the lookahead point.

The angular velocity is approximately determined using:

`angular velocity = linear velocity × curvature`

The resulting linear and angular velocities are published as `geometry_msgs/Twist` commands to:

`/a200_0000/cmd_vel`

This causes the Husky to continuously steer toward the path while moving forward.

When the robot is within the defined goal tolerance, the controller publishes zero velocity and stops the robot.

## Navigation Pipeline

The complete system works as follows:

`Warehouse Map`

↓

`Current Husky Pose`

↓

`Navigation Goal`

↓

`Custom A* Planner`

↓

`Custom Path`

↓

`Pure Pursuit Controller`

↓

`Linear + Angular Velocity`

↓

`Husky`

## Testing and Results

The custom A* planner successfully generated paths through the simulated warehouse environment.

The generated path was published to `/a200_0000/custom_path` and visualized in RViz.

The Pure Pursuit controller successfully received the generated path and produced velocity commands that moved the simulated Husky toward the navigation goal.

The final demonstration showed the full navigation pipeline operating without using Nav2's built-in planner or controller.

## Challenges and Debugging

Several issues arose while building the system.

### Gazebo Rendering

The Gazebo simulation initially crashed while rendering the LiDAR-equipped robot. The simulation worked after switching to software rendering using:

`LIBGL_ALWAYS_SOFTWARE=1`

### ROS 2 QoS

The map and AMCL pose publishers used transient-local durability.

The custom planner initially did not receive previously published map and pose messages. Matching the subscriber QoS settings to the Clearpath publishers resolved this issue.

### Coordinate Systems

A* operates on discrete grid cells, while ROS navigation uses positions in meters.

I therefore implemented conversions between world coordinates and occupancy-grid coordinates using the map origin and resolution.

### Planner and Controller Separation

One of the most important concepts I learned was the difference between planning and control.

The A* planner determines **where the robot should travel**.

The Pure Pursuit controller determines **how the robot should move to follow that path**.

Separating these responsibilities made the overall navigation architecture much easier to understand.

## What I Learned

This project helped me understand:

* ROS 2 nodes, topics, publishers, and subscribers
* Occupancy-grid maps
* Robot localization with AMCL
* LiDAR-based navigation
* ROS 2 QoS behavior
* World-to-grid coordinate conversion
* A* graph search
* Heuristic functions
* Path reconstruction
* Pure Pursuit path tracking
* Robot coordinate transformations
* Linear and angular velocity control
* Integration of planning and control algorithms in ROS 2

Most importantly, this project helped me move from using existing navigation systems to understanding and implementing the algorithms that operate underneath them.

## Project Files

`src/astar_planner.py` — Custom A* global planner

`src/pure_pursuit_controller.py` — Custom Pure Pursuit path-following controller

`screenshots/` — Simulation and navigation screenshots

`demo/README.md` — Demo video link

