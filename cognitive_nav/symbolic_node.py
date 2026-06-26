import rclpy
from rclpy.node import Node

from owlready2 import sync_reasoner, default_world
from cognitive_nav.ontology import load_ontology
from yolo_msgs.msg import DetectionArray


# Maximum distance (in meters) for a detection to be added to the ontology
MAX_DETECTION_DISTANCE = 3.0

# Mapping from YOLO class names to ontology class names
LABEL_TO_ONTOLOGY = {
    "sofa":         "Sofa",
    "bed":          "Bed",
    "chair":        "Chair",
    "dining table": "DiningTable",
    "tv":           "TV",
    "cup":          "Cup",
    "refrigerator": "Fridge",
    "oven":         "Oven",
}


class SymbolicNode(Node):

    def __init__(self):
        super().__init__('Symbolic_node')

        # Load the ontology and initialize the room instance
        self.onto = load_ontology()
        self.Room = self.onto.Room
        self.room = self.Room("unknown_room_1")

        # Subscribe to 3D detections from YOLO
        self.subscription = self.create_subscription(
            DetectionArray,
            '/yolo/detections',
            self.detections_callback,
            10
        )

        self.get_logger().info("Symbolic node initialized")

    def detections_callback(self, msg: DetectionArray):
        """
        Callback for incoming YOLO 3D detections.
        Adds all valid detections to the ontology, then runs the symbolic cycle once.

        Args:
            msg (DetectionArray): The message containing a list of detections.
        """
        any_valid = False
        for detection in msg.detections:
            distance = detection.bbox3d.center.position.z

            # Only process detections within the maximum distance threshold
            if distance > MAX_DETECTION_DISTANCE:
                self.get_logger().debug(
                    f"Skipping '{detection.class_name}' at {distance:.2f} m (too far)"
                )
                continue

            if self.add_perception(detection.class_name, detection.id):
                any_valid = True

        # Only reason and act if at least one new instance was added to the ontology
        if any_valid:
            self.symbolic_cycle()

    def add_perception(self, label, detection_id):
        """
        Add a perceived object to the ontology based on the given label and detection ID.

        Args:
            label (str): The YOLO class name of the perceived object.
            detection_id (str): Unique ID assigned by YOLO to this detection.
        """
        ontology_class_name = LABEL_TO_ONTOLOGY.get(label)

        if ontology_class_name is None:
            self.get_logger().warn(f"Unknown object: '{label}'")
            return

        with self.onto:
            # Create a uniquely named instance using the YOLO detection ID
            ontology_class = getattr(self.onto, ontology_class_name)

            instance_name = f"{ontology_class_name.lower()}_{detection_id}"

            # Skip if an instance with this name already exists in the ontology
            existing = self.onto.search_one(iri=f"*{instance_name}")
            if existing is not None:
                self.get_logger().debug(f"'{instance_name}' already in ontology, skipping")
                return False

            obj = ontology_class(instance_name)

            # Add to the room, log and signal that the ontology changed
            self.room.contains.append(obj)
            self.get_logger().info(f"Added '{instance_name}'")
            return True

        return False

    def reason(self):
        """
        Perform reasoning on the ontology to infer new knowledge.
        Must be called within the ontology context so the reasoner
        can access all declared axioms.
        """
        with self.onto:
            sync_reasoner(self.onto, debug=0)

    def get_room_type(self):
        """
        Query the inferred types of the current room using owlready2's is_a property.
        Returns all classes (direct and inferred) the room instance belongs to.

        Returns:
            list: A list of inferred classes for the room.
        """
        return list(self.room.is_a)

    def log_ontology_instances(self):
        """
        Log all object instances currently stored in the room's ontology.
        Useful for debugging after reasoning.
        """
        instances = [o.name for o in self.room.contains]
        self.get_logger().info(f"Ontology instances: {instances}")

    def symbolic_cycle(self):
        """
        Execute the symbolic cycle: reasoning, query, and action.
        All perceptions must be added before calling this method.
        """
        # Perform reasoning over all accumulated perceptions
        self.reason()

        # Log all instances currently stored in the ontology after reasoning
        # self.log_ontology_instances()

        # Query the inferred room type
        classes = self.get_room_type()

        self.get_logger().info(f"Inferred classes: {[c.name for c in classes if hasattr(c, 'name')]}")

        # Take action based on the inferred room type
        if self.onto.LivingRoom in classes:
            self.get_logger().info("I am in the living room, switching on tv...")
        if self.onto.Kitchen in classes:
            self.get_logger().info("I am in the kitchen, starting to cook...")

def main():
    rclpy.init()

    node = SymbolicNode()

    # Keep the node running and listening for detections
    rclpy.spin(node)

    # Clean up and shut down
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()