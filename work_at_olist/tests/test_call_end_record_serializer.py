import uuid
import pytest

from django.utils import timezone

from work_at_olist.serializers import CallEndRecordSerializer


pytestmark = [pytest.mark.django_db, pytest.mark.serial]


def test_should_serialize_call_end_record(call_end_record):
    # GIVEN
    # WHEN
    serializer = CallEndRecordSerializer(call_end_record)

    # THEN
    assert isinstance(serializer.data, dict)
    assert serializer.data.get('id') is not None
    assert serializer.data.get('call_id') is not None


def test_should_deserialize_call_end_record():
    # GIVEN
    call_end_record_id = uuid.uuid4()
    call_id = uuid.uuid4()
    call_end_record_data = {
        'id': call_end_record_id,
        'call_id': call_id,
        'timestamp': timezone.now()
    }

    # WHEN
    serializer = CallEndRecordSerializer(data=call_end_record_data)

    # THEN
    assert serializer.is_valid()

    call_end_record = serializer.save(id=call_end_record_id)
    assert call_end_record.id == call_end_record_id
    assert call_end_record.call_id == call_id
