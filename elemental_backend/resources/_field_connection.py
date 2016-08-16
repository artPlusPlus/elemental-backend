import weakref

from ._field_ingress import FieldIngress


class FieldConnection(object):
    def __init__(self):
        super(FieldConnection, self).__init__()

        self._source_id = None
        self._target_id = None

        self._target_ingress = None

    def connect(self, source_field, target_field,
                source_session_key=None, source_value_key=None,
                target_session_key=None, target_value_key=None):

        source_field.was_dirtied.add_handler(
            self._handle_source_dirtied,
            session_key=source_session_key, value_key=source_value_key)

        self._target_ingress = FieldIngress()
        target_field.set_value(weakref.proxy(self._target_ingress),
                               session_key=target_session_key,
                               value_key=target_value_key)

    def _handle_source_dirtied(self, sender, data):
        self._target_ingress.dirty = True
