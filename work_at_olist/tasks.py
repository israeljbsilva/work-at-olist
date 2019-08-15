import sys

from background_task import background

from .models import CallEndRecord, CallStartRecord, TelephoneBill


@background()
def task_calculate_call_price():  # pragma: no cover
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
                pass

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


if 'process_tasks' in sys.argv:  # pragma: no cover
    task_calculate_call_price(verbose_name='task_calculate_call_price')
