# Exercise 2: Symbolic Reasoning Under Uncertainty

In Exercise 1, the robot used an OWL ontology and a symbolic reasoner to infer room categories from the objects it observed. This approach assumes that observations are correct and that the robot can reason directly from the symbolic knowledge stored in the ontology.

However, in uncertain environments:

* Object detectors are not perfect
* Some objects may be partially visible
* Important objects may not be detected
* Observations from the past may no longer be relevant

In this exercise, we will extend the symbolic reasoning system with two cognitive capabilities:

1. **Belief management**, allowing the robot to represent confidence in its conclusions
2. **Memory decay**, allowing the robot to gradually forget outdated observations

## Knowledge management

Complete `knowledge_management_node.py`. First let's create a belief state storing confidence values for each room type.

Example:

```python
room_beliefs = {
    "LivingRoom": 0.0,
    "Bedroom": 0.0,
    "Kitchen": 0.0,
    "DiningRoom": 0.0,
}
```

These values will evolve over time as the robot gathers new observations. Use YOLO confidence


### 1. Use YOLO Confidence Scores

In Exercise 1, every detected object contributed equally to the ontology. In reality, detections have different confidence values. The robot should use these confidence values as evidence supporting room hypotheses.

For example:

```text
Detected:
    Sofa (0.95)

Evidence:
    LivingRoom += 0.95
```

Higher-confidence detections should contribute more strongly than uncertain detections.

### 2. Combine Symbolic Inference and Beliefs

The ontology still performs symbolic reasoning, for example, after observing a sofa and a TV the OWL reasoner may infer it is in the living room.

The belief layer should then increase confidence in the inferred room category.

Example:

```text
Inferred:
    LivingRoom

Belief:
    LivingRoom += 1.75
```

where the value depends on the confidence of the contributing detections.

There is a separation between the two layers as the symbolic reasoner answers:

> Which room categories are possible?

while the belief layer answers:

> Which room category is most likely?

Note on normalisation: Belief values are not probabilities and do not need to sum to 1. What matters is the relative ranking between room hypotheses. However, if values grow without bound over time, thresholds become meaningless. This is addressed in the next section via memory decay.

### 3. Forget Old Evidence

Currently, room beliefs will continuously accumulate evidence.This causes a problem. Imagine the robot first observes a sofa and a TV and later moves to a kitchen. Without forgetting, the robot may continue believing it is in a living room long after leaving it.

Let's implement a memory decay mechanism so at every cognitive cycle, the influence of old observations is gradually reduced. For example:

Initially:

```text
LivingRoom = 1.80
```

After several cycles without observing living room objects:

```text
LivingRoom = 1.44
LivingRoom = 1.15
LivingRoom = 0.92
LivingRoom = 0.74
...
```

The decay factor controls how quickly the robot forgets. There is a fundamental tradeoff:

| Decay factor | Behaviour |
|---|---|
| Close to 1.0 (e.g. 0.98) | Slow forgetting; stable in a single room, slow to adapt after moving |
| Moderate (e.g. 0.80) | Forgets old evidence within ~10 cycles; reasonable for a moving robot |
| Close to 0.0 (e.g. 0.30) | Rapid forgetting; almost no memory, reacts to current observations only |

**Experiment:** run the simulation with `λ = 0.95` and then with `λ = 0.50`. Observe how quickly the robot adapts after moving between rooms. Note your observations.

### 4. Decision Making

Determine the room with the highest belief value. The room in which the robot is should be reported only if the confidence is high enough. The robot should avoid making strong conclusions when evidence is insufficient.

## Running the Exercise

Let's test the cognitive system in simulation. Start the house environment as described in the README.

Open a new terminal and launch the symbolic reasoning node:

```bash
source venv_cogarchs/bin/activate
ros2 run cognitive_nav symbolic_node
```

The node will subscribe to object detections, populate the ontology, execute the reasoner, and report the inferred room type.

```bash
source venv_cogarchs/bin/activate
ros2 run cognitive_nav knowledge_management_node
```

Observe how symbolic classifications and room beliefs evolve over time.

Example:

```text
Added 'sofa_1'
Added 'tv_2'

Inferred classes:
    Room
    LivingRoom

Beliefs:
    LivingRoom = 1.72
    Kitchen = 0.00
    Bedroom = 0.00

I am in a LivingRoom.
```

Later:

```text
Beliefs:
    LivingRoom = 0.74
    Kitchen = 0.62

I am not sure where I am.
```

## Discussion

After completing the exercise, consider the following questions:

1. Why are confidence values useful even when an ontology is available?
2. What happens if the robot never forgets?
3. What happens if memory decay is too strong?
4. How can beliefs help resolve ambiguity?
