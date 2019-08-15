import uuid

from django.db import models
from django.db.models.fields import CharField, UUIDField

from decimal import Decimal


class AbstractCallRecord(models.Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4, serialize=False, editable=False, unique=True)
    timestamp = models.DateTimeField('TIMESTAMP', null=False)
    call_id = UUIDField('CALL_ID', unique=True, null=False)

    class Meta:
        abstract = True


class CallEndRecord(AbstractCallRecord, models.Model):

    class Meta:
        db_table = 'CallEndRecord'
        verbose_name = 'call_end_record'
        verbose_name_plural = 'call_end_records'


class CallStartRecord(AbstractCallRecord, models.Model):
    source = CharField('SOURCE', max_length=11, null=False)
    destination = CharField('DESTINATION', max_length=11, null=False)

    class Meta:
        db_table = 'CallStartRecord'
        verbose_name = 'call_start_record'
        verbose_name_plural = 'call_start_records'


class TelephoneBill(models.Model):
    call_id = UUIDField(primary_key=True, default=uuid.uuid4, serialize=False, editable=False, unique=True)
    destination = CharField('DESTINATION', max_length=11, null=False)
    call_start_date = models.DateTimeField('CALL_START_DATE', null=False)
    call_start_time = models.TimeField('CALL_START_TIME', null=False)
    call_duration = models.TimeField('CALL_DURATION', null=False)
    call_price = models.DecimalField(decimal_places=2, max_digits=17, default=Decimal("0.0"))
    source = CharField('SOURCE', max_length=11, null=False)

    class Meta:
        db_table = 'TelephoneBill'
        verbose_name = 'telephone_bill'
        verbose_name_plural = 'telephone_bills'
