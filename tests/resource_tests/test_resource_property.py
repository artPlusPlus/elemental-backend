import weakref

import pytest

from elemental_backend.resources._resource_property import ResourceProperty


class _TestOwner(object):
    @ResourceProperty
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def __init__(self, name=None):
        self._value = None

        self.value = name

        self.results = weakref.WeakKeyDictionary()


class _TestHandler(object):
    def __init__(self):
        self.results = None

    @staticmethod
    def static_handler(sender, original_value, current_value):
        sender.results[sender] = (original_value, current_value)

    @classmethod
    def class_handler(cls, sender, original_value, current_value):
        sender.results[sender] = (original_value, current_value)

    def method_handler(self, sender, original_value, current_value):
        sender.results[sender] = (original_value, current_value)


@pytest.fixture()
def owner_a():
    return _TestOwner('a')


@pytest.fixture()
def owner_b():
    return _TestOwner('b')


@pytest.fixture()
def handler_inst():
    return _TestHandler()


@pytest.fixture()
def handler_func():

    def _handler(sender, original_value, current_value):
        sender.results[sender] = (original_value, current_value)

    return _handler


def test_resource_property_instantiation():
    prop = ResourceProperty()
    assert isinstance(prop, ResourceProperty)


def test_resource_property_get(owner_a, owner_b):
    assert owner_a.value == 'a'
    assert owner_b.value == 'b'


def test_resource_property_set(owner_a, owner_b):
    owner_a.value = 'new_a'
    assert owner_a.value == 'new_a'
    assert owner_b.value == 'b'


class _SubParams(object):
    handler_data =[
        'static_handler',
        'class_handler',
        'method_handler',
        'func_handler'
    ]


@pytest.mark.parametrize('handler_data', _SubParams.handler_data)
def test_resource_property_sub(owner_a, owner_b,
                               handler_inst, handler_func, handler_data):
    handler_name = handler_data

    try:
        handler = getattr(handler_inst, handler_name)
    except AttributeError:
        handler = handler_func

    type(owner_a).value += (owner_a, handler)
    type(owner_b).value += (owner_b, handler)

    owner_a.value = 'foo'
    owner_b.value = 'bar'

    assert owner_a in owner_a.results
    assert owner_b not in owner_a.results
    assert owner_a.results[owner_a] == ('a', 'foo')
    assert owner_b in owner_b.results
    assert owner_a not in owner_b.results
    assert owner_b.results[owner_b] == ('b', 'bar')

    owner_a.results.clear()
    owner_b.results.clear()

    owner_a.value = 'foo'
    owner_b.value = 'bar'

    assert len(owner_a.results) == 0
    assert len(owner_b.results) == 0

    type(owner_a).value -= (owner_a, handler)
    type(owner_b).value -= (owner_b, handler)

    assert len(type(owner_a).value._subscribers) == 0
    assert len(type(owner_b).value._subscribers) == 0
