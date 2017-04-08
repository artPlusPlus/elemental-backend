from typing import AnyStr

from elemental_core import (
    Hook,
    ValueChangedHookData
)

from ._immutable_resource import ImmutableResource


class ImmutableTypeResource(ImmutableResource):
    """
    Represents a type whose data is not tracked using the `Value` system.
    """
    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        if value == self._label:
            return

        original_value = self._label
        self._label = value

        self._on_label_changed(original_value, value)

    @property
    def doc(self):
        return self._doc

    @doc.setter
    def doc(self, value):
        if value == self._doc:
            return

        original_value = self._doc
        self._doc = value

        self._on_doc_changed(original_value, value)

    def __init__(self,
                 label: AnyStr = None,
                 doc: AnyStr = None):
        super(ImmutableTypeResource, self).__init__()

        self._label = None
        self._doc = None

        self.label_changed = Hook()
        self.doc_changed = Hook()

        self.label = label
        self.doc = doc

    def _on_label_changed(self, original_value, current_value):
        data = ValueChangedHookData(original_value, current_value)
        self.label_changed(self, data)

    def _on_doc_changed(self, original_value, current_value):
        data = ValueChangedHookData(original_value, current_value)
        self.doc_changed(self, data)
