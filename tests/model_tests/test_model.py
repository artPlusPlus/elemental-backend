from tests.fixtures import *


def test_model_unordered_register_and_release(
        model, attribute_type_name, attribute_type_path, attribute_inst_name,
        attribute_inst_path, content_type_base, content_type_sub,
        content_inst_sub, filter_type, filter_instance, view_type,
        view_instance):
    """
    Tests registering and releasing interdependent resources.

    The model should tolerate changes to resource existence regardless of
        relationships between resources.
    """
    _all_resources = [
        attribute_type_name,
        attribute_type_path,
        attribute_inst_name,
        attribute_inst_path,
        content_type_base,
        content_type_sub,
        content_inst_sub,
        filter_type,
        filter_instance,
        view_type,
        view_instance
    ]

    for resource_idx_offset in range(0, len(_all_resources)):
        for resource_idx in range(0, len(_all_resources)):
            resource_idx += resource_idx_offset % len(_all_resources)
            resource_idx %= len(_all_resources)

            resource = _all_resources[resource_idx]
            model.register_resource(resource)

        assert attribute_inst_name.attribute_type is attribute_type_name
        assert attribute_inst_path.attribute_type is attribute_type_path
        assert content_inst_sub.id in view_instance.content_instances

        for resource_idx in range(0, len(_all_resources)):
            resource_idx += resource_idx_offset % len(_all_resources)
            resource_idx %= len(_all_resources)

            resource = _all_resources[resource_idx]
            model.release_resource(resource.id)

    assert len(model._resources) == 0
    for rc in model._map__resource_class__resources:
        assert len(model._map__resource_class__resources[rc]) == 0
    assert len(model._map__resource_type__resource_instances) == 0
    assert len(model._map__target_attr__source_attr) == 0
    assert len(model._map__attribute_type__content_type) == 0
    assert len(model._map__attribute_type__filter_types) == 0
    assert len(model._map__attribute_instance__content_instance) == 0
    assert len(model._map__view_type__content_instances) == 0
    assert len(model._map__view_instance__content_instances) == 0
    assert len(model._map__content_type__view_types) == 0
    assert len(model._map__filter_instance__view_instance) == 0
