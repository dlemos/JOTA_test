from rest_framework import serializers

from .models import Subscription, User


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    subscription = SubscriptionSerializer()

    class Meta:
        model = User
        exclude = ['password', 'last_login', 'date_joined']
