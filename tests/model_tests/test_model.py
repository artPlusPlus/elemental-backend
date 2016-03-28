from tests.fixtures import *


def test_model_unordered_register_and_release(
        model, attribute_type_name, attribute_type_path, attribute_inst_name,
        attribute_inst_path, content_type_base, content_type_sub,
        content_inst_sub):
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
        content_inst_sub
    ]

    for resource_idx_offset in range(0, len(_all_resources)):
        for resource_idx in range(0, len(_all_resources)):
            resource_idx += resource_idx_offset % len(_all_resources)
            resource_idx %= len(_all_resources)

            resource = _all_resources[resource_idx]
            model.register_resource(resource)

        for resource_idx in range(0, len(_all_resources)):
            resource_idx += resource_idx_offset % len(_all_resources)
            resource_idx %= len(_all_resources)

            resource = _all_resources[resource_idx]
            model.release_resource(resource.id)

    assert len(model._resources) == 0
    for rt in model._map__resource_type__resources:
        assert len(model._map__resource_type__resources[rt]) == 0
    assert len(model._map__content_type__content_instances) == 0
    assert len(model._map__content_instance__attribute_instances) == 0
    assert len(model._map__target_attr__source_attr) == 0
    assert len(model._map__attribute_type__content_type) == 0
    assert len(model._map__attribute_type__attribute_instances) == 0
    assert len(model._map__attribute_instance__content_instance) == 0
