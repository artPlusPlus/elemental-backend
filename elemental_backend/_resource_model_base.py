from weakref import (
    ref as WeakRef,
    WeakKeyDictionary,
    WeakMethod,
    WeakSet
)
from functools import partial

from elemental_core import NO_VALUE

from .resources import Resource


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
        self._map__hook__handler = WeakKeyDictionary()
        self._map__hook__ref = WeakKeyDictionary()
        self._unresolved_reference_maps = WeakKeyDictionary()
        self._resolved_reference_maps = WeakKeyDictionary()

        self._init_hook_forward_reference_map()
        self._init_forward_reference_resolver_map()
        self._init_forward_reference_maps()

    def _init_hook_forward_reference_map(self):
        pass

    def _init_forward_reference_resolver_map(self):
        pass

    def _init_forward_reference_maps(self):
        if not self.__resource_cls__:
            return

        for fwd_ref in self.__resource_cls__.iter_fwd_refs():
            self._unresolved_reference_maps[fwd_ref] = WeakKeyDictionary()
            self._resolved_reference_maps[fwd_ref] = WeakKeyDictionary()
            fwd_ref.reference_resolver = self._get_resource

    def register(self, resource):
        for hook, fwd_ref in self._map__hook__ref.iteritems():
            hook = hook.__get__(resource)
            fwd_ref = WeakRef(fwd_ref)
            handler = partial(self._handle_forward_reference_key_changed,
                              fwd_ref)
            hook += handler

        for hook, handler in self._map__hook__handler.iteritems():
            hook = hook.__get__(resource)
            hook += handler

        for fwd_ref in resource.iter_forward_references():
            self._track_forward_reference(resource, fwd_ref)

    def _handle_forward_reference_key_changed(self, fwd_ref, sender, data):
        self._forward_reference_target_changed(
            sender, fwd_ref, data.original_value)

    def retrieve(self, resource_id, resource=None):
        return resource

    def release(self, resource):
        for hook, handler in self._map__hook__handler.iteritems():
            hook = hook.__get__(resource)
            hook -= handler

    def _handle_resource_registered(
            self, sender,
            data: Resource):
        self._resolve_forward_references(data)

    def _handle_resource_registration_failed(self, sender, data):
        pass

    def _handle_resource_retrieved(self, sender, data):
        pass

    def _handle_resource_retrieval_failed(self, sender, data):
        pass

    def _handle_resource_released(self, sender, data):
        self._break_forward_references(data)

    def _handle_resource_release_failed(self, sender, data):
        pass

    def _get_resources(self, resource_ids):
        result = [self._get_resource(r_id) for r_id in resource_ids]
        result = [r for r in result if r]
        if len(result) == len(resource_ids):
            return result
        return NO_VALUE

    def _resolve_forward_references(self, reference_target):
        for reference in self._unresolved_reference_maps:
            map__ref_tgt_id__referrer_ids = self._unresolved_reference_maps[reference]
            try:
                referrer_ids = map__ref_tgt_id__referrer_ids.pop(reference_target.id)
            except KeyError:
                continue
            else:
                break
        else:
            return

        for referrer_id in referrer_ids:
            referrer = self._get_resource(referrer_id)
            reference.__set__(referrer, reference_target)
            self._track_forward_reference(
                referrer, reference_target.id,
                reference_map=self._resolved_reference_maps[reference])

    def _break_forward_references(self, reference_target):
        for reference in self._resolved_reference_maps:
            map__ref_tgt_id__referrer_ids = self._resolved_reference_maps[reference]
            try:
                referrer_ids = map__ref_tgt_id__referrer_ids.pop(reference_target.id)
            except KeyError:
                continue
            else:
                break
        else:
            return

        for referrer_id in referrer_ids:
            referrer = self._get_resource(referrer_id)
            self._track_forward_reference(
                referrer, reference_target,
                reference_map=self._unresolved_reference_maps[reference])

    def _forward_reference_target_changed(self, referrer, reference,
                                          original_target):
        try:
            self._unresolved_reference_maps[reference][original_target].pop(referrer.id)
        except KeyError:
            try:
                self._resolved_reference_maps[reference][original_target].pop(referrer.id)
            except KeyError:
                pass

        self._track_forward_reference(referrer, reference)

    def _track_forward_reference(self, referrer, reference, reference_map=None):
        """
        Tracks whether a ForwardReference is resolved or not.
         
        This state is tracked in order to know 
         
        Args:
            referrer: 
            reference: 

        Returns:

        """
        bound_reference = reference.__get__(referrer)
        if not bound_reference.reference_key:
            return

        if not reference_map:
            if bound_reference():
                reference_map = self._resolved_reference_maps[reference]
            else:
                reference_map = self._unresolved_kind_id_refs[reference]

        try:
            referrers = reference_map[bound_reference.reference_key]
        except KeyError:
            referrers = WeakSet()
            reference_map[bound_reference.reference_key] = referrers
        referrers.add(referrer.id)
