from compas_cadwork.datamodel import Element

from . import get_all_element_ids
from . import get_dimensions


class ElementDelta:
    """Helper for detecting changes in the available element collection"""

    def __init__(self):
        self._known_element_ids = None
        self.reset()

    def check_for_changed_elements(self):
        """Returns a list of element ids added to the file database since the last call.

        Returns
        -------
        list(:class:`compas_cadwork.datamodel.Element`)
            List of new elements.
        """
        current_ids = set(get_all_element_ids())
        new_ids = current_ids - self._known_element_ids
        removed_ids = self._known_element_ids - current_ids
        self._known_element_ids = current_ids
        return [Element(id) for id in new_ids], [Element(id) for id in removed_ids]

    def reset(self):
        """Reset the known element ids"""
        self._known_element_ids = set(get_all_element_ids())


class DimensionsDelta:
    """Helper for detecting edits to the dimensions in the document

    TODO: check if and how this can be merged with ElementDelta, seems this could do both jobs, question is just the reset point.

    """

    def __init__(self):
        self._known_dimensions = None
        self.reset()

    def check_for_changed_dimensions(self):
        """Returns a list of dimensions that existed but were modified since the last call to :method:`reset`.

        Returns
        -------
        list(:class:`compas_cadwork.datamodel.Dimension`)
            List of modified dimensions.
        """
        # Changes will contain additions as well, since the objects are compared as a whole..
        # However, addtions need to be handled separately. Therefore, new ids are filtered out.
        current_dimensions = get_dimensions()
        changes = set(current_dimensions) - self._known_dimensions
        additions = set([m.id for m in current_dimensions]) - set([m.id for m in self._known_dimensions])
        return list(filter(lambda m: m.id not in additions, changes))

    def reset(self):
        """Reset the known dimensions. Any changed dimensions after this call will be considered modifications."""
        self._known_dimensions = set(get_dimensions())
