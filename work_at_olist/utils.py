from rest_framework import serializers


def validate_phone_number(field):
    if len(field) <= 9 or not field.isdigit():
        raise serializers.ValidationError('Only 10 or 11 numbers. With area code.')
