import sys

from django.conf import settings

from decimal import Decimal

from background_task import background

from .models import CallEndRecord, CallStartRecord, TelephoneBill


@background()
def task_pricing_rules():  # pragma: no cover
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

                timestamp_start = call_start_record.timestamp
                timestamp_end = call_end_record.timestamp

                call_price, call_duration = _calculate_call_price(timestamp_start, timestamp_end)

                telefone_bill = TelephoneBill(
                    call_id=call_start_record.call_id,
                    destination=call_start_record.destination,
                    call_start_timestamp=call_start_record.timestamp,
                    call_start_time=call_start_record.timestamp.strftime('%H:%M:%S'),
                    call_duration=str(call_duration),
                    call_price=call_price,
                    source=call_start_record.source
                )
                telefone_bill.save(force_insert=True)
            else:
                # This call has already been calculated.
                pass
    else:
        # There is no complete call to calculate the call
        pass


def _calculate_call_price(timestamp_start: str, timestamp_end: str):
    call_price = 0
    call_duration = timestamp_end - timestamp_start
    time_start = int(timestamp_start.strftime('%H%M'))
    call_price += settings.FIXED_CHARGES

    if 600 <= time_start <= 2200:
        call_duration_in_minutes = int(call_duration.seconds / 60)
        total_standard_time_call_charges = call_duration_in_minutes * settings.STANDARD_TIME_CALL_RATE
        call_price += total_standard_time_call_charges

    # if the call is more than one day old, add the full day rate value
    if call_duration.days == 1:
        minutes_full_standard_time_call = 959
        standard_full_day_call_rates = minutes_full_standard_time_call * settings.STANDARD_TIME_CALL_RATE
        call_price += standard_full_day_call_rates

    return Decimal(call_price), call_duration


if 'process_tasks' in sys.argv:  # pragma: no cover
    task_pricing_rules(verbose_name='task_pricing_rules')
