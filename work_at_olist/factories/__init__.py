import uuid
import factory

from django.utils import timezone

from work_at_olist.models import CallStartRecord, CallEndRecord


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
