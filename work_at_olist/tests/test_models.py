import pytest

from work_at_olist.models import CallStartRecord, CallEndRecord
from work_at_olist.enums import CallRecordType


pytestmark = [pytest.mark.django_db, pytest.mark.serial]


def test_should_create_call_start_record(call_start_record):
    assert CallStartRecord.objects.count() == 1
    assert call_start_record.id is not None
    assert call_start_record.type == CallRecordType.start
    assert call_start_record.call_id is not None
    assert call_start_record.source == '99988526423'
    assert call_start_record.destination == '9933468278'


def test_should_create_call_end_record(call_end_record):
    assert CallEndRecord.objects.count() == 1
    assert call_end_record.id is not None
    assert call_end_record.type == CallRecordType.end
    assert call_end_record.call_id is not None
