import os

from django.http import JsonResponse
from django.utils import timezone

from rest_framework import viewsets, mixins

from .models import CallStartRecord, CallEndRecord, TelephoneBill
from .serializers import CallStartRecordSerializer, CallEndRecordSerializer, TelephoneBillSerializer


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

    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)
