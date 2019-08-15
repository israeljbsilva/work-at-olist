import json
import uuid

from http import HTTPStatus

from django.utils import timezone


RESOURCE_PATH = '/api/v1'


def test_should_create_call_end_record(customer_client):
    # GIVEN
    call_id = uuid.uuid4()
    call_end_record_data = {
        'call_id': str(call_id),
        'timestamp': str(timezone.now())
    }

    # WHEN
    response = customer_client.post(
        f'{RESOURCE_PATH}/call-end-record', data=json.dumps(call_end_record_data), content_type='application/json')

    # THEN
    assert response.status_code == HTTPStatus.CREATED

    content = json.loads(response.content.decode())
    assert content.get('id') is not None
    assert content.get('call_id') == str(call_id)


def test_should_not_create_call_end_record(customer_client):
    # GIVEN
    call_end_record_data = {}

    # WHEN
    response = customer_client.post(
        f'{RESOURCE_PATH}/call-end-record', data=json.dumps(call_end_record_data), content_type='application/json')

    # THEN
    assert response.status_code == HTTPStatus.BAD_REQUEST

    content = json.loads(response.content.decode())
    assert content == {
        'timestamp': ['Este campo é obrigatório.'],
        'call_id': ['Este campo é obrigatório.']
    }
