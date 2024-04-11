from rest_framework import serializers

from services.models import Plan, Subscription


class PlanSerializer(serializers.ModelSerializer):
    """Тарифный план."""

    class Meta:
        model = Plan
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    """Подписка."""

    plan = PlanSerializer()
    client_name = serializers.CharField(source='client.company_name')
    email = serializers.CharField(source='client.user.email')
    price = serializers.SerializerMethodField()

    def get_price(self, instance):
        """Получает стоимость подписки из annotate."""
        return instance.price

    class Meta:
        model = Subscription
        fields = ('id', 'plan_id', 'client_name', 'email', 'plan', 'price')
