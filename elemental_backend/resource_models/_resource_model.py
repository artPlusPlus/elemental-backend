import logging
import weakref

from .._resource_model_base import ResourceModelBase
from ..resources import Resource
from ..errors import (
    ResourceError,
    ResourceCollisionError,
    ResourceNotFoundError
)


_LOG = logging.getLogger(__name__)


class ResourceModel(ResourceModelBase):
    __resource_cls__ = Resource
    __resource_indexes__ = tuple()

    def register(self, core_model, resource):
        if core_model.has_resource(resource):
            msg = (
                'Failed to register resource with id "{0}": '
                'Resource already exists with id "{0}"'
            )
            msg = msg.format(resource.id)

            _LOG.error(msg)
            raise ResourceCollisionError(msg, resource_type=type(resource),
                                         resource_id=resource.id)

        core_model.add_resource(resource)

        idx_rc_rs = core_model.index__resource_cls__resources
        cls_resources = idx_rc_rs.setdefault(type(resource), weakref.WeakSet())
        cls_resources.add(resource.id)

        hook = resource.id_changed
        handler = self._handle_resource_id_changed
        hook.add_handler(handler)

    def retrieve(self, core_model, resource_id, resource=None):
        # MSR|2017.03
        # `return` was added to compensate for commented function body.
        # Why the function body was commented is unknown.
        return

        try:
            return core_model.get_resource(resource_id)
        except KeyError:
            msg = (
                'Failed to retrieve resource:'
                'No resource found matching id "{0}"'
            )
            msg = msg.format(resource_id)

            _LOG.error(msg)
            raise ResourceNotFoundError(
                msg, resource_type=None, resource_id=resource_id)

    def release(self, core_model, resource):
        try:
            core_model.remove_resource(resource)
        except KeyError:
            msg = (
                'Failed to release resource: '
                'No resource found matching id "{0}"'
            )
            msg = msg.format(resource.id)

            _LOG.error(msg)
            raise ResourceNotFoundError(
                msg, resource_type=type(resource), resource_id=resource.id)

        idx_rc_rs = core_model.map__resource_cls__resources
        try:
            idx_rc_rs[type(resource)].discard(resource.id)
        except KeyError:
            msg = (
                'Failed to deregister resource with id "{0}": '
                'Unrecognized resource type "{1}".'
            )
            msg = msg.format(resource.id, repr(type(resource)))

            _LOG.error(msg)
            raise ResourceNotFoundError(
                msg, resource_type=type(resource), resource_id=resource.id)

        hook = resource.id_changed
        handler = self._handle_resource_id_changed
        hook.remove_handler(handler)

    def _handle_resource_id_changed(self, sender, data):
        msg = 'Mutable Ids are not supported.'

        _LOG.error(msg)
        raise ResourceError(
            msg, resource_type=type(sender), resource_id=sender.id)
