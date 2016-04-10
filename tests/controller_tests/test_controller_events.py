import json
import uuid

import elemental_backend as backend

from tests.fixtures import *
from tests import resource_data


class _PostEventParams(object):
    event_data = [
        (  # No Deserializer
            backend.transactions.Actions.POST,
            {
                'resource_type': None,
                'resource_id': None,
                'super_id': None,
                'inbound_format': None,
                'inbound_payload': None,
                'outbound_format': None
            },
            (
                backend.ControllerEvents.transaction_opened,
                backend.ControllerEvents.resource_not_created,
                backend.ControllerEvents.transaction_failed,
                backend.ControllerEvents.transaction_closing
            )
        ),
        (  # No Resource Type
            backend.transactions.Actions.POST,
            {
                'resource_type': None,
                'resource_id': None,
                'super_id': None,
                'inbound_format': 'json',
                'inbound_payload': None,
                'outbound_format': None
            },
            (
                backend.ControllerEvents.transaction_opened,
                backend.ControllerEvents.resource_not_created,
                backend.ControllerEvents.transaction_failed,
                backend.ControllerEvents.transaction_closing
            )
        ),
        (  # Invalid Inbound Format
            backend.transactions.Actions.POST,
            {
                'resource_type': backend.resources.ContentType,
                'resource_id': None,
                'super_id': None,
                'inbound_format': 'foormat',
                'inbound_payload': '',
                'outbound_format': None
            },
            (
                backend.ControllerEvents.transaction_opened,
                backend.ControllerEvents.transaction_failed,
                backend.ControllerEvents.transaction_closing
            )
        ),
        (  # No Resource Data
            backend.transactions.Actions.POST,
            {
                'resource_type': backend.resources.ContentType,
                'resource_id': None,
                'super_id': None,
                'inbound_format': 'json',
                'inbound_payload': '',
                'outbound_format': None
            },
            (
                backend.ControllerEvents.transaction_opened,
                backend.ControllerEvents.resource_created,
                backend.ControllerEvents.resource_not_updated,
                backend.ControllerEvents.transaction_failed,
                backend.ControllerEvents.transaction_closing
            )
        ),
        (  # Success
            backend.transactions.Actions.POST,
            {
                'resource_type': backend.resources.ContentType,
                'resource_id': None,
                'super_id': None,
                'inbound_format': 'json',
                'inbound_payload': json.dumps(resource_data.DATA_CONTENT_TYPE_BASE),
                'outbound_format': None
            },
            (
                backend.ControllerEvents.transaction_opened,
                backend.ControllerEvents.resource_created,
                backend.ControllerEvents.resource_updated,
                backend.ControllerEvents.resource_registered,
                backend.ControllerEvents.transaction_succeeded,
                backend.ControllerEvents.transaction_closing
            )
        ),
    ]


@pytest.mark.parametrize('event_data', _PostEventParams.event_data)
def test_post_events(controller_json, event_data):
    _test_events_helper(controller_json, event_data)


class _GetEventParams(object):
    event_data = [
        (  # No Resource Id
            backend.transactions.Actions.GET,
            {
                'resource_type': None,
                'resource_id': None,
                'super_id': None,
                'inbound_format': None,
                'inbound_payload': None,
                'outbound_format': None
            },
            (
                backend.ControllerEvents.transaction_opened,
                backend.ControllerEvents.resource_not_resolved,
                backend.ControllerEvents.transaction_failed,
                backend.ControllerEvents.transaction_closing
            )
        ),
        (  # Success
            backend.transactions.Actions.GET,
            {
                'resource_type': None,
                'resource_id': resource_data.DATA_CONTENT_TYPE_BASE['id'],
                'super_id': None,
                'inbound_format': None,
                'inbound_payload': None,
                'outbound_format': None
            },
            (
                backend.ControllerEvents.transaction_opened,
                backend.ControllerEvents.resource_resolved,
                backend.ControllerEvents.transaction_succeeded,
                backend.ControllerEvents.transaction_closing
            )
        ),
    ]


@pytest.mark.parametrize('event_data', _GetEventParams.event_data)
def test_get_events(controller_json, event_data):
    _test_events_helper(controller_json, event_data)


class _PutEventParams(object):
    event_data = [
        (  # No Resource Id
            backend.transactions.Actions.PUT,
            {
                'resource_type': None,
                'resource_id': None,
                'super_id': None,
                'inbound_format': None,
                'inbound_payload': None,
                'outbound_format': None
            },
            (
                backend.ControllerEvents.transaction_opened,
                backend.ControllerEvents.resource_not_resolved,
                backend.ControllerEvents.transaction_failed,
                backend.ControllerEvents.transaction_closing
            )
        ),
        (  # No Inbound Format
            backend.transactions.Actions.PUT,
            {
                'resource_type': None,
                'resource_id': resource_data.DATA_CONTENT_TYPE_BASE['id'],
                'super_id': None,
                'inbound_format': None,
                'inbound_payload': None,
                'outbound_format': None
            },
            (
                backend.ControllerEvents.transaction_opened,
                backend.ControllerEvents.resource_resolved,
                backend.ControllerEvents.resource_not_updated,
                backend.ControllerEvents.transaction_failed,
                backend.ControllerEvents.transaction_closing
            )
        ),
        (  # Invalid Outbound Format
            backend.transactions.Actions.PUT,
            {
                'resource_type': None,
                'resource_id': resource_data.DATA_CONTENT_TYPE_BASE['id'],
                'super_id': None,
                'inbound_format': 'json',
                'inbound_payload': None,
                'outbound_format': 'foormat'
            },
            (
                backend.ControllerEvents.transaction_opened,
                backend.ControllerEvents.resource_resolved,
                backend.ControllerEvents.transaction_failed,
                backend.ControllerEvents.transaction_closing
            )
        ),
        (  # No Inbound Payload
            backend.transactions.Actions.PUT,
            {
                'resource_type': None,
                'resource_id': resource_data.DATA_CONTENT_TYPE_BASE['id'],
                'super_id': None,
                'inbound_format': 'json',
                'inbound_payload': None,
                'outbound_format': None
            },
            (
                backend.ControllerEvents.transaction_opened,
                backend.ControllerEvents.resource_resolved,
                backend.ControllerEvents.resource_not_updated,
                backend.ControllerEvents.transaction_failed,
                backend.ControllerEvents.transaction_closing
            )
        ),
        (  # Success
            backend.transactions.Actions.PUT,
            {
                'resource_type': None,
                'resource_id': resource_data.DATA_CONTENT_TYPE_BASE['id'],
                'super_id': None,
                'inbound_format': 'json',
                'inbound_payload': json.dumps(resource_data.DATA_CONTENT_TYPE_BASE),
                'outbound_format': None
            },
            (
                backend.ControllerEvents.transaction_opened,
                backend.ControllerEvents.resource_resolved,
                backend.ControllerEvents.resource_updated,
                backend.ControllerEvents.transaction_succeeded,
                backend.ControllerEvents.transaction_closing
            )
        )
    ]


@pytest.mark.parametrize('event_data', _PutEventParams.event_data)
def test_put_events(controller_json, event_data):
    _test_events_helper(controller_json, event_data)


class _DeleteEventParams(object):
    event_data = [
        (  # No Resource Id
            backend.transactions.Actions.DELETE,
            {
                'resource_type': None,
                'resource_id': None,
                'super_id': None,
                'inbound_format': None,
                'inbound_payload': None,
                'outbound_format': None
            },
            (
                backend.ControllerEvents.transaction_opened,
                backend.ControllerEvents.resource_not_resolved,
                backend.ControllerEvents.transaction_failed,
                backend.ControllerEvents.transaction_closing
            )
        ),
        (  # Invalid Outbound Format
            backend.transactions.Actions.DELETE,
            {
                'resource_type': None,
                'resource_id': resource_data.DATA_CONTENT_TYPE_BASE['id'],
                'super_id': None,
                'inbound_format': None,
                'inbound_payload': None,
                'outbound_format': 'foormat'
            },
            (
                backend.ControllerEvents.transaction_opened,
                backend.ControllerEvents.resource_resolved,
                backend.ControllerEvents.transaction_failed,
                backend.ControllerEvents.transaction_closing
            )
        ),
        (  # Success
            backend.transactions.Actions.DELETE,
            {
                'resource_type': None,
                'resource_id': resource_data.DATA_CONTENT_TYPE_BASE['id'],
                'super_id': None,
                'inbound_format': None,
                'inbound_payload': None,
                'outbound_format': None
            },
            (
                backend.ControllerEvents.transaction_opened,
                backend.ControllerEvents.resource_resolved,
                backend.ControllerEvents.resource_deleted,
                backend.ControllerEvents.transaction_succeeded,
                backend.ControllerEvents.transaction_closing
            )
        )
    ]


@pytest.mark.parametrize('event_data', _DeleteEventParams.event_data)
def test_delete_events(controller_json, event_data):
    _test_events_helper(controller_json, event_data)


def _test_events_helper(controller_json, event_data):
    transaction_action, transaction_data, target_events = event_data

    handlers = []
    fired_events = []
    for event in backend.ControllerEvents:
        def handler(e, t):
            fired_events.append(e)

        handlers.append(handler)
        controller_json.handler(event)(handler)

    transaction = backend.transactions.Transaction(transaction_action,
                                                   **transaction_data)
    controller_json.process_transaction(transaction)

    assert tuple(fired_events) == target_events
