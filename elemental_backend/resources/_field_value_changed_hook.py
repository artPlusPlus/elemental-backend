import weakref
from collections import namedtuple

from elemental_backend.resources._hook import Hook


FieldValueChangedData = namedtuple(
    'FieldValueChangedEventArgs',
    ['original_value', 'current_value', 'session_key', 'value_key'])


class FieldValueChangedHook(Hook):
    def __init__(self):
        super(FieldValueChangedHook, self).__init__()

        self._handler_refs = {}

    def add_handler(self, handler, session_key=None, value_key=None):
        try:
            handler_ref = weakref.WeakMethod(handler, self._handler_ref_died)
        except TypeError:
            handler_ref = weakref.ref(handler, self._handler_ref_died)

        self._handler_refs.setdefault(session_key, {})[value_key] = handler_ref

    def remove_handler(self, handler, session_key=None, value_key=None):
        try:
            del self._handler_refs[session_key][value_key]
        except KeyError:
            pass

    def __call__(self, sender, data):
        try:
            sender = weakref.proxy(sender)
        except TypeError:
            pass

        try:
            handler_ref = self._handler_refs[data.session_key][data.value_key]
        except KeyError:
            return

        handler = handler_ref()
        if handler:
            handler(sender, data)
