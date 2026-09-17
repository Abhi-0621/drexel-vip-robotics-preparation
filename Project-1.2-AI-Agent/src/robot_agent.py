from ollama import chat

pick_attempts = 0


def detect_object(object_name: str) -> str:
    """
    Detect an object and return its location.

    Args:
        object_name: Name of the object to detect.

    Returns:
        The detected location of the object.
    """
    print(f"\nTOOL: detect_object('{object_name}')")

    if object_name.lower() == "red cube":
        return "location_A"

    return "object_not_found"


def navigate_to(location: str) -> str:
    """
    Navigate the robot to a location.

    Args:
        location: Location the robot should navigate to.

    Returns:
        Navigation result.
    """
    print(f"\nTOOL: navigate_to('{location}')")

    if location == "location_A":
        return "navigation_success"

    return "navigation_failed"


def pick_object(object_name: str) -> str:
    """
    Attempt to pick up an object.

    Args:
        object_name: Name of the object to pick up.

    Returns:
        Result of the pick attempt.
    """
    global pick_attempts

    pick_attempts += 1
    print(f"\nTOOL: pick_object('{object_name}')")

    if object_name.lower() != "red cube":
        return "pick_failed_object_unknown"

    if pick_attempts == 1:
        return "pick_failed_object_out_of_reach"

    return "pick_success"


available_tools = {
    "detect_object": detect_object,
    "navigate_to": navigate_to,
    "pick_object": pick_object,
}


messages = [
    {
        "role": "system",
        "content": """
You are a robot task-planning agent.

You control a robot using the available tools.

Rules:
1. Before picking an object, detect it first.
2. Navigate to the object's detected location before attempting to pick it.
3. If a pick fails because the object is out of reach, navigate to the object's location again and retry the pick.
4. Use tools rather than pretending an action succeeded.
5. Stop once the requested task is successfully completed.
""",
    },
    {
        "role": "user",
        "content": "Pick up the red cube.",
    },
]


while True:
    response = chat(
        model="qwen3:4b-instruct",
        messages=messages,
        tools=[
            detect_object,
            navigate_to,
            pick_object,
        ],
    )

    messages.append(response.message)

    if not response.message.tool_calls:
        print("\nAGENT:", response.message.content)
        break

    for tool_call in response.message.tool_calls:
        tool_name = tool_call.function.name
        tool_args = tool_call.function.arguments

        print("\nAGENT chose tool:", tool_name)
        print("Arguments:", tool_args)

        tool_function = available_tools.get(tool_name)

        if tool_function is None:
            tool_result = "tool_not_found"
        else:
            tool_result = tool_function(**tool_args)

        print("Tool result:", tool_result)

        messages.append(
            {
                "role": "tool",
                "tool_name": tool_name,
                "content": str(tool_result),
            }
        )
       
