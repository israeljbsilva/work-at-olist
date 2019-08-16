from rest_framework import serializers

from .models import CallStartRecord, CallEndRecord, TelephoneBill
from .utils import validate_phone_number


class CallEndRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = CallEndRecord
        fields = '__all__'
        read_only_fields = ('id', )


class CallStartRecordSerializer(CallEndRecordSerializer, serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = CallStartRecord

    def validate(self, data):
        validate_phone_number(data.get('source'))
        validate_phone_number(data.get('destination'))
        return data


class TelephoneBillSerializer(serializers.ModelSerializer):
    call_start_date = serializers.DateTimeField(format='%d/%m/%Y', source='call_start_timestamp')

    class Meta:
        fields = ('destination', 'call_start_date', 'call_start_time', 'call_duration', 'call_price')
        read_only_fields = ('call_id',)
        model = TelephoneBill
