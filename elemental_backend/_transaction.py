import uuid


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
        return self._resource_type

    @property
    def resource_id(self):
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
    def outbound_payload(self):
        return self._outbound_payload

    @property
    def data(self):
        return self._data

    @property
    def errors(self):
        return self._errors

    def __init__(self, action, resource_type, resource_id, super_id=None,
                 inbound_format=None, inbound_paylaod=None,
                 outbound_format=None):
        self._id = uuid.uuid4()
        self._action = action
        self._resource_type = resource_type
        self._resource_id = resource_id
        self._super_id = super_id
        self._inbound_format = inbound_format
        self._inbound_payload = inbound_paylaod
        self.inbound_importer = None
        self._outbound_format = outbound_format
        self._outbound_payload = None
        self.outbound_exporter = None

        self.target_resource = None
        self._data = {}
        self._errors = []
