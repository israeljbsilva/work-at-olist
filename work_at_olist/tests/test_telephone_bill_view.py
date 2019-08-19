import json

from http import HTTPStatus


RESOURCE_PATH = '/api/v1'


def test_should_list_telephone_bill_from_the_previous_month(customer_client, telephone_bill_previous_month):
    # GIVEN
    # WHEN
    response = customer_client.get(
        f'{RESOURCE_PATH}/phone-bill?subscriber_telephone_number={telephone_bill_previous_month.source}')

    # THEN
    assert response.status_code == HTTPStatus.OK

    content = json.loads(response.content.decode())['results'][0]
    assert content.get('destination') == telephone_bill_previous_month.destination
    assert content.get('call_start_date') == telephone_bill_previous_month.call_start_timestamp.strftime('%d/%m/%Y')
    assert content.get('call_start_time') == telephone_bill_previous_month.call_start_time
    assert content.get('call_duration') == telephone_bill_previous_month.call_duration
    assert content.get('call_price') == str(telephone_bill_previous_month.call_price)


def test_should_list_telephone_bill_with_reference_period_completed(customer_client, telephone_bill):
    # GIVEN
    # WHEN
    response = customer_client.get(
        f'{RESOURCE_PATH}/phone-bill?subscriber_telephone_number={telephone_bill.source}'
        f'&reference_period={telephone_bill.call_start_timestamp.strftime("%m/%Y")}')

    # THEN
    assert response.status_code == HTTPStatus.OK

    content = json.loads(response.content.decode())['results'][0]
    assert content.get('destination') == telephone_bill.destination
    assert content.get('call_start_date') == telephone_bill.call_start_timestamp.strftime('%d/%m/%Y')
    assert content.get('call_start_time') == telephone_bill.call_start_time
    assert content.get('call_duration') == telephone_bill.call_duration
    assert content.get('call_price') == str(telephone_bill.call_price)


def test_should_not_list_telephone_bill_with_incorrect_reference_period_format(customer_client, telephone_bill):
    # GIVEN
    # WHEN
    response = customer_client.get(
        f'{RESOURCE_PATH}/phone-bill?subscriber_telephone_number={telephone_bill.source}'
        f'&reference_period=082019')

    # THEN
    assert response.status_code == HTTPStatus.BAD_REQUEST

    content = json.loads(response.content.decode())
    assert content == {
        'message': 'The reference period is not in the correct format.',
        'correct_format': '(month/year). Ex: 08/2019'
    }
