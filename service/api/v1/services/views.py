from django.conf import settings
from django.core.cache import cache
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

        price_cache = cache.get(settings.PRICE_CACHE_NAME)

        if price_cache:
            total_price = price_cache
        else:
            total_price = queryset.aggregate(
                total=Sum('price')
            ).get('total')
            cache.set(settings.PRICE_CACHE_NAME, total_price, 60 * 60)

        response_data = {'result': response.data}
        response_data['total_amount'] = total_price
        response.data = response_data
        return response
