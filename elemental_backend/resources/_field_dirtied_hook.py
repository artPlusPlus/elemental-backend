import weakref
from functools import partial
from collections import namedtuple

from elemental_core import Hook


FieldDirtiedData = namedtuple(
    'FieldDirtiedEventArgs',
    [
        'value_key',
        'session_key'
    ]
)


class FieldDirtiedHook(Hook):
    def __init__(self):
        super(FieldDirtiedHook, self).__init__()

        self._handler_refs = {}

    def add_handler(self, handler, value_key=None, session_key=None):
        handler_ref_died = partial(self._handler_ref_died, value_key, session_key)

        try:
            handler_ref = weakref.WeakMethod(handler, handler_ref_died)
        except TypeError:
            handler_ref = weakref.ref(handler, self._handler_ref_died)

        handler_refs = self._handler_refs.setdefault(session_key, {})
        handler_refs = handler_refs.setdefault(value_key, [])
        handler_refs.append(handler_ref)

    def remove_handler(self, handler, value_key=None, session_key=None):
        try:
            handler_refs = self._handler_refs[session_key][value_key]
            handler_refs.remove(handler)
        except (KeyError, IndexError):
            pass

    def _handler_ref_died(self, value_key, session_key, handler_ref):
        try:
            self._handler_refs[value_key][session_key].remove(handler_ref)
        except (KeyError, ValueError):
            pass

    def __call__(self, sender, value_key, session_key):
        try:
            sender = weakref.proxy(sender)
        except TypeError:
            pass

        try:
            handler_refs = self._handler_refs[value_key][session_key]
        except KeyError:
            return

        data = FieldDirtiedData(value_key=value_key, session_key=session_key)

        for handler_ref in handler_refs:
            handler = handler_ref()
            if handler:
                handler(sender, data)
