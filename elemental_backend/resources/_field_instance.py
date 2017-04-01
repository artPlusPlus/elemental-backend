from elemental_core import NO_VALUE

from ._resource_instance import ResourceInstance

from ._field_dirtied_hook import FieldDirtiedHook


class FieldInstance(ResourceInstance):
    @property
    def was_dirtied(self):
        return self._was_dirtied

    def __init__(self, id=None, type_id=None):
        super(FieldInstance, self).__init__(id=id, type_id=type_id)

        self._value_data = {}
        self._was_dirtied = FieldDirtiedHook()

    def is_dirty(self, value_key=NO_VALUE, session_key=NO_VALUE):
        history = self._get_history(value_key, session_key)
        if history is not NO_VALUE:
            return history.current_value.is_dirty
        return False

    def get_value(self, value_key=NO_VALUE, session_key=NO_VALUE):
        history = self._get_history(value_key, session_key)
        if history is not NO_VALUE:
            return history.current_value
        return NO_VALUE

    def set_value(self, new_value, value_key=NO_VALUE, session_key=NO_VALUE):
        history = self._get_history(value_key, session_key)

        if history is NO_VALUE:
            session_values = self._value_data.setdefault(value_key, {})
            history = session_values.setdefault(session_key, FieldHistory())

        handler = self._handle_value_was_dirtied
        new_value.was_dirtied.add_handler(handler)

        history.append(new_value)
        self._was_dirtied(self, value_key, session_key)

    def get_history_cursor(self, value_key=NO_VALUE, session_key=NO_VALUE):
        history = self._get_history(value_key, session_key)
        if history is not NO_VALUE:
            return history.cursor

    def set_history_cursor(self, position, value_key=NO_VALUE, session_key=NO_VALUE):
        history = self._get_history(value_key, session_key)
        if history is not NO_VALUE:
            history.cursor = position

    def _get_history(self, value_key, session_key):
        if self.type.value_resolution_order:
            if value_key is NO_VALUE:
                for value_key in self.type.value_resolution_order:
                    if value_key in self._value_data:
                        break
                else:
                    return NO_VALUE
            elif value_key not in self.type.value_resolution_order:
                msg = 'Invalid Value Key: "{0}" not in defined value slots.'
                msg = msg.format(value_key)
                raise KeyError(msg)
        elif value_key is not NO_VALUE:
            msg = 'Invalid Value Key: Field has no value slots.'
            msg = msg.format(value_key)
            raise KeyError(msg)

        try:
            return self._value_data[value_key][session_key]
        except KeyError:
            return NO_VALUE

    def _handle_value_was_dirtied(self, sender, data):
        try:
            value_key = data.value_key
            session_key = data.session_key
        except AttributeError:
            return

        try:
            history = self._value_data[value_key][session_key]
            current_value = history.current
        except (KeyError, IndexError):
            return

        # Only propagate change if sender is the current value.
        if sender is current_value:
            self._was_dirtied(self, value_key, session_key)
