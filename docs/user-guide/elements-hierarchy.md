# Elements Hierarchy

In COMPAS cadwork, project elements can belong to different types, such as beams, panels, and walls.
These elements are organized in a hierarchy, and each type exposes its own set of properties and methods.

This means that, while all elements share common behavior, some operations and attributes are specific to a particular element type.
Understanding this hierarchy will help you understand which functionality is available for each kind of element.

The following class diagram summarizes the element classes provided by the library:

```mermaid
classDiagram
    class Element {
        + MutableMapping[UserAttributeId, str] attribute_keys$
        + ElementType type
        + ElementId id
        + UUID guid
        + IfcUUID ifc_guid
        + IfcElementType ifc_element_type
        + IfcPredefinedType ifc_predefined_type
        + str name
        + MutableMapping[UserAttributeId, str] attributes
        + MutableSet[Element] children
        + delete() None
    }

    Element <|-- Node
    class Node {
        + Point position
        + NodeSymbol symbol
    }

    Element <|-- OrientedElement
    class OrientedElement {
        + Frame frame
        + translate(Vector vector) None
        + duplicate(Vector vector) Self
    }

    OrientedElement <|-- Line
    class Line {
        + Point start
        + Point end
        + float length
    }

    OrientedElement <|-- DimensionalElement
    class DimensionalElement {
        + float length
        + float width
        + float height
        + Material material
    }

    DimensionalElement <|-- Beam

    DimensionalElement <|-- Panel

    Panel <|-- Opening

    Panel <|-- Floor
    class Floor {
        + FloorLayerStack layers «LayeredMixin»
    }

    Panel <|-- Roof
    class Roof {
        + RoofLayerStack layers «LayeredMixin»
    }

    Panel <|-- Wall
    class Wall {
        + WallLayerStack layers «LayeredMixin»
    }
```
