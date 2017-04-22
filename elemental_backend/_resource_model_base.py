from weakref import (
    WeakMethod,
    WeakSet
)

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

    def _resolve_forward_reference(self, reference, reference_attr,
                                   unresolved_ref_map, resolved_ref_map):
        try:
            referrer_ids = unresolved_ref_map.pop(reference.id)
        except KeyError:
            return

        for referrer_id in referrer_ids:
            referrer = self._get_resource(referrer_id)
            setattr(referrer, reference_attr, reference)
            self._track_ref(referrer_id, reference.id, resolved_ref_map)

    def _break_forward_reference(self, reference, reference_attr,
                                 resolved_ref_map, unresolved_ref_map):
        try:
            referrer_ids = resolved_ref_map.pop(reference.id)
        except KeyError:
            return

        for referrer_id in referrer_ids:
            referrer = self._get_resource(referrer_id)
            reference_id = getattr(referrer, reference_attr).reference_key
            self._track_ref(referrer.id, reference_id, unresolved_ref_map)

    @staticmethod
    def _forward_reference_target_changed(referrer, reference_attr,
                                          unresolved_ref_map, original_target):
        try:
            del unresolved_ref_map[original_target]
        except KeyError:
            pass

        reference = getattr(referrer, reference_attr)

        if reference.reference_key and not reference():
            unresolved_ref_map[reference.reference_key] = referrer.id

    @staticmethod
    def _track_forward_reference(referrer_id, reference_id, reference_map):
        try:
            referrers = reference_map[reference_id]
        except KeyError:
            referrers = WeakSet()
            reference_map[reference_id] = referrers
        referrers.add(referrer_id)
