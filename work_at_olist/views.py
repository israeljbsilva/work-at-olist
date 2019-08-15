import os

from django.http import JsonResponse
from django.utils import timezone

from rest_framework import viewsets

from .models import CallStartRecord
from .serializers import CallStartRecordSerializer


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
