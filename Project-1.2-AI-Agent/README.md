# Project 1.2 – AI Robot Agent with Tool Calling

## Overview

This project was completed as preparation for Drexel University's **Coordination and Planning for Multi-Robot Systems** VIP team.

The goal of the project was to build a small AI agent capable of controlling a simulated robot through tool calling.

Instead of hard-coding the entire action sequence, I provided a local large language model with a set of robot tools and allowed the model to decide which tool to call based on the task and the results of previous actions.

The final system runs completely locally using **Ollama** and the **Qwen3 4B Instruct** model.

## Objective

The agent was given the task:

> Pick up the red cube.

To complete this task, the agent had access to three tools:

* `detect_object(object_name)`
* `navigate_to(location)`
* `pick_object(object_name)`

The agent had to determine the correct order in which to call these tools and react appropriately if one of the tools failed.

## Tools and Technologies

* Python 3
* Ollama
* Qwen3 4B Instruct
* Ubuntu Linux
* Local LLM inference
* Function / tool calling
* Git and GitHub

## Robot Tools

### detect_object()

This tool represents an object-detection system.

It accepts the name of an object and returns its location.

For this project, detecting the red cube returns:

```text
location_A
```

The function is a mock implementation intended to simulate the output of a real perception system.

### navigate_to()

This tool represents robot navigation.

It accepts a target location and returns whether navigation was successful.

In a real robotic system, this tool could eventually be connected to a navigation framework such as Nav2.

### pick_object()

This tool represents the robot manipulator attempting to pick up an object.

For demonstration purposes, the first pick attempt intentionally fails because the object is considered out of reach.

The second attempt succeeds after the agent decides to reposition the robot.

## Agent Prompt and Context

The model was given a system prompt explaining that it was a robot task-planning agent with access to the available robot tools.

The prompt included several rules:

1. Detect an object before attempting to pick it.
2. Navigate to the detected object location before attempting manipulation.
3. If a pick fails because the object is out of reach, reposition and retry.
4. Use the provided tools rather than assuming that an action succeeded.
5. Stop once the requested task has successfully been completed.

The user then gave the agent the high-level instruction:

```text
Pick up the red cube.
```

The model was not directly given a fixed sequence of function calls. Instead, it received the available tools and selected which function to call based on the task and the result returned by each tool.

## Successful Tool-Calling Sequence

During the successful run, the agent selected the following sequence:

```text
detect_object("red cube")
        ↓
location_A

navigate_to("location_A")
        ↓
navigation_success

pick_object("red cube")
        ↓
pick_failed_object_out_of_reach

navigate_to("location_A")
        ↓
navigation_success

pick_object("red cube")
        ↓
pick_success
```

The final agent response confirmed that the red cube had successfully been picked up.

## Failure Handling

Failure handling was an important part of this project.

The first failure occured when i had to use the openAi platform for the model calling and object picking but it would cost me 5 dollars and in order to solve this problem i found afree alternative which was to use ollama ai which after installation immediately detected my gpu and ran the llm's.

The first call to `pick_object()` intentionally returned:

```text
pick_failed_object_out_of_reach
```

Instead of immediately terminating the task, the language model interpreted this result and chose to call:

```text
navigate_to("location_A")
```

again.

After repositioning, the model attempted `pick_object()` a second time.

The second attempt returned:

```text
pick_success
```


This demonstrated that the agent could use tool results as context and modify its next action instead of following a completely fixed sequence.

## Rule-Based Prototype

Before creating the model-driven agent, I first created a rule-based Python prototype.

In the rule-based version, the sequence:

```text
detect → navigate → pick → retry
```

was explicitly written using Python `if` statements.

This helped me understand the task logic and verify that each individual function worked correctly before introducing the LLM.

The final version replaced this hard-coded sequencing with model-driven tool selection.

The rule-based prototype is included in:

```text
src/rule_based_prototype.py
```

## Final AI Agent

The final tool-calling implementation is located in:

```text
src/robot_agent.py
```

The agent uses the Ollama Python interface to provide the three Python functions as tools to the Qwen model.

The model examines the task and previous tool results before deciding which function to call next.

## Results

The final agent successfully:

* Detected the requested object.
* Selected the correct navigation tool.
* Navigated to the object's location.
* Attempted to pick the object.
* Recognized that the first pick failed.
* Repositioned the robot.
* Retried the pick operation.
* Successfully completed the task.

## What I Learned

This project helped me understand the difference between a traditional rule-based controller and an AI agent using tool calling.

In the rule-based version, the programmer determines the entire sequence of actions ahead of time.

In the tool-calling version, the programmer defines the available capabilities and provides context and instructions, while the language model selects the actions based on the current state and tool results.

I also gained experience with:

* Python functions.
* Function arguments and return values.
* Local large language models.
* Ollama.
* Tool calling.
* Prompt design.
* Maintaining conversational context between model calls.
* Failure handling.
* Separating robot capabilities from higher-level decision making.

## Further Exploration

Some questions I would like to explore further include:

1. How could these mock tools be connected to real ROS 2 actions and services?

2. How could `detect_object()` use an actual camera or perception model instead of returning a predefined location?

3. How could `navigate_to()` communicate directly with Nav2?

4. How could an agent safely recover from more complicated failures such as blocked navigation paths, failed grasp attempts, or unavailable objects?

5. How would this architecture scale when one agent has to coordinate several robots rather than controlling a single robot?

## Project Files

* `src/robot_agent.py` – Final local LLM tool-calling agent.
* `src/rule_based_prototype.py` – Earlier rule-based implementation.
* `screenshots/` – Evidence showing the successful tool-calling sequence and failure recovery.

