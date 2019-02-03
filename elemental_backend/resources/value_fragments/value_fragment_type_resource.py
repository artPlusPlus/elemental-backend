from .._immutable_object_type_resource import ImmutableObjectTypeResource


class ValueFragmentTypeResource(ImmutableObjectTypeResource):
    def __init__(self):
        super(ValueFragmentTypeResource, self).__init__(id=id)

    def _compute(self, previous):
        raise NotImplementedError()
