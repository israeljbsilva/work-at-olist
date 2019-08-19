import uuid
from decimal import Decimal

import pytest

from django.utils import timezone

from work_at_olist.serializers import TelephoneBillSerializer


pytestmark = [pytest.mark.django_db, pytest.mark.serial]


def test_should_serialize_telephone_bill(telephone_bill):
    # GIVEN
    # WHEN
    serializer = TelephoneBillSerializer(telephone_bill)

    # THEN
    assert isinstance(serializer.data, dict)
    assert serializer.data.get('destination') == '48984359051'
    assert serializer.data.get('call_start_time') == '06:00:00'
    assert serializer.data.get('call_duration') == '0:02:46.956000'
    assert serializer.data.get('call_price') == '0.54'


def test_should_deserialize_telephone_bill():
    # GIVEN
    call_id = uuid.uuid4()
    telephone_bill_data = {
        'call_id': call_id,
        'destination': '48984359051',
        'call_start_date': timezone.now(),
        'call_start_time': '06:00:00',
        'call_duration': '0:02:46.956000',
        'call_price': '0.54',
    }

    # WHEN
    serializer = TelephoneBillSerializer(data=telephone_bill_data)

    # THEN
    assert serializer.is_valid()

    telephone_bill = serializer.validated_data
    assert telephone_bill['destination'] == '48984359051'
    assert telephone_bill['call_start_time'] == '06:00:00'
    assert telephone_bill['call_duration'] == '0:02:46.956000'
    assert telephone_bill['call_price'] == Decimal('0.54')
