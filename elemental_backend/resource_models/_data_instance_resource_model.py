import logging
from typing import Optional
from uuid import UUID

from .._resource_model_base import ResourceModelBase
from ..resources import DataInstanceResource


_LOG = logging.getLogger(__name__)


class DataInstanceResourceModel(ResourceModelBase):
    __resource_cls__ = DataInstanceResource
    __resource_indexes__ = tuple()

