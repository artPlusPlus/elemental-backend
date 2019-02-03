import logging

from .._resource_model_base import ResourceModelBase
from ..resources import ImmutableResource


_LOG = logging.getLogger(__name__)


class ImmutableResourceModel(ResourceModelBase):
    __resource_cls__ = ImmutableResource
    __resource_indexes__ = tuple()
