import uuid

from django.db import models
from django.db.models.fields import CharField, UUIDField

from .enums import CallRecordType


class AbstractCallRecord(models.Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4, serialize=False, editable=False, unique=True)
    type = CharField('TYPE', max_length=3, choices=CallRecordType.choices, default=CallRecordType.end)
    timestamp = models.DateTimeField('TIMESTAMP', null=False)
    call_id = UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True


class CallEndRecord(AbstractCallRecord, models.Model):

    class Meta:
        db_table = 'CallEndRecord'
        verbose_name = 'call_end_record'
        verbose_name_plural = 'call_end_records'


class CallStartRecord(AbstractCallRecord, models.Model):
    type = CharField('TYPE', max_length=4, choices=CallRecordType.choices, default=CallRecordType.start)
    source = CharField('SOURCE', max_length=11, null=False)
    destination = CharField('DESTINATION', max_length=11, null=False)

    class Meta:
        db_table = 'CallStartRecord'
        verbose_name = 'call_start_record'
        verbose_name_plural = 'call_start_records'
