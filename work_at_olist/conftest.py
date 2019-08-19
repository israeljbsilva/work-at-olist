import datetime
import uuid
import pytest

from decimal import Decimal

from pytest_factoryboy import register

from .factories import CallStartRecordFactory, CallEndRecordFactory, TelephoneBillFactory


register(CallStartRecordFactory)
register(CallEndRecordFactory)
register(TelephoneBillFactory)


@pytest.fixture
def customer_client(db):
    from django.test.client import Client
    return Client()


@pytest.fixture
def telephone_bill_previous_month():
    today = datetime.date.today()
    first_day_month = today.replace(day=1)
    last_month = first_day_month - datetime.timedelta(days=1)
    return TelephoneBillFactory(
        call_id=uuid.uuid4(), destination='48984359051', call_start_timestamp=last_month,
        call_end_timestamp=last_month, call_start_time='06:00:00', call_duration='0:02:46.956000',
        call_price=Decimal('0.54'), source='48984359052')
