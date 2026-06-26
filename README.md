# Cognitive architectures introduction

In session, we will build a simple cognitive system for a robot operating inside a house. The robot perceives objects using YOLO and acts based on its understanding of the room it is currently observing. The cognitive pipeline is organized as follows:

* **Perception:** YOLO detects objects in the environment.
* **Representation:** Detected objects are inserted into an OWL ontology.
* **Reasoning:** An OWL reasoner infers the type of room from the observed objects.
* **Action:** The robot executes a simple room-dependent action.

## Install

Get all the dependancies executing the `install.sh` script.

```bash
chmod +x install.sh
./install.sh
```

## Exercises

TODO<link to exercises>

Some proposed solutions are available in <here>

## Setup

## Test setup

Start the simulated house environment:

```bash
source venv_cogarchs/bin/activate
ros2 launch cognitive_nav mirte_house.launch.py
```

This will launch the robot and the simulated environment containing different rooms and objects.

Use keyboard teleoperation to explore the environment:

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

Navigate through different rooms and observe how the inferred room type changes as different objects become visible.

To inspect the raw detections produced by the perception system:

```bash
ros2 topic echo /yolo/detections
```

You may also visualize the annotated camera image:

```bash
ros2 run rqt_image_view rqt_image_view /yolo/dbg_image
```

Compare the detected objects with the room classification reported by the cognitive node.

## Troubleshooting: Arm in the camera field of view

If the arm hasn't move up during the lauch process, you can easily move it up with:

## Troubleshooting: Arm Occluding the Camera

If the arm does not move out of the camera field of view during launch, YOLO detections may be degraded because the robot sees its own arm instead of the environment. You can manually move the arm to a neutral position using:

```bash
ros2 topic pub --once \
/mirte_master_arm_controller/joint_trajectory \
trajectory_msgs/msg/JointTrajectory "
joint_names:
- shoulder_pan_joint
- shoulder_lift_joint
- elbow_joint
- wrist_joint

points:
- positions: [0.0, 0.0, 0.0, 0.0]
  time_from_start:
    sec: 2
"
```

## Troubleshooting: YOLO Stuck During Startup

If the launch process stops after:

```text
[yolo_node] Activating...
```

and no detections are published, the YOLO model file may be corrupted.

Activate the Python environment and try loading the model manually:

```bash
source venv_cogarchs/bin/activate

python - <<EOF
from ultralytics import YOLO
YOLO("yolov8m.pt")
print("MODEL OK")
EOF
```

If the model is installed correctly, the command should finish with:

```text
MODEL OK
```

If not found, ultralytics will automatically download a copy of the model.
