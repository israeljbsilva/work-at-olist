import sys

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

                _calculate_call_price(timestamp_start, timestamp_end)


                #  realizar o calculo

                # salvar
                '''telefone_bill = TelephoneBill(
                    call_id=call_start_record.call_id,
                    destination=call_start_record.destination, 
                    call_start_date=call_start_record.timestamp,
                    call_start_time=call_start_record.timestamp,
                    call_duration='',
                    call_price='',
                    source=call_start_record.source
                )'''
            else:
                # Essa chamada já foi calculada
                pass
    else:
        # Não existe nenhuma ligação completa para realizar o calculo da chamada
        pass


def _calculate_call_price(timestamp_start: str, timestamp_end: str) -> Decimal:
    dt = timestamp_start - timestamp_end
    print(dt)


if 'process_tasks' in sys.argv:  # pragma: no cover
    task_pricing_rules(verbose_name='task_pricing_rules')
