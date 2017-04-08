from elemental_core import Hook, ValueChangedHookData

from ._immutable_instance_resource import ImmutableInstanceResource


class ValueDataInstanceResource(ImmutableInstanceResource):
    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        if value == self._content:
            return

        original_value = self._content
        self._content = value

        self._on_content_changed(original_value, self._content)

    def __init__(self):
        super(ValueDataInstanceResource, self).__init__()

        self._content = None

        self.content_changed = Hook()

    def _on_content_changed(self, original_value, current_value):
        data = ValueChangedHookData(original_value, current_value)
        self.content_changed(self, data)
