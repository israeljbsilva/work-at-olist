from rest_framework import serializers
from .models import CallStartRecord, CallEndRecord


class CallEndRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = CallEndRecord
        fields = '__all__'
        read_only_fields = 'id'


class CallStartRecordSerializer(CallEndRecordSerializer, serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = CallStartRecord
