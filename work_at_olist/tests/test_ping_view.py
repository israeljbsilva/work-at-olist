import json
from http import HTTPStatus


def test_should_ping(customer_client):
    # GIVEN
    # WHEN
    response = customer_client.get('/ping')

    # THEN
    assert response.status_code == HTTPStatus.OK

    content = json.loads(response.content.decode())
    assert set(content.keys()) == {'request', 'timestamp', 'build_date', 'revision'}
