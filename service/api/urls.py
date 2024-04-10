from django.urls import include, path

from django.conf import settings

app_name = 'api'

urlpatterns = [
    path('v1/', include('api.v1.urls')),
]