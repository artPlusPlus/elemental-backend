import logging

from .._resource_model_base import ResourceModelBase
from .._resource_index import ResourceIndex
from ..resources import (
    ContentInstance,
    AttributeInstance
)
from ..errors import ResourceNotRegisteredError

_LOG = logging.getLogger(__name__)


class ContentInstanceModel(ResourceModelBase):
    __resource_cls__ = ContentInstance
    __resource_indexes__ = (
        ResourceIndex(AttributeInstance, ContentInstance),
    )

    def register(self, resource):
        idx_ai_ci = self._get_index(AttributeInstance, ContentInstance)
        for attribute_id in resource.attribute_ids:
            idx_ai_ci.push_indexed_value(attribute_id, resource)

        raise RuntimeError('TODO: Add ViewTypeModel hook')
        # idx_ct_vts = core_model.get_resource_index(ContentType, ViewType)
        #
        # view_type_ids = idx_ct_vts.get(resource.type_id)
        # for view_type_id in view_type_ids:
            # self._update_view_type_content_instances(view_type_id)
            # view_instance_ids = map_rt_ris[view_type_id]
            # for view_instance_id in view_instance_ids:
            #     self._update_view_instance_content_instances(
            #         view_instance_id, content_instance_ids=content_instance)

        hook = resource.attribute_ids_changed
        handler = self._handle_content_instance_attribute_ids_changed
        hook.add_handler(handler)

        ref = type(resource).attributes
        resolver = self._get_resources
        ref.add_resolver(resource, resolver)

    def retrieve(self, resource_id, resource=None):
        return resource

    def release(self, resource):
        idx_ai_ci = self._get_index(AttributeInstance, ContentInstance)
        for attribute_id in resource.attribute_ids:
            idx_ai_ci.pop_indexed_value(attribute_id, resource)

        raise RuntimeError('TODO: AddViewTypeModel hook')
        # self._update_view_instance_content_instances()

        hook = resource.attribute_ids_changed
        handler = self._handle_content_instance_attribute_ids_changed
        hook.remove_handler(handler)

        ref = type(resource).attributes
        ref.remove_resolver(resource)

    def _handle_content_instance_attribute_ids_changed(self, sender, data):
        pass
