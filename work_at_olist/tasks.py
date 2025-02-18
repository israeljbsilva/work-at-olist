import logging
import sys

from datetime import timedelta

from django.conf import settings

from decimal import Decimal

from background_task import background

from .models import CallEndRecord, CallStartRecord, TelephoneBill


logger = logging.getLogger(__name__)


def save_calculated_phone_bill():
    call_id_start_records = CallStartRecord.objects.values_list('call_id', flat=True)
    call_id_end_records = CallEndRecord.objects.values_list('call_id', flat=True)

    full_calls_id = call_id_start_records.intersection(call_id_end_records)

    if full_calls_id:
        for call_id in full_calls_id:
            if not TelephoneBill.objects.filter(call_id=call_id):
                call_start_record = \
                    [call_start_record for call_start_record in CallStartRecord.objects.filter(call_id=call_id)][0]
                call_end_record = \
                    [call_end_record for call_end_record in CallEndRecord.objects.filter(call_id=call_id)][0]

                call_price, call_duration = calculate_call_price(
                    call_start_record.timestamp, call_end_record.timestamp)

                save_telephone_bill(call_start_record, call_end_record, call_duration, call_price)
            else:
                logger.info('This call has already been calculated.')
    else:
        logger.info('There is no complete call to calculate the call.')


@background()
def task_save_calculated_phone_bill():  # pragma: no cover
    logger.debug('Running Pricing Rules Task.')
    save_calculated_phone_bill()


if 'process_tasks' in sys.argv:  # pragma: no cover
    task_save_calculated_phone_bill(verbose_name='task_pricing_rules')


def save_telephone_bill(call_start_record: CallStartRecord, call_end_record: CallEndRecord,
                        call_duration: timedelta, call_price: Decimal):
    telephone_bill = TelephoneBill(
        call_id=call_start_record.call_id,
        destination=call_start_record.destination,
        call_start_timestamp=call_start_record.timestamp,
        call_end_timestamp=call_end_record.timestamp,
        call_start_time=call_start_record.timestamp.strftime('%H:%M:%S'),
        call_duration=str(call_duration),
        call_price=call_price,
        source=call_start_record.source
    )
    telephone_bill.save(force_insert=True)


def calculate_call_price(timestamp_start: str, timestamp_end: str):
    call_price = 0
    call_duration = timestamp_end - timestamp_start
    time_start = int(timestamp_start.strftime('%H%M'))
    time_end = int(timestamp_end.strftime('%H%M'))
    call_price += settings.FIXED_CHARGES
    standard_time_call_charges = False

    if 600 <= time_start <= 2200:
        standard_time_call_charges = True
        call_duration_in_minutes = int(call_duration.seconds / 60)
        total_standard_time_call_charges = call_duration_in_minutes * settings.STANDARD_TIME_CALL_RATE
        call_price += total_standard_time_call_charges

    if time_end >= 2200 or 0 <= time_end <= 600:
        if standard_time_call_charges:
            call_duration_in_minutes = time_end - 2200
            total_standard_time_call_charges = call_duration_in_minutes * settings.STANDARD_TIME_CALL_RATE
            call_price -= total_standard_time_call_charges

    # if the call is more than one day old, add the full day rate value
    if call_duration.days == 1:
        minutes_full_standard_time_call = 960
        standard_full_day_call_rates = minutes_full_standard_time_call * settings.STANDARD_TIME_CALL_RATE
        call_price += standard_full_day_call_rates

    return Decimal(call_price), call_duration
