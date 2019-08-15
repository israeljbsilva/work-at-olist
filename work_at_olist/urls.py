"""work_at_olist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from rest_framework_nested import routers

from .views import CallStartRecordView


app_name = 'work_at_olist'


call_start_record_router = routers.DefaultRouter(trailing_slash=False)
call_start_record_router.register(r'call-start-record', CallStartRecordView)


urlpatterns = [
    path('', include(call_start_record_router.urls))
]
