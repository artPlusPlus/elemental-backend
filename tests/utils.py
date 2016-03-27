import pytest

import elemental_backend as backend


def register_resource(model, resource, *errors_expected):
    collision_error = backend.errors.ResourceCollisionError
    if resource.id in model._resources and collision_error not in errors_expected:
        # pytest Parameterization can cause an unexpected ResourceCollisionError.
        # If an ID already exists in model._resources, but a ResourceCollisionError
        # is not expected, bail.
        return

    result = _invoke_model(model.register_resource,
                           resource, errors_expected)
    return result


def retrieve_resource(model, resource_id, *errors_expected):
    result = _invoke_model(model.retrieve_resource,
                           resource_id, errors_expected)
    return result


def release_resource(model, resource_id, *errors_expected):
    result = _invoke_model(model.release_resource,
                           resource_id, errors_expected)
    return result


def _invoke_model(model_func, model_value, errors_expected):
    result = None
    errors_expected = tuple([e for e in errors_expected if e])

    if errors_expected:
        with pytest.raises(errors_expected):
            model_func(model_value)
    else:
        result = model_func(model_value)

    return result
