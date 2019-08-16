from rest_framework import serializers
from .models import CallStartRecord, CallEndRecord, TelephoneBill


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
        self._validate_phone_number(data.get('source'))
        self._validate_phone_number(data.get('destination'))
        return data

    @staticmethod
    def _validate_phone_number(field):
        if len(field) <= 9 or not field.isdigit():
            raise serializers.ValidationError('Only 10 or 11 numbers. With area code.')


class TelephoneBillSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        read_only_fields = ('call_id',)
        model = TelephoneBill
