import logging
import uuid

from ._errors import (
    ContentTypeImportError,
    ContentTypeNotFoundError,
    ContentImportError,
    ContentNotFoundError,
    AttributeTypeCollisionError,
    AttributeCollisionError
)

from ._content_type import ContentType
from ._content_instance import ContentInstance
from ._attribute_type import AttributeType
from ._attribute_instance import AttributeInstance


_LOG = logging.getLogger(__name__)


class Manager(object):
    def __init__(self):
        self._content_types = {}
        self._content_instances = {}
        self._attribute_types = {}
        self._attribute_instances = {}
        self._map__content_type__attribute_types = {}
        self._map__content_type__content_instances = {}
        self._map__content_instance__attribute_instances = {}
        self._map__target_attr__source_attr = {}

    def import_content_type_json(self, content_type_json):
        """
        Creates a managed ContentType instance from the provided json data.

        The ContentType instance is owned by the Manager. If an existing
        ContentType instance owned by the Manager shares the ID provided in the
        json data, an error is raised unless `force` is `True`.

        :param content_type_json:
        :return:
        """
        content_type, attribute_types = self._load_content_type_json(content_type_json)

        if content_type.id in self._content_types:
            msg = (
                'Failed to Import Content Type "{0}". '
                'Collision with existing Content Type: {1}'
            )
            msg = msg.format(content_type.name, content_type.id)
            _LOG.error(msg)
            raise ContentTypeImportError(msg)

        attr_collisions = [a for a in attribute_types if a in self._attribute_types]
        attr_collisions = ["{0}".format(a.id) for a in attr_collisions]
        attr_collisions = ', '.join(attr_collisions)
        if attr_collisions:
            msg = (
                'Failed to Import Attribute Types for Content Type "{0}". '
                'Id collisions with existing Attribute Types: {1}.'
            )
            msg = msg.format(content_type.id, attr_collisions)
            _LOG.error(msg)
            raise AttributeTypeCollisionError(msg)

        self._register_content_type(content_type)
        for attribute_type in attribute_types:
            self._register_attribute_type(content_type.id, attribute_type)

        return content_type.id, tuple([at.id for at in attribute_types])

    def get_content_type(self, content_type_id):
        """
        Retrieves an existing, managed ContentType instance with the given id.

        :param content_type_id:
        :return:
        """
        if not isinstance(content_type_id, uuid.UUID):
            content_type_id = uuid.UUID(content_type_id)

        try:
            return self._content_types[content_type_id]
        except KeyError:
            msg = 'No Content Type found with id: "{0}".'
            msg = msg.format(content_type_id)
            _LOG.error(msg)
            raise ContentTypeNotFoundError(msg)

    def export_content_type_json(self, content_type_id):
        """

        :param content_type_id:
        :return:
        """
        if not isinstance(content_type_id, uuid.UUID):
            content_type_id = uuid.UUID(content_type_id)

        try:
            content_type = self._content_types[content_type_id]
        except KeyError:
            msg = 'No Content Type found with id: "{0}".'
            msg = msg.format(content_type_id)
            _LOG.error(msg)
            raise ContentTypeNotFoundError(msg)

        attr_type_ids = self._map__content_type__attribute_types[content_type.id]
        attr_type_ids = [str(attr_type.id) for attr_type in attr_type_ids]

        base_ids = [str(id) for id in content_type.base_ids]

        result = {
            'id': str(content_type.id),
            'name': content_type.name,
            'base_ids': base_ids,
            'attribute_type_ids': attr_type_ids,
        }

        return result

    def import_content_json(self, content_json, force=False):
        """
        Creates a managed Content Instance from the provided json data.

        The ContentInstance instance is owned by the Manager. If an existing
        ContentInstance instance owned by the Manager shares the ID provided
        in the json data, an error is raised unless `force` is `True`.

        :param content_json:
        :return:
        """
        content, attributes = self._load_content_instance_json(content_json)

        if content.id in self._content_instances and not force:
            msg = (
                'Failed to Import Content Instance "{0}". '
                'Collision with existing Content Instance.'
            )
            msg = msg.format(id)
            _LOG.error(msg)
            raise ContentImportError(msg)

        attr_collisions = [a for a in attributes if a in self._attribute_instances]
        attr_collisions = ["{0}".format(a.id) for a in attr_collisions]
        attr_collisions = ', '.join(attr_collisions)
        if attr_collisions and not force:
            msg = (
                'Failed to Import Attributes for Content Instance "{0}". '
                'Id collisions with existing Attributes: {1}.'
            )
            msg = msg.format(id, attr_collisions)
            _LOG.error(msg)
            raise AttributeCollisionError(msg)

        self._register_content_instance(content)
        for attr in attributes:
            self._register_content_attribute(id, attr)

    def get_content(self, content_id):
        """
        Retrieves an existing, managed Content instance with the given id.

        :param content_id:
        :return:
        """
        if not isinstance(content_id, uuid.UUID):
            content_id = uuid.UUID(content_id)

        try:
            return self._content_instances[content_id]
        except:
            msg = 'No Content found with id "{0}".'
            msg = msg.format(content_id)
            _LOG.error(msg)
            raise ContentNotFoundError(msg)

    @staticmethod
    def _load_content_type_json(content_type_json):
        id = uuid.UUID(content_type_json['id'])
        name = content_type_json['name']
        base_ids = content_type_json['base_ids']
        base_ids = [uuid.UUID(base) for base in base_ids]
        base_ids = tuple(base_ids)

        content_type = ContentType(name, id=id, base_ids=base_ids)

        attribute_types = []
        for i, attr_type_json in enumerate(content_type_json['attributes']):
            attr_type = Manager._load_attribute_type_json(attr_type_json)
            attribute_types.append(attr_type)

        return content_type, attribute_types

    @staticmethod
    def _load_attribute_type_json(attr_type_json):
        id = attr_type_json['id']
        name = attr_type_json['name']
        kind_id = attr_type_json['kind_id']
        default_value = attr_type_json['default_value']
        kind_properties = attr_type_json['kind_properties']

        return AttributeType(kind_id, name, id=id, default_value=default_value,
                             kind_properties=kind_properties)

    @staticmethod
    def _load_content_instance_json(content_json):
        type_id = uuid.UUID(content_json['type_id'])
        id = uuid.UUID(content_json['id'])

        content_instance = ContentInstance(type_id, id=id)

        attribute_instances = []
        for attr_json in content_json['attributes']:
            attr = Manager._load_attribute_instance_json(attr_json)
            attribute_instances.append(attr)

        return content_instance, attribute_instances

    @staticmethod
    def _load_attribute_instance_json(attr_json):
        type_id = attr_json['type_id']
        id = attr_json['id']
        value = attr_json['value']

        return AttributeInstance(type_id, id=id, value=value)

    def _register_content_type(self, content_type):
        self._content_types[content_type.id] = content_type

    def _register_content_instance(self, content_instance):
        self._content_instances[content_instance.id] = content_instance

        map_type_instances = self._map__content_type__content_instances
        try:
            content_instances = map_type_instances[content_instance.type_id]
        except KeyError:
            content_instances = []
            map_type_instances[content_instance.type_id] = content_instances
        content_instances.append(content_instance.id)

    def _register_attribute_type(self, content_type_id, attribute_type):
        self._attribute_types[attribute_type.id] = attribute_type

        content_type_attr_types = self._map__content_type__attribute_types
        try:
            attr_types = content_type_attr_types[content_type_id]
        except KeyError:
            attr_types = []
            content_type_attr_types[content_type_id] = attr_types
        attr_types.append(attribute_type)

    def _register_content_attribute(self, content_id, attribute):
        self._attribute_instances[attribute.id] = attribute

        map_content_attrs = self._map__content_instance__attribute_instances
        try:
            content_attrs = map_content_attrs[content_id]
        except KeyError:
            content_attrs = []
            map_content_attrs[content_id] = content_attrs
        content_attrs.append(attribute.id)
