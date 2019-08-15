import pytest

from pytest_factoryboy import register

from .factories import CallStartRecordFactory, CallEndRecordFactory

from config.celery_app import create_app


register(CallStartRecordFactory)
register(CallEndRecordFactory)


@pytest.fixture
def customer_client(db):
    from django.test.client import Client
    return Client()


@pytest.fixture(autouse=True)
def celery():
    app = create_app()
    return app
