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

    def register(self, core_model, resource):
        if not resource.type_id:
            msg = (
                'Failed to register resource "{0}": '
                'Invalid type id - "{1}"'
            )
            msg = msg.format(repr(resource), resource.type_id)

            _LOG.error(msg)
            raise ResourceNotRegisteredError(
                msg, resource_type=type(resource),
                resource_id=resource.id)

        idx_ai_ci = core_model.get_resource_index(AttributeInstance, ContentInstance)
        for attribute_id in resource.attribute_ids:
            idx_ai_ci.push_index_value(attribute_id, resource)

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
        resolver = self._resolve_resources
        ref.add_resolver(resource, resolver)

    def retrieve(self, core_model, resource_id, resource=None):
        pass

    def release(self, core_model, resource):
        idx_ai_ci = core_model.get_resource_index(AttributeInstance, ContentInstance)
        for attribute_id in resource.attribute_ids:
            idx_ai_ci.pop_index_value(attribute_id, resource)

        raise RuntimeError('TODO: AddViewTypeModel hook')
        # self._update_view_instance_content_instances()

        hook = resource.attribute_ids_changed
        handler = self._handle_content_instance_attribute_ids_changed
        hook.remove_handler(handler)

        ref = type(resource).attributes
        ref.remove_resolver(resource)

    def _handle_content_instance_attribute_ids_changed(self, sender, data):
        pass
