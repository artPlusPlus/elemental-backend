import logging
from typing import Union
from uuid import UUID

from .._resource_model_base import ResourceModelBase
from ..resources import Resource
from ..errors import (
    ResourceError
)


_LOG = logging.getLogger(__name__)


class ResourceModel(ResourceModelBase):
    __resource_cls__ = Resource
    __resource_indexes__ = tuple()

    def register(self,
                 resource: Resource):
        hook = resource.id_changed
        handler = self._handle_resource_id_changed
        hook.add_handler(handler)

    def retrieve(self,
                 resource_id: UUID,
                 resource: Union[None, Resource] = None):
        return resource

    def release(self,
                resource: Resource):
        hook = resource.id_changed
        handler = self._handle_resource_id_changed
        hook.remove_handler(handler)

    @staticmethod
    def _handle_resource_id_changed(sender, data):
        msg = 'Mutable Ids are not supported.'

        _LOG.error(msg)
        raise ResourceError(
            msg, resource_type=type(sender), resource_id=sender.id)
