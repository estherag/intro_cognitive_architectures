from owlready2 import *

def load_ontology():

    onto = get_ontology("http://cognitive-nav.org/ontology.owl")

    with onto:
        # Core concepts
        class Room(Thing):
            pass

        class PhysicalObject(Thing):
            pass

        class contains(ObjectProperty):
            domain = [Room]
            range = [PhysicalObject]

        # Objects
        class Sofa(PhysicalObject):
            pass

        # TODO:
        # Define additional object classes that can be detected by YOLO.
        #
        # Examples:
        #   Bed
        #   TV
        #   Chair
        #   DiningTable
        #   Cup
        #   Fridge
        #   Oven
        #

        # Rooms

        class LivingRoom(Room):
            pass

        # TODO:
        # Define additional room types.
        #
        # Examples:
        #   Bedroom
        #   Kitchen
        #   DiningRoom
        #

        
        # Classification rules

        # TODO:
        # Add OWL equivalence rules that allow the reasoner
        # to infer the room type from the observed objects.
        #
        # Example:
        #
        # LivingRoom.equivalent_to.append(
        #     Room
        #     & contains.some(Sofa)
        # )

        # Example rule:
        #
        # Bedroom.equivalent_to.append(
        #     Room
        #     & contains.some(Bed)
        # )

        # Try to make your rules specific enough to avoid
        # confusing one room with another.

    return onto
