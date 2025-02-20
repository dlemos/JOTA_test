from django.db.models import Q
from django.contrib.auth.models import Group

from rest_framework import viewsets
from rest_framework import permissions

from main.models import Subscription

from .models import News
from .serializers import NewsSerializer


class NewsViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = NewsSerializer

    def get_queryset(self):
        queryset = News.objects.all()
        if self.request.user.is_superuser:
            return queryset

        if self.request.user.groups.contains(Group.objects.get(name="Editor")):
            return queryset.filter(author=self.request.user)

        # Next cases can only see published News
        queryset = queryset.filter(status=News.Status.PUBLISHED)

        if (not self.request.user.is_anonymous
                and self.request.user.has_subscription()
                and self.request.user.subscription.plan == Subscription.Plans.JOTA_PRO):
            return queryset.filter(
                Q(is_pro_only=False) |
                ((Q(is_pro_only=True) & Q(category__in=self.request.user.subscription.verticals.all())))
            )

        return queryset.filter(is_pro_only=False)
