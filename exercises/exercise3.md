# Exercise 3: Goal-Oriented Behaviour

In Exercises 1 and 2, the robot built a belief about its current location from object detections. It could answer the question:

> Where am I, and how confident am I?

In this exercise, the robot is given a purpose. It receives a sequence of symbolic goals:

> Go to the Kitchen. Then go to the Bedroom.

The robot must use its beliefs to determine whether it has reached its current goal. If the goal has not yet been achieved, it should continue exploring. Once it is sufficiently confident that it has reached its destination, it should report success, remember the location of the room, and move on to the next goal.

## Goal manager

Complete `goal_manager_node.py` to manage the current objective, monitor whether it has been achieved, store the location of discovered rooms, and advance to the next goal once the current one has been completed.

### 1. Define a Goal Sequence

Define a list of symbolic goals the robot must achieve in order. The robot will pursue one goal at a time, moving to the next goal after the current one is satisfied.

### 2. Define a Satisfaction Condition and Monitor

A goal is satisfied when the belief for the target room exceeds a confidence threshold. Use the same belief values produced by the knowledge management node from Exercise 2.

> The threshold here plays a different role than in Exercise 2. In Exercise 2 it controlled when the robot reported its location. Here it controls when the robot acknowledges to having reached a destination. Think about whether the same value is appropriate for both purposes.

At every cognitive cycle:

* Check whether the current goal has been achieved.
* If not, continue pursuing the current goal.
* If the goal has been achieved, report success and activate the next goal.
* When all goals have been completed, report that the mission is finished.

### 3. Report Cognitive State

At each cycle, the robot should report:

* Its current goal
* Its current best belief about its location
* Whether the goal has been satisfied

Example:

```text
Goal:    Kitchen
Beliefs: Kitchen = 1.62 | LivingRoom = 0.31 | Bedroom = 0.00
Status:  Pursuing goal...
```

```text
Goal:    Kitchen
Beliefs: Kitchen = 1.89 | LivingRoom = 0.18 | Bedroom = 0.00
Status:  Goal reached. Next goal: Bedroom.
```

### 3.1 Extend semantic mememory

When the robot reaches a room with sufficient confidence, store the room together with the robot's current position.

This creates a simple semantic memory that associates symbolic concepts ("Kitchen") with locations in the environment.

## Running the Exercise

Start the house environment as described in the README.

Launch all three nodes:

```bash
# Terminal 1
source venv_cogarchs/bin/activate
ros2 run cognitive_nav symbolic_node

# Terminal 2
source venv_cogarchs/bin/activate
ros2 run cognitive_nav knowledge_management_node

# Terminal 3
source venv_cogarchs/bin/activate
ros2 run cognitive_nav goal_manager_node
```

Navigate the robot manually through the house in the order defined by your goal sequence. Observe when each goal is triggered and how the belief state evolves during transitions.

## Evaluation

Once the basic sequence works, test the following situations:

* Navigate to a room that is not the current goal. Does the robot correctly continue pursuing the current objective?
* Ambiguous transition. Move slowly between two rooms so that beliefs are split between both hypotheses. Does the robot wait until sufficient evidence has been accumulated?
* Revisiting a room. Define a goal sequence such as: `
["Kitchen", "Bedroom", "Kitchen"]` Does the robot correctly recognise the second visit as the completion of a new goal?

## Discussion

After completing the exercise, consider the following questions:

1. The robot reaches a goal based on belief, not on ground truth. Can it ever be wrong? What are the consequences?
2. The goal sequence is fixed in advance. What would need to change for the robot to decide its own goals?
