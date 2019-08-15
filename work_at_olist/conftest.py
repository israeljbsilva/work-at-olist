import pytest

from pytest_factoryboy import register

from .factories import CallStartRecordFactory, CallEndRecordFactory


register(CallStartRecordFactory)
register(CallEndRecordFactory)


@pytest.fixture
def customer_client(db):
    from django.test.client import Client
    return Client()
