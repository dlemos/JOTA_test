from rest_framework import serializers

from django.contrib.auth.models import Group

from .models import Subscription, User


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    subscription = SubscriptionSerializer(required=False)
    groups = GroupSerializer(required=False)

    class Meta:
        model = User
        exclude = ['password', 'last_login', 'date_joined', 'user_permissions']

    def create(self, validated_data):
        if "subscription" in validated_data:
            subscription_data = validated_data.pop("subscription")
            verticals_data = subscription_data.pop("verticals")
            subscription, created = Subscription.objects.get_or_create(**subscription_data)
            subscription.verticals.set(verticals_data)
            return User.objects.create(subscription=subscription, **validated_data)

        return User.objects.create(**validated_data)
