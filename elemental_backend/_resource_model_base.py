from weakref import WeakMethod

from elemental_core import NO_VALUE


class ResourceModelBase(object):
    __resource_cls__ = None
    __resource_indexes__ = None

    @property
    def resource_registered_handler(self):
        return WeakMethod(self._handle_resource_registered)

    @property
    def resource_registration_failed_handler(self):
        return WeakMethod(self._handle_resource_registration_failed)

    @property
    def resource_retrieved_handler(self):
        return WeakMethod(self._handle_resource_retrieved)

    @property
    def resource_retrieval_failed_handler(self):
        return WeakMethod(self._handle_resource_retrieval_failed)

    @property
    def resource_released_handler(self):
        return WeakMethod(self._handle_resource_released)

    @property
    def resource_release_failed_handler(self):
        return WeakMethod(self._handle_resource_release_failed)

    def __init__(self, resource_getter, index_getter):
        super(ResourceModelBase, self).__init__()

        self._get_resource = resource_getter
        self._get_index = index_getter

    def register(self, resource):
        raise NotImplementedError()

    def retrieve(self, resource_id, resource=None):
        raise NotImplementedError()

    def release(self, resource):
        raise NotImplementedError()

    def _handle_resource_registered(self, sender, data):
        pass

    def _handle_resource_registration_failed(self, sender, data):
        pass

    def _handle_resource_retrieved(self, sender, data):
        pass

    def _handle_resource_retrieval_failed(self, sender, data):
        pass

    def _handle_resource_released(self, sender, data):
        pass

    def _handle_resource_release_failed(self, sender, data):
        pass

    def _get_resources(self, resource_ids):
        result = [self._get_resource(r_id) for r_id in resource_ids]
        result = [r for r in result if r]
        if len(result) == len(resource_ids):
            return result
        return NO_VALUE
