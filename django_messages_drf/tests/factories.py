from django.contrib.auth import get_user_model

import factory

import django_messages_drf.models


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda n: "testes-%s" % n)
    password = factory.PostGenerationMethodCall('set_password', 'testes')
    first_name = "Test"
    last_name = 'User'
    email = factory.LazyAttribute(lambda u: "%s@testes.example.com" % u.username)

    class Meta:
        model = get_user_model()


class ThreadFactory(factory.django.DjangoModelFactory):
    subject = factory.LazyAttribute(lambda n: "This is a thread %s" % n)

    class Meta:
        model = django_messages_drf.models.Thread


class UserThreadFactory(factory.django.DjangoModelFactory):
    thread = factory.SubFactory(ThreadFactory)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = django_messages_drf.models.UserThread


class MessageFactory(factory.django.DjangoModelFactory):
    thread = factory.SubFactory(ThreadFactory)

    sender = factory.SubFactory(UserFactory)
    content = factory.LazyAttribute(lambda n: "this is a content %s" % n)

    class Meta:
        model = django_messages_drf.models.Message
