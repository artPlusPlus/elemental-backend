import logging
from typing import Optional
from uuid import UUID

from .._resource_model_base import ResourceModelBase
from ..resources import DataTypeResource


_LOG = logging.getLogger(__name__)


class DataTypeResourceModel(ResourceModelBase):
    __resource_cls__ = DataTypeResource
    __resource_indexes__ = tuple()

    def register(self,
                 resource: DataTypeResource):
        pass

    def retrieve(self,
                 resource_id: UUID,
                 resource: DataTypeResource = None
                 ) -> Optional[DataTypeResource]:
        return resource

    def release(self,
                resource: DataTypeResource):
        pass
