from tests.fixtures import *


def test_model_unordered_register_and_release(
        model, attribute_type_name, attribute_type_path, attribute_inst_name,
        attribute_inst_path, content_type_base, content_type_sub,
        content_inst_sub, filter_type, filter_instance, sorter_type,
        sorter_instance, view_type, view_instance, view_result):
    """
    Tests registering and releasing interdependent resources.

    The model should tolerate changes to resource existence regardless of
        relationships between resources.
    """
    _all_resources = [
        attribute_type_name,
        attribute_type_path,
        content_type_base,
        content_type_sub,
        filter_type,
        sorter_type,
        view_type,
        attribute_inst_name,
        attribute_inst_path,
        content_inst_sub,
        filter_instance,
        sorter_instance,
        view_instance,
        view_result
    ]

    for resource_idx_offset in range(0, len(_all_resources)):
        for resource_idx in range(0, len(_all_resources)):
            resource_idx += resource_idx_offset % len(_all_resources)
            resource_idx %= len(_all_resources)

            resource = _all_resources[resource_idx]
            model.register_resource(resource)

        retrieved_resources = {}
        for resource_idx in range(0, len(_all_resources)):
            resource_idx += resource_idx_offset % len(_all_resources)
            resource_idx %= len(_all_resources)

            resource = _all_resources[resource_idx]
            retrieved_resources[resource] = model.retrieve_resource(resource.id)

        for src_resource, ret_resource in retrieved_resources.items():
            assert src_resource is ret_resource

        assert attribute_inst_name.type is attribute_type_name
        assert attribute_inst_path.type is attribute_type_path
        assert content_inst_sub.type is content_type_sub
        assert filter_instance.type is filter_type
        assert view_instance.type is view_type

        assert view_result.view_instance is view_instance
        assert content_inst_sub in view_result.content_instances

        for resource_idx in range(0, len(_all_resources)):
            resource_idx += resource_idx_offset % len(_all_resources)
            resource_idx %= len(_all_resources)

            resource = _all_resources[resource_idx]
            model.release_resource(resource.id)

        view_result.content_instance_ids = tuple()

    assert len(model._resources) == 0
    for rc in model._map__resource_cls__resources:
        assert len(model._map__resource_cls__resources[rc]) == 0
    assert len(model._map__resource_type__resource_instances) == 0
    assert len(model._map__attribute_type__filter_types) == 0
    assert len(model._map__attribute_instance__content_instance) == 0
    assert len(model._map__view_type__content_instances) == 0
    assert len(model._map__content_type__view_types) == 0
    assert len(model._map__filter_instance__view_instance) == 0
    assert len(model._map__view_result__view_instance) == 0
