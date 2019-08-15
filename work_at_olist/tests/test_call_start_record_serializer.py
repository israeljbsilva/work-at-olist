import uuid
import pytest

from django.utils import timezone

from work_at_olist.serializers import CallStartRecordSerializer


pytestmark = [pytest.mark.django_db, pytest.mark.serial]


def test_should_serialize_call_start_record(call_start_record):
    # GIVEN
    # WHEN
    serializer = CallStartRecordSerializer(call_start_record)

    # THEN
    assert isinstance(serializer.data, dict)
    assert serializer.data.get('id') is not None
    assert serializer.data.get('call_id') is not None
    assert serializer.data.get('source') == '99988526423'
    assert serializer.data.get('destination') == '9933468278'


def test_should_deserialize_call_start_record():
    # GIVEN
    call_start_record_id = uuid.uuid4()
    call_id = uuid.uuid4()
    call_start_record_data = {
        'id': call_start_record_id,
        'call_id': call_id,
        'timestamp': timezone.now(),
        'source': '99988526423',
        'destination': '9933468278'
    }

    # WHEN
    serializer = CallStartRecordSerializer(data=call_start_record_data)

    # THEN
    assert serializer.is_valid()

    call_start_record = serializer.save(id=call_start_record_id)
    assert call_start_record.id == call_start_record_id
    assert call_start_record.call_id == call_id
    assert call_start_record.source == '99988526423'
    assert call_start_record.destination == '9933468278'
