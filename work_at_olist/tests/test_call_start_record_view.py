import json
import uuid

from http import HTTPStatus

from django.utils import timezone


RESOURCE_PATH = '/api/v1'


def test_should_create_call_start_record(customer_client):
    # GIVEN
    call_id = uuid.uuid4()
    call_start_record_data = {
        'call_id': str(call_id),
        'timestamp': str(timezone.now()),
        'source': '99988526423',
        'destination': '9933468278'
    }

    # WHEN
    response = customer_client.post(
        f'{RESOURCE_PATH}/call-start-record', data=json.dumps(call_start_record_data), content_type='application/json')

    # THEN
    assert response.status_code == HTTPStatus.CREATED

    content = json.loads(response.content.decode())
    assert content.get('id') is not None
    assert content.get('call_id') == str(call_id)
    assert content.get('source') == '99988526423'
    assert content.get('destination') == '9933468278'


def test_should_not_create_call_start_record(customer_client):
    # GIVEN
    call_start_record_data = {}

    # WHEN
    response = customer_client.post(
        f'{RESOURCE_PATH}/call-start-record', data=json.dumps(call_start_record_data), content_type='application/json')

    # THEN
    assert response.status_code == HTTPStatus.BAD_REQUEST

    content = json.loads(response.content.decode())
    assert content == {
        'timestamp': ['Este campo é obrigatório.'],
        'call_id': ['Este campo é obrigatório.'],
        'source': ['Este campo é obrigatório.'],
        'destination': ['Este campo é obrigatório.']
    }


def test_should_not_create_call_start_record_with_phone_number_less_than_or_equal_to_9(customer_client):
    # GIVEN
    call_id = uuid.uuid4()
    call_start_record_data = {
        'call_id': str(call_id),
        'timestamp': str(timezone.now()),
        'source': '988526423',
        'destination': '33468278'
    }

    # WHEN
    response = customer_client.post(
        f'{RESOURCE_PATH}/call-start-record', data=json.dumps(call_start_record_data), content_type='application/json')

    # THEN
    assert response.status_code == HTTPStatus.BAD_REQUEST

    content = json.loads(response.content.decode())
    assert content == {
        "non_field_errors": [
            "Only 10 or 11 numbers. With area code."
        ]
    }
