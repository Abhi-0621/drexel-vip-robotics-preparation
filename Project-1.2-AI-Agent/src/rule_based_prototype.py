pick_attempts = 0


def detect_object(object_name):
    print("Searching for:", object_name)

    if object_name == "red cube":
        return "location_A"
    else:
        return None


def navigate_to(location):
    print("Navigating to:", location)

    if location == "location_A":
        return True
    else:
        return False


def pick_object(object_name):
    global pick_attempts

    pick_attempts += 1
    print("Attempting to pick:", object_name)

    if pick_attempts == 1:
        print("Pick failed: object is out of reach.")
        return False

    return True


def robot_agent(task):
    print("\nAgent received task:", task)

    if task == "pick up the red cube":
        location = detect_object("red cube")

        if location is None:
            print("Agent: I could not find the red cube.")
            return False

        navigation_success = navigate_to(location)

        if navigation_success == False:
            print("Agent: Navigation failed.")
            return False

        pick_success = pick_object("red cube")

        if pick_success == False:
            print("Agent: Pick failed. Repositioning closer to the object.")

            navigation_success = navigate_to("location_A")

            if navigation_success == False:
                print("Agent: Repositioning failed.")
                return False

            pick_success = pick_object("red cube")

            if pick_success == False:
                print("Agent: Second pick attempt failed.")
                return False

        print("Agent: Task completed successfully!")
        return True

    else:
        print("Agent: I do not understand this task.")
        return False


robot_agent("pick up the red cube")
        
       
