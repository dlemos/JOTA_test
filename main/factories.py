import factory

from django.contrib.auth.models import Group

from .models import User, Subscription


class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Group


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User


class EditorFactory(UserFactory):
    # This should work but I keep getting:
    # "RuntimeError: Database access not allowed, use the "django_db" mark, or the "db" or
    # "transactional_db" fixtures to enable it."
    #
    # group = GroupFactory(name="Editor")
    pass


class SubscriptionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Subscription

    @factory.post_generation
    def verticals(self, create, extracted, **kwargs):
        if not create or not extracted:
            # Simple build, or nothing to add, do nothing.
            return

        # Add the iterable of groups using bulk addition
        self.verticals.add(*extracted)


class ProUserFactory(UserFactory):
    subscription = factory.SubFactory(SubscriptionFactory, plan=Subscription.Plans.JOTA_PRO)
