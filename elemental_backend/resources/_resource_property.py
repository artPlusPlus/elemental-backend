import weakref
from functools import partial


class ResourceProperty(object):
    """
    Observable property intended for use by `Resource` classes.
    """
    def __init__(self, fget=None, fset=None, fdel=None, fpost=None):
        self._fget = fget
        self._fset = fset
        self._fdel = fdel
        self._fpost = fpost
        self._subscribers = weakref.WeakKeyDictionary()

    def __get__(self, instance, owner):
        if instance is None:
            return self
        if self._fget is None:
            raise AttributeError()
        return self._fget(instance)

    def __set__(self, instance, value):
        if self._fset is None:
            raise AttributeError()

        original_value = self._fget(instance)
        self._fset(instance, value)
        current_value = self._fget(instance)

        if original_value != current_value:
            self._on_changed(instance, original_value, current_value)

    def getter(self, fget):
        return type(self)(fget, self._fset, self._fdel, self._fpost)

    def setter(self, fset):
        return type(self)(self._fget, fset, self._fdel, self._fpost)

    def deleter(self, fdel):
        return type(self)(self._fget, self._fset, fdel, self._fpost)

    def subscribe(self, instance, callback):
        subscribers = self._subscribers.setdefault(instance, set())  # set instead of WeakSet to support WeakMethod
        callback_died_handler = partial(self._callback_died,
                                        weakref.ref(instance))
        try:
            callback = weakref.WeakMethod(callback, callback_died_handler)
        except TypeError:
            callback = weakref.ref(callback, callback_died_handler)

        subscribers.add(callback)

    def unsubscribe(self, instance, callback):
        try:
            subscribers = self._subscribers[instance]
        except KeyError:
            return

        try:
            callback = weakref.WeakMethod(callback)
        except TypeError:
            callback = weakref.ref(callback)

        subscribers.remove(callback)
        if not len(subscribers):
            del self._subscribers[instance]

    def _on_changed(self, instance, original_value, current_value):
        try:
            subscribers = self._subscribers[instance]
        except KeyError:
            return

        subscribers = [s() for s in subscribers]
        subscribers = [s for s in subscribers if s]
        for sub in subscribers:
            sub(instance, original_value, current_value)

    def __iadd__(self, instance_callback):
        instance, callback = instance_callback
        self.subscribe(instance, callback)
        return self

    def __isub__(self, instance_callback):
        instance, callback = instance_callback
        self.unsubscribe(instance, callback)
        return self

    def _callback_died(self, instance_ref, callback_ref):
        instance = instance_ref()
        if instance is None:
            return
        try:
            self._subscribers[instance].discard(callback_ref)
        except KeyError:
            pass
