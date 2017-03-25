import weakref
from collections import deque


class ResourceIndex(object):
    @property
    def key_type(self):
        return self._key_type

    @property
    def value_type(self):
        return self._value_type

    def __init__(self, index_key_type, indexed_value_type,
                 indexed_capacity=None):
        super(ResourceIndex, self).__init__()

        try:
            self._index_key_type = weakref.ref(index_key_type)
        except TypeError:
            self._index_key_type = index_key_type

        try:
            self._value_type = weakref.ref(indexed_value_type)
        except TypeError:
            self._value_type = indexed_value_type

        self._indexed_capacity = int(indexed_capacity)
        self._eternal_keys = weakref.WeakSet()
        self._map__index_key__indexed_data = weakref.WeakKeyDictionary()

    def create_index(self, key):
        try:
            key = key.id
        except AttributeError:
            key = key

        if key in self._map__idx_resource_id__resource_ids:
            if key in self._eternal_keys:
                msg = 'Index already has eternal key'
                raise ValueError(msg)
            self._set_eternal_key(key)
        else:
            value_collection = deque()
            self._map__idx_resource_id__resource_ids[key] = value_collection

    def push_index_value(self, key, value):
        try:
            key = key.id
        except AttributeError:
            key = key

        try:
            value = value.id
        except AttributeError:
            value = value

        try:
            value_collection = self._map__idx_resource_id__resource_ids[key]
        except KeyError:
            value_collection = deque()
            self._map__idx_resource_id__resource_ids[key] = value_collection

        value_collection.append(value)
        while 0 < self._indexed_capacity < len(value_collection):
            value_collection.popleft()

    def iter_index(self, key):
        try:
            key = key.id
        except AttributeError:
            key = key

        try:
            collection = self._map__idx_resource_id__resource_ids[key]
        except KeyError:
            raise StopIteration()

        for item in collection:
            yield item

    def pop_index(self, key):
        try:
            key = key.id
        except AttributeError:
            key = key

        try:
            result = self._map__idx_resource_id__resource_ids.pop(key)
        except KeyError:
            result = NO_VALUE
        else:
            result = tuple(result)

        return result

    def pop_index_value(self, key, value):
        try:
            key = key.id
        except AttributeError:
            key = key

        try:
            value_collection = self._map__idx_resource_id__resource_ids[key]
        except KeyError:
            return NO_VALUE

        try:
            value_collection.remove(value)
        except KeyError:
            return None
        else:
            return value

    def move_index_value(self, value, source_key, target_key):
        self.remove(source_key, value)
        self.add(target_key, value)

    def _set_eternal_key(self, current_key, eternal_key):
        """
        Helper function for ensuring a specific object instance is used
        as the key for a map entry.

        Model is intended to support unordered registration of `Resources`.
        There are cases where a dependent `Resource` will create an entry
        in a map because the dependency has not yet been registered. This
        function allows the dependency to insert its own object as the key.
        This is especially important when using a WeakKeyDictionary as the map.
        """
        try:
            value_collection = self._map__idx_resource_id__resource_ids.pop(current_key)
        except KeyError:
            value_collection = deque

        self._map__idx_resource_id__resource_ids[eternal_key] = value_collection
        self._eternal_keys.add(eternal_key)
