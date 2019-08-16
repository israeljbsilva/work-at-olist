import os
import datetime

from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q

from drf_yasg.openapi import Parameter
from drf_yasg.utils import swagger_auto_schema

from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from .models import CallStartRecord, CallEndRecord, TelephoneBill
from .serializers import CallStartRecordSerializer, CallEndRecordSerializer, TelephoneBillSerializer
from .pagination import DefaultPagination
from .utils import validate_phone_number


def ping(request):
    return JsonResponse({
        'request': f'{request.environ.get("REQUEST_METHOD")} '
        f'{request.environ.get("HTTP_HOST")}{request.environ.get("PATH_INFO")}',
        'timestamp': timezone.localtime(),
        'build_date': os.environ.get('BUILD_DATE'),
        'revision': os.environ.get('REVISION')})


class CallStartRecordView(viewsets.ModelViewSet):
    queryset = CallStartRecord.objects.all()
    serializer_class = CallStartRecordSerializer


class CallEndRecordView(viewsets.ModelViewSet):
    queryset = CallEndRecord.objects.all()
    serializer_class = CallEndRecordSerializer


class PhoneBillView(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = TelephoneBill.objects.all()
    serializer_class = TelephoneBillSerializer
    pagination_class = DefaultPagination

    @swagger_auto_schema(
        manual_parameters=[
            Parameter(
                'subscriber_telephone_number',
                'query',
                description='The subscriber telephone number. Ex: 48984359057',
                required=False,
                type='string'
            ),
            Parameter(
                'reference_period',
                'query',
                description='The reference period (month/year). Ex: 08/2019',
                required=False,
                type='string'
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        filters = (Q())
        subscriber_telephone_number = self.request.query_params.get('subscriber_telephone_number')
        if subscriber_telephone_number:
            validate_phone_number(subscriber_telephone_number)
            filters.add(Q(source=subscriber_telephone_number), Q.AND)
        reference_period = self.request.query_params.get('reference_period')
        if reference_period:
            if '/' not in reference_period:
                return Response({'message': 'The reference period is not in the correct format.',
                                'correct_format': '(month/year). Ex: 08/2019'}, HTTP_400_BAD_REQUEST)
            month, year = reference_period.split('/')
            filters.add(Q(call_start_timestamp__month=month, call_start_timestamp__year=year), Q.AND)
        else:
            today = datetime.date.today()
            first_day_month = today.replace(day=1)
            last_month = first_day_month - datetime.timedelta(days=1)
            filters.add(Q(call_start_timestamp__month=last_month.strftime("%m"),
                          call_start_timestamp__year=last_month.strftime("%Y")), Q.AND)
        result_page = self.paginator.paginate_queryset(self.queryset.filter(filters), request)
        serializer = TelephoneBillSerializer(result_page, many=True)
        return self.paginator.get_paginated_response(serializer.data)
