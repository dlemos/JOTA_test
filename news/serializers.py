from rest_framework import serializers, parsers

from .models import News, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class NewsSerializer(serializers.ModelSerializer):
    parser_classes = [parsers.MultiPartParser, parsers.JSONParser]

    image = serializers.ImageField(required=False)

    class Meta:
        model = News
        fields = '__all__'
