import uuid

from .._util import (
    process_uuid_value,
    process_resource_type_value,
    process_data_format_value
)


class Transaction(object):
    @property
    def id(self):
        return self._id

    @property
    def super_id(self):
        return self._super_id

    @property
    def action(self):
        return self._action

    @property
    def resource_type(self):
        if self.target_resource:
            return type(self.target_resource)
        return self._resource_type

    @property
    def resource_id(self):
        if self.target_resource:
            return self.target_resource.id
        return self._resource_id

    @property
    def inbound_format(self):
        return self._inbound_format

    @property
    def inbound_payload(self):
        return self._inbound_payload

    @property
    def outbound_format(self):
        return self._outbound_format

    @property
    def data(self):
        return self._data

    @property
    def errors(self):
        return self._errors

    def __init__(self, action, resource_type=None, resource_id=None,
                 super_id=None, inbound_format=None, inbound_payload=None,
                 outbound_format=None):
        self._id = uuid.uuid4()
        self._action = action
        self._resource_type = process_resource_type_value(resource_type)
        self._resource_id = process_uuid_value(resource_id)
        self._super_id = process_uuid_value(super_id)
        self._inbound_format = process_data_format_value(inbound_format)
        self._inbound_payload = inbound_payload
        self.inbound_deserializer = None
        self._outbound_format = process_data_format_value(outbound_format)
        self.outbound_payload = None
        self.outbound_serializer = None

        self.target_resource = None
        self._data = {}
        self._errors = []

    def _drop_handler(self, ref):
        self._handler = None
