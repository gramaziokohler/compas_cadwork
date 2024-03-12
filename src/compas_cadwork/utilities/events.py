from compas_cadwork.datamodel import Element

from . import get_all_element_ids


class ElementDelta:
    """Helper for detecting changes in the available element collection"""

    def __init__(self):
        self._known_element_ids = set(get_all_element_ids())

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
        return [Element.from_id(id) for id in new_ids], [Element.from_id(id) for id in removed_ids]
