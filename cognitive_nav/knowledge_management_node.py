import rclpy
from rclpy.node import Node

from owlready2 import sync_reasoner, default_world


def main():
    rclpy.init()

    node = CognitiveNode()

    # Keep the node running and listening for detections
    rclpy.spin(node)

    # Clean up and shut down
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()