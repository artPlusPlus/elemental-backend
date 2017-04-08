import logging
from typing import Union
from uuid import UUID

from .._resource_model_base import ResourceModelBase
from ..resources import ImmutableTypeResource


_LOG = logging.getLogger(__name__)


class ImmutableTypeResourceModel(ResourceModelBase):
    __resource_cls__ = ImmutableTypeResource
    __resource_indexes__ = tuple()

    def register(self,
                 resource: ImmutableTypeResource):
        hook = resource.label_changed
        hook += self._handle_resource_label_changed

        hook = resource.extends_resource_ids_changed
        hook += self._handle_resource_extends_resource_ids_changed

        hook = resource.doc_changed
        hook += self._handle_resource_doc_changed

    def retrieve(self,
                 resource_id: UUID,
                 resource: Union[None, ImmutableTypeResource] = None):
        return resource

    def release(self,
                resource: ImmutableTypeResource):
        hook = resource.label_changed
        hook -= self._handle_resource_label_changed

        hook = resource.extends_resource_ids_changed
        hook -= self._handle_resource_extends_resource_ids_changed

        hook = resource.doc_changed
        hook -= self._handle_resource_doc_changed

    def _handle_resource_label_changed(self):
        pass

    def _handle_resource_extends_resource_ids_changed(self):
        pass

    def _handle_resource_doc_changed(self):
        pass
