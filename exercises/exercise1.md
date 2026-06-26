# Exercise 1: Symbolic Reasoning: Inferring the Current Room

In this exercise, you will build a simple symbolic reasoning system that allows a robot to infer the type of room it is currently observing. The robot receives object detections from a YOLO-based perception system and inserts them into an OWL ontology. An OWL reasoner then uses the semantic relationships defined in the ontology to classify the current room.

The objective is to demonstrate one of the key ideas behind symbolic cognitive architectures:

> Knowledge is represented explicitly and separately from the control code.


The robot does **not** know which room it is in. Instead, it must infer the room type from the objects it observes. For example:

```text
Observed objects:
    Sofa
    TV
    Chair

Inference:
    LivingRoom
```


## Provided Components

The following components are already implemented:

### Perception

A YOLO node publishes object detections on:

```text
/yolo/detections
```

Each detection contains:

* Object label
* Unique detection ID
* Estimated 3D position

### Cognitive Node

The cognitive node:

1. Receives object detections.
2. Maps YOLO labels to ontology concepts.
3. Creates ontology instances.
4. Runs an OWL reasoner.
5. Reports the inferred room type.


### Ontology

The ontology contains the basic structure required for reasoning but is intentionally incomplete. Modify `ontology.py` to extend it with the knowledge necessary to classify rooms.

#### 1. Define Room Concepts

Create ontology classes representing different room categories.

Examples include:

* LivingRoom
* Bedroom
* Kitchen
* DiningRoom

These classes should inherit from the common concept:

```text
Room
```

#### 2. Define Object Concepts

Create ontology classes representing the objects that may appear in the environment.

Examples include:

* Sofa
* TV
* Bed
* Chair
* DiningTable
* Cup

These classes should inherit from:

```text
PhysicalObject
```

#### 3. Define Semantic Relationships

Create a relationship describing that a room contains objects. This relationship will allow the reasoner to associate observations with room categories.

#### 4. Define Classification Rules

Define logical rules that characterize each room.

Examples:

```text
A LivingRoom contains a Sofa and a TV.

A Bedroom contains a Bed.

A DiningRoom contains a DiningTable and a Chair.
```

The goal is to make the rules sufficiently discriminative to distinguish between different room types. Think carefully about which objects provide strong evidence for a particular room.


## Running the exercise

Let's test the cognitive system in simulation. Start the house environment as described in the README.

Open a new terminal and launch the symbolic reasoning node:

```bash
source venv_cogarchs/bin/activate
ros2 run cognitive_nav symbolic_node
```

The node will subscribe to object detections, populate the ontology, execute the reasoner, and report the inferred room type.


### Observe the Cognitive Reasoning Output

Monitor the logs produced by the cognitive node. For each set of detected objects, the reasoner will attempt to classify the current room according to the ontology rules you defined.

Example:

```text
Added 'sofa_12'
Added 'tv_15'
Inferred classes: ['Room', 'LivingRoom']
I am in the living room...
```

## Analysis

As you move through the house, consider the following questions to improve your ontology:

1. Which room categories is the robot able to identify correctly?
2. Which object detections are most informative for room classification?
3. Are there situations where the robot cannot determine the room type?
4. Are there situations where multiple room categories are inferred simultaneously?
5. What happens after the robot visits several rooms without restarting the node?

> Discuss whether the robot is reasoning about what it currently sees or everything it has ever seen and how this affects its conclusions.