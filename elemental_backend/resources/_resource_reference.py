import weakref
import logging
from functools import partial


_LOG = logging.getLogger(__name__)


class ResourceReference(object):
    """
    Provides a mechanism for allowing one `Resource` object to provide access
        to another `Resource` object.

    The implementation of this mechanism relies on a `Model` to provide a
    reference to its resources table upon registration of a `Resources`.
    Currently, multiple `Model` instances can exist at the same time. Being a
    descriptor, `ResourceReference` instances exist in a broader  scope (class
    instances) than `Model` instances. Thus, `ResourceReference` instances must
    account for the possibility that multiple resource tables will need to be
    handled concurrently. To handle this possibility, `ResourceReference`
    maintains a map of `Resource` Ids and resource handles. Whenever a `Model`
    registers a `Resource`, a new entry is created in this mapping. This
    directly affects performance when registering and resolving `Resource`s.
    Should a bottleneck occur, a decision will need to be made as to whether
    or not multiple `Model` instances should be permitted.
    """
    def __init__(self, resource_key_fget):
        self._resource_key_fget = resource_key_fget
        self._map__resource_id__resolver = weakref.WeakKeyDictionary()

    def __get__(self, instance, _):
        if instance is None:
            return self

        if self._resource_key_fget is None:
            # Should never get here, but just in case
            msg = 'ResourceReference not attached to a getter method.'
            raise AttributeError(msg)

        result = None

        try:
            resolver = self._map__resource_id__resolver[instance.id]
        except TypeError:
            # Occurs when instance.id is None. While this happens during
            # testing, it should not happen in production.
            return result
        except KeyError:
            msg = (
                'Failed to resolve Resource:'
                'Resource instance "{0}" not registered with a Model.'
            )
            msg = msg.format(repr(instance))

            _LOG.warn(msg)
            return result
        else:
            if isinstance(resolver, weakref.ref):
                resolver = resolver()
                if not resolver:
                    msg = 'Failed to resolve Resource: Resolver reference dead'
                    raise RuntimeError(msg)

        resource_key = self._resource_key_fget(instance)

        if resource_key:
            try:
                result = resolver(resource_key)
            except AttributeError:
                if not self._model_resources:
                    msg = (
                        'Failed to resolve Resource: '
                        'Model._resources reference is dead.'
                    )
                    _LOG.error(msg)
            else:
                if result:
                    msg = 'Resolved Resource: "{0}"'
                    msg = msg.format(repr(result))
                else:
                    msg = 'Failed to resolve Resource "{0}"'
                    msg = msg.format(resource_key)
                _LOG.debug(msg)
        else:
            msg = (
                'Failed to resolve Resource: '
                'invalid Resource Id "{0}"'
            )
            msg = msg.format(resource_key)
            _LOG.warn(msg)

        return result

    def add_resolver(self, resource_instance, resolver):
        """
        Registers a callable capable of producing one or more `Resources`
            using a given key.

        The intention behind registration is to provide for the possibility
        that multiple `Model` instances may exist within the same interpreter.
        Whenever a `Resource` is registered with a `Model`, the `Model` will
        register a handler with this object.

        Note:
            This could be problematic, as it allows for the possibility of a
            very large number of reference objects to be created.
            See class docstring.
        """
        callback_died_handler = partial(
            weakref.WeakMethod(self._callback_died),
            weakref.ref(resource_instance.id))

        try:
            resolver = weakref.WeakMethod(resolver, callback_died_handler)
        except TypeError:
            resolver = weakref.ref(resolver, callback_died_handler)

        map_rid_r = self._map__resource_id__resolver
        map_rid_r[resource_instance.id] = resolver

    def remove_resolver(self, resource_instance):
        """
        Removes a previously registered resolver callable.
        """
        map_rid_r = self._map__resource_id__resolver
        try:
            del map_rid_r[resource_instance.id]
        except KeyError:
            pass

    def _callback_died(self, resource_id_ref, _):
        try:
            del self._map__resource_id__resolver[resource_id_ref()]
        except KeyError:
            pass
