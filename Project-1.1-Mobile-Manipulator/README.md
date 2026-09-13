# Project 1.1 – ROS 2 Mobile Manipulator

## Overview

This project was completed as preparation for Drexel University's Coordination and Planning for Multi-Robot Systems VIP team.

The objective of this project was to gain experience with ROS 2 mobile manipulation by working with a simulated robot in Gazebo, using Nav2 for mobile robot navigation and MoveIt 2 for robotic arm motion planning.

## Objectives

* Set up a mobile manipulator in simulation.
* Use Gazebo to simulate the robot and its environment.
* Use Nav2 to navigate the mobile base.
* Use MoveIt 2 to control and plan motions for the robotic arm.
* Perform a pick-and-place task.
* Develop familiarity with ROS 2, Linux, Python, and robotic simulation tools.

## Tools and Technologies

* Ubuntu 22.04
* ROS 2
* Gazebo
* RViz
* Nav2
* MoveIt 2
* Python
* Linux command line
* GitHub

## Implementation

The project combines mobile robot navigation and robotic manipulation in a simulated environment.

The mobile base is operated within Gazebo, while Nav2 provides the navigation framework for moving the robot through the environment.

MoveIt 2 is used for motion planning of the robotic arm. The manipulation portion of the project demonstrates the arm moving toward an object, grasping it, moving it to another location, and releasing it.

## Results

The simulation was successfully launched and the robotic arm was controlled using MoveIt 2.

A demonstration video was recorded showing the simulated system and manipulation task.

Additional screenshots and source-code files are included in this repository as supporting documentation.

## Problems and Debugging

During the project I encountered several problems that helped me become more comfortable troubleshooting ROS 2 and Linux environments.

Some of the issues included:

* Understanding the structure of ROS 2 packages and nodes.
* Becoming comfortable using Linux commands and working through the terminal.
* Understanding how simulation, visualization, navigation, and motion-planning tools interact.
  Another issue that if aced was that the robotic arm base had only a fixed orientation and could not move the arm in 360 degrees which made the pick and place objective really hard and the physics of the gazebo was also messign witht he pick and place task as the robot would not grip the object properly or if it came in contact wiht the object it would run backwards causing trouble and making me reset the world.

Additional project-specific Nav2 and MoveIt 2 issues will be documented as I review the completed implementation.

## What I Learned

This project helped me develop a basic understanding of how multiple robotics software components work together.

In particular, I gained experience with:

* ROS 2 nodes and packages.
* Using the Linux terminal for robotics development.
* Gazebo robot simulation.
* RViz visualization.
* Basic Nav2 concepts.
* MoveIt 2 motion planning.
* Organizing and documenting engineering projects.

This was my first larger ROS 2 robotics project, so one of the most important outcomes was becoming more comfortable navigating a ROS 2 development environment and troubleshooting problems when the system did not initially work as expected.

## Questions and Further Exploration

1. How are Nav2 and MoveIt 2 coordinated when multiple mobile manipulators operate within the same environment?

2. How does a mobile manipulator determine when it should reposition its mobile base instead of attempting to reach a target using only the robotic arm?

3. What additional challenges arise when transferring a navigation and manipulation system developed in Gazebo to a physical robot?

4. I know this is just the first project and hence we werent told to interact with the access to the python codes of gazebo or moveit 2 or rviz but i would like to see how the code works and I would also like to modify the physics of the environment to match real world applications as i would say right now it is slight wonky in some aspects.

## Demo

A demonstration video of the completed simulation will be linked here.

**Demo Video:** Coming soon

## Project Files

* `src/` – Relevant source code and configuration files.
* `screenshots/` – Screenshots of the simulation, navigation, manipulation, and code.
* `demo/` – Demonstration material and video information.

