import logging
import collections

from .._resource_model_base import ResourceModelBase
from .._resource_index import ResourceIndex
from ..resources import (
    ViewResult,
    ViewInstance
)


_LOG = logging.getLogger(__name__)


class ViewResultModel(ResourceModelBase):
    __resource_cls__ = ViewResult
    __resource_indexes__ = (
        ResourceIndex(ViewResult, ViewInstance)
    )

    def register(self, resource):
        idx_vr_vi = self._get_index(ViewResult, ViewInstance)
        idx_vr_vi.push_index(resource)

        hook = resource.content_instance_ids_changed
        handler = self._handle_view_result_content_instance_ids_changed
        hook.add_handler(handler)

        ref = type(resource).view_instance
        resolver = self._resolve_view_result_view_instance
        ref.add_resolver(resource, resolver)

        ref = type(resource).content_instances
        resolver = self._get_resources
        ref.add_resolver(resource, resolver)

    def retrieve(self, resource_id, resource=None):
        result = resource

        self._update_view_result_content_instances(resource.id)

        return result

    def release(self, resource):
        idx_vr_vi = self._get_index(ViewResult, ViewInstance)
        idx_vr_vi.pop_index(resource)

        hook = resource.content_instance_ids_changed
        handler = self._handle_view_result_content_instance_ids_changed
        hook.remove_handler(handler)

        ref = type(resource).view_instance
        ref.remove_resolver(resource)

        ref = type(resource).content_instances
        ref.remove_resolver(resource)

    def _handle_view_result_content_instance_ids_changed(
            self, sender, event_data):
        pass

    def _resolve_view_result_view_instance(self, view_result_id):
        idx_vr_vi = self._get_index(ViewResult, ViewInstance)

        try:
            result = idx_vr_vi.get_indexed_value(view_result_id)[0]
        except IndexError:
            result = NO_VALUE
        else:
            result = self._get_resource(result)

        return result

    def _update_view_result_content_instances(
            self, view_result_id, content_instance_ids=None,
            filter_instance_ids=None, sorter_instance_ids=None):
        """
        Computes the ContentInstances referenced by a ViewResult.

        A ViewResult references ContentInstances that match criteria defined
        by FilterInstances that are managed by the ViewResult's corresponding
        ViewInstance.
        """
        view_result = self._resources.get(view_result_id)
        if not view_result:
            return

        view_instance = view_result.view_instance
        if not view_instance:
            return

        view_result_content_instance_ids = view_result.content_instance_ids.copy()

        if not content_instance_ids:
            map_vt_cis = self._map__view_type__content_instances
            content_instance_ids = map_vt_cis.get(view_instance.type_id, set())

            # This intersection update accounts for when a ViewType no longer
            # references a ContentType. The ContentInstance Ids of the discarded
            # ContentType need to be purged from the ViewResult.
            view_result_content_instance_ids.intersection_update(
                content_instance_ids)
        elif not isinstance(content_instance_ids, collections.Iterable):
            content_instance_ids = [content_instance_ids]

        if filter_instance_ids:
            if isinstance(filter_instance_ids, collections.Iterable):
                filter_instances = self._resolve_resources(filter_instance_ids)
            else:
                try:
                    filter_instances = self._resources[filter_instance_ids]
                except KeyError:
                    msg = 'Invalid value for filter_instance_ids: {0}'
                    msg = msg.format(filter_instance_ids)

                    _LOG.error(msg)
                    raise ValueError(msg)
                else:
                    filter_instances = [filter_instances]
        else:
            filter_instances = view_instance.filter_instances

        if sorter_instance_ids:
            if isinstance(sorter_instance_ids, collections.Iterable):
                sorter_instances = self._resolve_resources(sorter_instance_ids)
            else:
                try:
                    sorter_instances = self._resources[sorter_instance_ids]
                except KeyError:
                    msg = 'Invalid value for sorter_instance_ids: {0}'
                    msg = msg.format(sorter_instance_ids)

                    _LOG.error(msg)
                    raise ValueError(msg)
                else:
                    sorter_instances = [sorter_instances]
        else:
            sorter_instances = view_instance.sorter_instances

        adds, discards = self._apply_filters(content_instance_ids,
                                             filter_instances)
        view_result_content_instance_ids.difference_update(discards)
        view_result_content_instance_ids.update(adds)

        view_result_content_instance_ids = self._apply_sorters(
            view_result_content_instance_ids, sorter_instances)

        view_result.content_instance_ids = view_result_content_instance_ids
