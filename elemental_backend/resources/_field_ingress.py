import weakref

from ._field_value import FieldValue


class FieldIngress(FieldValue):
    @property
    def value(self):
        if self._is_dirty:
            ingress_value = self._source_field.get_value(session_key=self._source_session_key)
            self._value = ingress_value.value
            self._is_dirty = False
        return self._value

    def __init__(self, source_field, source_session_key):
        super(FieldIngress, self).__init__()

        try:
            self._source_field = weakref.proxy(source_field)
        except TypeError:
            self._source_field = source_field

        self._source_session_key = source_session_key

        self._source_field.was_dirtied.add_handler(
            self._handle_source_field_dirtied, session_key=source_session_key)

    def _handle_source_field_dirtied(self, sender, data):
        self.dirty()
