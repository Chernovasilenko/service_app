from django.db.models import Prefetch, Sum
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.v1.services import serializers
from clients.models import Client
from services.models import Subscription

HUNDRED_PERCENT = 100.0


class SubscriptionViewSet(ReadOnlyModelViewSet):
    """Вьюсет подписки."""

    queryset = Subscription.objects.all().prefetch_related(
        'plan',
        Prefetch(
            'client',
            queryset=Client.objects.all().select_related('user').only(
                'company_name', 'user__email'
            )
        )
    )
    serializer_class = serializers.SubscriptionSerializer

    def list(self, request, *args, **kwargs):
        """Добавляет суммарную оплату подписок."""
        queryset = self.filter_queryset(self.get_queryset())
        response = super().list(self, request, *args, **kwargs)
        response_data = {'result': response.data}
        response_data['total_amount'] = queryset.aggregate(
            total=Sum('price')
        ).get('total')
        response.data = response_data
        return response
