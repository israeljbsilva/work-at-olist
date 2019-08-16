import uuid
import factory

from django.utils import timezone

from decimal import Decimal

from work_at_olist.models import CallStartRecord, CallEndRecord, TelephoneBill


class CallStartRecordFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CallStartRecord

    id = uuid.uuid4()
    timestamp = timezone.now()
    call_id = uuid.uuid4()
    source = '99988526423'
    destination = '9933468278'


class CallEndRecordFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CallEndRecord

    id = uuid.uuid4()
    timestamp = timezone.now()
    call_id = uuid.uuid4()


class TelephoneBillFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TelephoneBill

    call_id = uuid.uuid4()
    destination = '48984359051'
    call_start_timestamp = timezone.now()
    call_start_time = '06:00:00'
    call_duration = '0:02:46.956000'
    call_price = Decimal('0.54')
    source = '48984359052'
