from __future__ import annotations
import abc
import time
import threading
from typing import List
from typing import Union

import element_controller as ec

from compas_cadwork.datamodel import Element


class Publisher:
    """Base class for event publishers."""
    def publish(self, *args, **kwargs):
        """Publishes new elements to all subscribers."""
        for subscriber in self._subscribers:
            if callable(subscriber):
                subscriber(*args, **kwargs)
            elif isinstance(subscriber, Subscriber):
                subscriber.update(*args, **kwargs)

    def subscribe(self, subscriber: Union[Subscriber, callable]):
        """Subscribes a subscriber to the publisher.

        Parameters
        ----------
        subscriber : :class:`Subscriber` or callable
            The subscriber to subscribe. A function can also be subscribed a-la callback.

        """
        self._subscribers.append(subscriber)

    def unsubscribe(self, subscriber: Union[Subscriber, callable]):
        """Unsubscribes a subscriber from the publisher.

        Parameters
        ----------
        subscriber : :class:`Subscriber` or callable
            The subscriber to unsubscribe.

        """
        self._subscribers.remove(subscriber)


class Subscriber(abc.ABC):
    """Optional interface for subscribers to implement."""
    @abc.abstractmethod
    def update(self, *args, **kwargs):
        """Update method to be called when a new event is published."""
        raise NotImplementedError


class ElementDelta:
    """Helps to detect new elements in the cadwork viewport."""
    def __init__(self):
        self._known_element_ids = set(ec.get_visible_identifiable_element_ids())

    def check_for_new_elements(self):
        """Returns a list of element ids added to the file database since the last call.

        Returns
        -------
        list(:class:`compas_cadwork.datamodel.Element`)
            List of new elements.
        """
        current_ids = set(ec.get_visible_identifiable_element_ids())
        new_ids = current_ids - self._known_element_ids
        if new_ids:
            self._known_element_ids = current_ids
            return [Element.from_id(id) for id in new_ids]
        return []


class NewElementEventPublisher(threading.Thread, Publisher):
    """Publishes new elements in the cadwork viewport.

    Attributes
    ----------
    INTERVAL_SEC : int
        Interval in seconds to check for new elements.

    Examples
    --------
    >>> publisher = NewElementEventPublisher()
    >>> publisher.subscribe(lambda new_elements: print(new_elements))
    >>> publisher.start()

    """
    INTERVAL_SEC = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._subscribers = []
        self._is_running = False
        self.deltalizer = ElementDelta()

    def run(self):
        self._is_running = True
        last_poll = 0
        while self._is_running:
            curr_poll = time.time()
            if curr_poll - last_poll < self.INTERVAL_SEC:
                continue
            new_ids = self.deltalizer.check_for_new_elements()
            if new_ids:
                self.publish([Element.from_id(id) for id in new_ids])

    def stop(self):
        """Stops the event publisher thread."""
        self._is_running = False

