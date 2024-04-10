from rest_framework.viewsets import ReadOnlyModelViewSet

from api.v1.services import serializers
from services.models import Subscription


class SubscriptionViewSet(ReadOnlyModelViewSet):
    """"""

    queryset = Subscription.objects.all()
    serializer_class = serializers.SubscriptionSerializer
