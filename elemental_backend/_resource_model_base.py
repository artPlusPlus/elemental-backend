import weakref


class ResourceModelBase(object):
    __resource_cls__ = None
    __resource_indexes__ = None

    def __init__(self, core_model):
        super(ResourceModelBase, self).__init__()

        self._core_model = weakref.proxy(core_model)

        self._core_model.register += self._handle_resource_registered
        self._core_model.retrieve += self._handle_resource_retrieved
        self._core_model.release += self._handle_resource_released

    def register(self, core_model, resource):
        raise NotImplementedError()

    def retrieve(self, core_model, resource_id, resource=None):
        raise NotImplementedError()

    def release(self, core_model, resource):
        raise NotImplementedError()

    def _handle_resource_registered(self, sender, data):
        if not isinstance(data, self.__resource_cls__):
            return

        self.register(sender, data)

    def _handle_resource_retrieved(self, sender, data):
        if not isinstance(data, self.__resource_cls__):
            return

        self.retrieve(sender, data)

    def _handle_resource_released(self, sender, data):
        if not isinstance(data, self.__resource_cls__):
            return

        self.release(sender, data)

    def _resolve_resource(self, resource_id):
        return self._core_model.get_resource(resource_id)

    def _resolve_resources(self, resource_ids):
        result = [self._core_model.get_resource(r_id) for r_id in resource_ids]
        result = [r for r in result if r]
        if len(result) == len(resource_ids):
            return result
        return tuple()

