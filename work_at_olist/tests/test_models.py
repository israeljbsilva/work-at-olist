from decimal import Decimal

import pytest

from work_at_olist.models import CallStartRecord, CallEndRecord, TelephoneBill


pytestmark = [pytest.mark.django_db, pytest.mark.serial]


def test_should_create_call_start_record(call_start_record):
    assert CallStartRecord.objects.count() == 1
    assert call_start_record.id is not None
    assert call_start_record.call_id is not None
    assert call_start_record.source == '99988526423'
    assert call_start_record.destination == '9933468278'


def test_should_create_call_end_record(call_end_record):
    assert CallEndRecord.objects.count() == 1
    assert call_end_record.id is not None
    assert call_end_record.call_id is not None


def test_should_create_telephone_bill(telephone_bill):
    assert TelephoneBill.objects.count() == 1
    assert telephone_bill.call_id is not None
    assert telephone_bill.destination is not None
    assert telephone_bill.call_start_time == '06:00:00'
    assert telephone_bill.call_duration == '0:02:46.956000'
    assert telephone_bill.call_price == Decimal('0.54')
    assert telephone_bill.source == '48984359052'
