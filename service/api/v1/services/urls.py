from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.v1.services.views import SubscriptionViewSet

router = DefaultRouter()

router.register(r'subscription', SubscriptionViewSet, basename='subscription')

urlpatterns = [
    path('', include(router.urls)),
]
