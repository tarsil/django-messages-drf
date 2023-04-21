---
title: Django Messages DRF

language_tabs: # must be one of https://github.com/rouge-ruby/rouge/wiki/List-of-supported-languages-and-lexers
  - python

toc_footers:
  - <a target='_blank' href='https://github.com/docuowl/docuowl/issues/new'>Can we improve it? Tell us</a>

includes:
  - errors

search: true

code_clipboard: true

meta:
  - name: description
    content: Documentation for the Django Messages DRF API
---

# Introduction

[![CircleCi](https://img.shields.io/circleci/project/github/tarsil/django-messages-drf.svg)](https://circleci.com/gh/tarsil/django-messages-drf)
[![codecov](https://codecov.io/gh/tarsil/django-messages-drf/branch/master/graph/badge.svg?token=VfTlWQlGeF)](https://codecov.io/gh/tarsil/django-messages-drf)

Django Messages DRF is an alternative and based on pinax-messages but using Django Rest Framework by making it easier to integrate with your existing project. It allows CRUD messages along with inbox and creating threads. Users can reply to messages and mark them as read.

A special thanks to pinax for inspiring me to do this and use some ideas.

Tested, easy to customize, up-to-date with Python 3.10 app that provided private user-to-user threaded messaging.

## Supported Django and Python Versions

| Django / Python | 3.6 | 3.7 | 3.8 | 3.9 | 3.10 |
| --------------- | --- | --- | --- | --- | ---- |
| 2.2             | Yes | Yes | Yes | Yes | Yes  |
| 3.0             | Yes | Yes | Yes | Yes | Yes  |
| 3.1             | Yes | Yes | Yes | Yes | Yes  |
| 3.2             | Yes | Yes | Yes | Yes | Yes  |
| 4.0             | Yes | Yes | Yes | Yes | Yes  |

# Installing

> In order to install run pip:

```shell
pip install django_messages_drf
```

> Then add `django_messages_drf` to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
  # ...
  "django_messages_drf",
  # ...
]
```

> Run Django migrations to create `django-messages-drf` database tables:

```shell
python manage.py migrate
```

> You'll also want to add `django_messages_drf.urls` into your main urlpatterns.

```python
urlpatterns = [
    # other urls
    path("api/messages-drf/", include("django_messages_drf.urls", namespace="django_messages_drf")),
]
```

> Remember to use at least Python 3.6

Process of installing uses default pip procedure like other django apps.

# URLs

## Overview

```python
from django.urls import path
from . import views

# Change app_name when customizing endpoints in your app
app_name = "django_messages_drf"

urlpatterns = [
    path('inbox/', views.InboxListApiView.as_view(), name='inbox'),
    path('message/thread/<uuid>/', views.ThreadListApiView.as_view(), name='thread'),
    path('message/thread/<user_id>/send/', views.ThreadCRUDApiView.as_view(), name='thread-create'),
    path('message/thread/<uuid>/<user_id>/send/', views.ThreadCRUDApiView.as_view(), name='thread-send'),
    path('message/thread/<user_id>/<thread_uuid>/edit/', views.EditMessageApiView.as_view(), name='message-edit'),
    path('thread/<uuid>/delete', views.ThreadCRUDApiView.as_view(), name='thread-delete'),
]

```

App provides 6 endpoints with CRUD functionalities.

## Inbox

```python
path('inbox/', views.InboxListApiView.as_view(), name='inbox'),
```

This endpoint retrieves all threads that have been sent to current user (initiated by other users).

### HTTP Request

`GET http://localhost:8000/api/messages-drf/inbox/`

<aside class="notics">
Remember — this inbox works like Gmail thread functionality
</aside>

## List Messages

```python
path('message/thread/<uuid>/', views.ThreadListApiView.as_view(), name='thread'),
```

This endpoint retrieves all messages that are within a thread.

### Route Parameters

| Parameter | Required | Description             |
| --------- | -------- | ----------------------- |
| uuid      | true     | The UUID of the thread. |

### HTTP Request

`GET http://localhost:8000/api/message/thread/<uuid>/`

<aside class="notics">
User can reply to a message that he recieved. This way he adds to a thread. When a message is replied to, the person who initiated the thread will see it in inbox.
</aside>

## Send First Message

```python
path('message/thread/<user_id>/send/', views.ThreadCRUDApiView.as_view(), name='thread-create'),
```

> This View can also take another url parameter - `thread_uuid` (see below)

This endpoint sends a new message to a user by initiating new thread.

### Route Parameters

| Parameter | Required | Description                                    |
| --------- | -------- | ---------------------------------------------- |
| user_id   | true     | The id of a user we want to send a message to. |

### Body Parameters

| Parameter | Description                | Method |
| :-------- | :------------------------- | :----- |
| message   | The content of the message | POST   |
| subject   | The subject of the message | POST   |

### HTTP Request

`GET http://localhost:8000/api/messages-drf/message/thread/<user_id>/send/`

<aside class="notics">
User can reply to a message that he recieved. This way he adds to a thread. When a message is replied to, the person who initiated the thread will see it in inbox.
</aside>

## Expand on thread

```python
path('message/thread/<uuid>/<user_id>/send/', views.ThreadCRUDApiView.as_view(), name='thread-send'),
```

> This is the same View that initiates a thread (see above).

This endpoint sends a reply to an existing message.

### Route Parameters

| Parameter | Required | Description                                    |
| --------- | -------- | ---------------------------------------------- |
| uuid      | true     | The id of a thread we want to send a reply to. |
| user_id   | true     | The id of a user we want to send a message to. |

### Body Parameters

| Parameter | Description                | Method |
| :-------- | :------------------------- | :----- |
| message   | The content of the message | POST   |
| subject   | The subject of the message | POST   |

### HTTP Request

`GET http://localhost:8000/api/messages-drf/message/thread/<uuid>/<user_id>/send/`

<aside class="notics">
Sending first message or sending another message with URL with only `<user_id>` param always initiates a thread. This was we always have a UUID of a thread to reply to.
</aside>

## Edit message

```python
path('message/thread/<user_id>/<thread_uuid>/edit/', views.EditMessageApiView.as_view(), name='message-edit'),
```

This endpoint edits a message from within a thread.

<!-- Can we change thread_uuid to a message id? Is message or thread being actually edited here ? -->

### Route Parameters

| Parameter | Required | Description                                    |
| --------- | -------- | ---------------------------------------------- |
| thread_uuid | true     | The id of a message we want to edit.           |
| user_id   | true     | The id of a user we want to send a message to. |

<!-- thread_uuid or uuid ? -->

### Body Parameters

| Parameter | Description                | Method |
| :-------- | :------------------------- | :----- |
| message   | The content of the message | POST   |
| subject   | The subject of the message | POST   |

### HTTP Request

`GET http://localhost:8000/api/messages-drf/message/thread/<user_id>/<thread_uuid>/edit/`

# Views

Django Messages DRF comes initially with a set of views that allows you
to apply in your projects. All the views are in Django Rest Framework and allowing customization
up to a certain level.

All of the serializers are provided by the settings and allows overriding from there.

## InboxListApiView

The main view for an inbox of a **`user`** where return an ordered list from the latest received to
the first.

```python
class InboxListApiView(DjangoMessageDRFAuthMixin, RequireUserContextView, ListAPIView):
    """
    Returns the Inbox the logged in User
    """
    serializer_class = InboxSerializer
    pagination_class = Pagination

    def get_queryset(self):
        queryset = Thread.inbox(self.request.user)
        return Thread.ordered(queryset)
```

### Tips

We use a custom **`Pagination`** object that adds some more details to the default Django
Pagination. You can have your own pagination object and override the default.

```python
# Custom Pagination Applied to the view

from rest_framework import pagination

from django_messages_drf.views import InboxListApiView

class MyCustomPagination(pagination.PageNumberPagination):
  # Add custom pagination logic


class MyInboxListApiView(InboxListApiView):
  pagination_class = MyCustomPagination

```

You can also override the serializer_class default using the same principle.

```python
# Custom Pagination Applied to the view

from rest_framework import serializers

from django_messages_drf.views import InboxListApiView

class MyCustomSerializer(serializers.ModelSerializer):
  # Add custom serializer logic


class MyInboxListApiView(InboxListApiView):
  serializer_class = MyCustomSerializer
```

Or combining both **`pagination`** and **`serializer_class`** in one.

```python
# Custom Pagination Applied to the view

from rest_framework import pagination
from rest_framework import serializers

from django_messages_drf.views import InboxListApiView

class MyCustomPagination(pagination.PageNumberPagination):
  # Add custom pagination logic

class MyCustomSerializer(serializers.ModelSerializer):
  # Add custom serializer logic


class MyInboxListApiView(InboxListApiView):
  serializer_class = MyCustomSerializer
  pagination_class = MyCustomPagination
```

## ThreadListApiView

```python
class ThreadListApiView(DjangoMessageDRFAuthMixin, ThreadMixin, RequireUserContextView, ListAPIView):
    """
    Gets all the messages from a given thread
    """
    serializer_class = ThreadSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_thread()
        if not instance:
            raise NotFound(code=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(instance, context=self.get_serializer_context())
        return Response(serializer.data, status=status.HTTP_200_OK)
```

### Tips

The same logic for **ThreadListApiView** is the same applied for [InboxListApiView](#tips) by
overriding the default **`serializer_class`**.

```python
# Custom Pagination Applied to the view

from rest_framework import serializers

from django_messages_drf.views import ThreadListApiView

class MyCustomSerializer(serializers.ModelSerializer):
  # Add custom serializer logic


class MyThreadListApiView(ThreadListApiView):
  serializer_class = MyCustomSerializer
```

## ThreadCRUDApiView

```python
class ThreadCRUDApiView(DjangoMessageDRFAuthMixin, ThreadMixin, RequireUserContextView, APIView):
    """
    View that allows the reply of a specific message as well as the
    We will apply some pagination to return a list for the results and therefore

    1. This API gets or creates the Thread
    2. If a UUID is passed, then a Thread is validated and created but if only a user_id is
    passed, then it will create a new thread and start a conversation.
    """
    serializer_class = ThreadReplySerializer

    def post(self, request, uuid=None, *args, **kwargs):
        """
        Replies a mensage in given thread
        """
        thread = self.get_thread() if uuid else None
        user = self.get_user()

        if not user:
            raise NotFound(code=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        subject = request.data.get('subject') or thread.subject
        if not thread:
            msg = Message.new_message(
                from_user=self.request.user, to_users=[user], subject=subject,
                content=request.data.get('message')
            )

        else:
            msg = Message.new_reply(thread, self.request.user, request.data.get('message'))
            thread.subject = subject
            thread.save()

        message = MessageSerializer(msg, context=self.get_serializer_context())
        return Response(message.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        """
        Flags a thread as deleted a thread from the system.
        To remove completely, another permanent view can be added to execute the action.
        """
        thread = self.get_thread()
        if not thread:
            raise NotFound(code=status.HTTP_404_NOT_FOUND)

        thread.userthread_set.filter(user=request.user).update(deleted=True)
        return Response(status=status.HTTP_200_OK)
```

### Tips

The same logic for **ThreadCRUDApiView** is the same applied for [InboxListApiView](#tips) by
overriding the default **`serializer_class`**.

```python
# Custom Pagination Applied to the view

from rest_framework import serializers

from django_messages_drf.views import ThreadCRUDApiView

class MyCustomSerializer(serializers.ModelSerializer):
  # Add custom serializer logic


class MyThreadCRUDApiView(ThreadCRUDApiView):
  serializer_class = MyCustomSerializer
```

## EditMessageApiView

```python
class EditMessageApiView(DjangoMessageDRFAuthMixin, ThreadMixin, RequireUserContextView, APIView):
    """
    Edits a message sent from a user in a given thread
    """
    serializer_class = EDIT_MESSAGE_SERIALIZER

    def get_instance(self, user, message_uuid):
        """
        Checks of the message exists
        """
        try:
            return Message.objects.get(sender=user, uuid=message_uuid)
        except Message.DoesNotExist:
            return

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'thread': self.get_thead_by_id(),
        })
        return context

    def put(self, request, user_id, thread_uuid, *args, **kwargs):
        """
        Edits a mensage in given thread.

        1. Gets the user_id from the URL.
        2. From the request.data gets the uuid of the message
        3. Validates
        4. Saves and returns
        """
        user = self.get_user()

        if not user:
            raise NotFound()

        if (not user.pk == request.user.pk):
            raise PermissionDenied()

        # Get the instance of the message for a given user
        instance = self.get_instance(user, request.data.get('uuid'))
        if not instance:
            raise NotFound()

        serializer = self.serializer_class(instance, data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        message = MessageSerializer(instance, context=self.get_serializer_context())
        return Response(message.data, status=status.HTTP_200_OK)

```

### General Tip

1. The views follow a similar structure and design everywhere but they can also be overwritten in a normal Django way.
2. Checkout the settings page to see how to override the variables.

# Mixins

Mixins are a super useful tool when it comes to apply the DRY principles or share functionalities
across the platform.

## RequireUserContextView

A simplification of a `get_serializer_context` that can be applied on every serializer that needs
the user in the `context`.

```python
class RequireUserContextView(GenericAPIView):
    """
    Handles with Generics of views
    """
    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'request': self.request,
            'user': self.request.user,
        })
        return context
```

## ThreadMixin

All things common to a thread.

```python
class ThreadMixin:
    """
    Everything related with a thread, is placed here.
    """
    def get_thread(self):
        """Gets the thread"""
        try:
            return Thread.objects.get(uuid=self.kwargs.get('uuid'))
        except Thread.DoesNotExist:
            return

    def get_user(self):
        """Gets a User to whom which the message will be sent"""
        try:
            return get_user_model().objects.get(pk=self.kwargs.get('user_id'))
        except get_user_model().DoesNotExist:
            return

    def get_thead_by_id(self):
        """Gets a thread by id"""
        try:
            return Thread.objects.get(id=self.kwargs.get('thread_uuid'))
        except Thread.DoesNotExist:
            return
```

## CurrentThreadDefault

Similar to `CurrentThreadDefault`, this mixin allows a similar behaviour to be injected into the
serializer fields as long as the `thread` is passed into the context.

```python
class CurrentThreadDefault:
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context['thread']

    def __repr__(self):
        return '%s()' % self.__class__.__name__
```

## Examples

```python
# serializers.py
from django_messages.drf.mixins import CurrentThreadDefault


class MessageSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(required=True)
    subject = serializers.CharField(required=True)
    content = serializers.CharField(
        required=True, allow_null=False, allow_blank=False, error_messages={
            'blank': _("The message cannot be empty"),
        }
    )
    sender = serializers.HiddenField(default=serializers.CurrentUserDefault())
    thread = serializers.HiddenField(default=CurrentThreadDefault())
```

# Models

We decided to use UUIDs to make harder to make associations by using it but not using as primary
key.

## Thread

```python
class Thread(AuditModel):
    """Main model where a thread is created. This model only contains a subject
    and a ManyToMany relationship with the users.

    Django by default creates an 'invisible' model when ManyToMany is declared
    but we can override the default and point to our own model.

    A `uuid` field is declared as a way to
    """
    uuid = models.UUIDField(blank=False, null=False, editable=False, default=uuid4)
    subject = models.CharField(max_length=150)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through="UserThread")
```

Thread is the main model and some sort of source of truth.

### Functions

```python
  @classmethod
  def inbox(cls, user):
      """Returns the inbox of a given user"""
      return cls.objects.filter(userthread__user=user, userthread__deleted=False)

  @classmethod
  def deleted(cls, user):
      """Returns the deleted messages of a given user"""
      return cls.objects.filter(userthread__user=user, userthread__deleted=True)

  @classmethod
  def unread(cls, user):
      """Returns all the unread messages of a given user"""
      return cls.objects.filter(
          userthread__user=user,
          userthread__deleted=False,
          userthread__unread=True
      )

  @property
  def first_message(self):
      """Returns the first message"""
      return self.messages.all()[0]

  @property
  def latest_message(self):
      """Returs the last message"""
      return self.messages.order_by("-sent_at")[0]

  @classmethod
  def ordered(cls, objs):
      """
      Returns the iterable ordered the correct way, this is a class method
      because we don"t know what the type of the iterable will be.
      """
      objs = list(objs)
      objs.sort(key=lambda o: o.latest_message.sent_at, reverse=True)
      return objs

  @classmethod
  def get_thread_users(cls):
      """Returns all the users from the thread"""
      return cls.users.all()

  def earliest_message(self, user_to_exclude=None):
      """
      Returns the earliest message of the thread

      :param user_to_exclude: Returns a list of the messages excluding a given user. This is
      particulary useful for showing the earliest message sent in a thread between two different
      users
      """
      try:
          return self.messages.exclude(sender=user_to_exclude).earliest('sent_at')
      except Message.DoesNotExist:
          return

  def last_message(self):
        """
        Returns the latest message of the thread. Is the reverse of the `earliest_message`
        """
        try:
            return self.messages.all().latest('sent_at')
        except Message.DoesNotExist:
            return

  def last_message_excluding_user(self, user_to_exclude=None):
      """
      Returns the latest message of the thread. Is the reverse of the `earliest_message`

      :param user_to_exclude: Returns a list of the messages excluding a given user. This is
      particulary useful for showing the latest message sent in a thread between two different
      users.
      """
      queryset = self.messages.all()
      try:
          if user_to_exclude:
              queryset = queryset.exclude(sender=user_to_exclude)
          return queryset.latest('sent_at')
      except Message.DoesNotExist:
          return

  def unread_messages(self, user):
      """
      Gets the unread messages from User in a given Thread.

      Example:
          '''
          t = Thread.objects.first()
          user = User.objects.first()
          unread = t.uread_messages(user)
          '''
      """
      return self.userthread_set.filter(user=user, deleted=False, unread=True, thread=self)

  def is_user_first_message(self, user):
      """
      Checks if the user started the thread
      :return: Bool
      """
      try:
          message = self.messages.earliest('sent_at')
      except Message.DoesNotExist:
          return False
      return bool(message.sender.pk == user.pk)
```

## UserThread

```python
class UserThread(models.Model):
    """Maps the user and the thread. This model was used to override the default ManyToMany
    relationship table generated by django.
    """
    uuid = models.UUIDField(blank=False, null=False, default=uuid4, editable=False,)

    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    unread = models.BooleanField()
    deleted = models.BooleanField()
```

This model is a substitution of the default generated by ManyToMany of Django.

## Message

```python
class Message(models.Model):
    """
    Message model where creates threads, user threads and mapping between them.
    """
    uuid = models.UUIDField(blank=False, null=False, default=uuid4, editable=False)
    thread = models.ForeignKey(Thread, related_name="messages", on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="sent_messages", on_delete=models.CASCADE)
    sent_at = models.DateTimeField(default=timezone.now)
    content = models.TextField()
```

### Functions

```python
  @classmethod
  def new_reply(cls, thread, user, content):
      """
      Create a new reply for an existing Thread. Mark thread as unread for all other participants,
      and mark thread as read by replier. We want an atomic operation as we can't afford having
      lost data between tables and causing problems with data integrity.
      """
      with transaction.atomic():
          try:
              msg = cls.objects.create(thread=thread, sender=user, content=content)
              thread.userthread_set.exclude(user=user).update(deleted=False, unread=True)
              thread.userthread_set.filter(user=user).update(deleted=False, unread=False)
              message_sent.send(sender=cls, message=msg, thread=thread, reply=True)
          except OperationalError as e:
              log.exception(e)
              return
      return msg

  @classmethod
  def new_message(cls, from_user, to_users, subject, content):
      """
      Create a new Message and Thread. Mark thread as unread for all recipients, and
      mark thread as read and deleted from inbox by creator. We want an atomic operation as we
      also can't afford having lost data between tables and causing problems with data integrity.
      """
      with transaction.atomic():
          try:
              thread = Thread.objects.create(subject=subject)
              for user in to_users:
                  thread.userthread_set.create(user=user, deleted=False, unread=True)
              thread.userthread_set.create(user=from_user, deleted=True, unread=False)
              msg = cls.objects.create(thread=thread, sender=from_user, content=content)
              message_sent.send(sender=cls, message=msg, thread=thread, reply=False)
          except OperationalError as e:
              log.exception(e)
              return
      return msg

  def get_absolute_url(self):
      return self.thread.get_absolute_url()
```

## Tips

When creating a new message, the default behavior is calling the `new_message` or `reply_message`,
depending of the type.

# Pagination

Two custom pagination classes are provided for the application. The information was gathered from
[here](https://gist.github.com/tarsil/6255492c273b682bb329ba3f8d623754).

## Pagination class

```python
class Pagination(pagination.PageNumberPagination):
    """
    Custom paginator for REST API responses
    'links': {
               'next': next page url,
               'previous': previous page url
            },
            'count': number of records fetched,
            'total_pages': total number of pages,
            'next': bool has next page,
            'previous': bool has previous page,
            'results': result set
    })
    """

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'pagination': {
                'previous_page': self.page.number - 1 if self.page.number != 1 else None,
                'current_page': self.page.number,
                'next_page': self.page.number + 1 if self.page.has_next() else None,
                'page_size': self.page_size
            },
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'next': self.page.has_next(),
            'previous': self.page.has_previous(),
            'results': data
        })
```

## SimplePagination

```python
class SimplePagination(pagination.PageNumberPagination):
    """
    Custom paginator for REST API responses
    """
    def get_paginated_response(self, data):
        return Response({
            'records_filtered': self.page.paginator.count,
            'data': data
        })
```

# Permissions

A small set of permissions are set in the app to make sure the data is safer and secure and those
can be also extended.

## AccessMixin

Base class of all permission mixins of Django Messages DRF. Adds an extension for the permissions of
Django Rest Framework where you can now append into a list instead of repeating on every class.

```python
class AccessMixin(metaclass=DjangoMessageDRFAuthMeta):
    """
    Django rest framework doesn't append permission_classes on inherited models which can cause
    issues when it comes to call an API programmatically, this way we create a metaclass that will
    read from a property custom from our subclasses and will append to the default
    `permission_classes` on the subclasses of AccessMixin.
    """
    pass
```

## DjangoMessageDRFAuthMixin

Base class of all views of the application and sets the principle that every view inheriting from
this will validate the user authentication.

```python
class DjangoMessageDRFAuthMixin(AccessMixin, APIView):
    """
    Base APIView requiring login credentials to access it from the inside of the platform
    Or via request (if known)
    """
    permissions = [IsAuthenticated]
    pagination_class = None

    def __init__(self, *args, **kwargs) -> None:
        """
        Checks if the views contain the `permissions` attribute and overrides the
        `permission_classes`.
        """
        super().__init__(*args, **kwargs)
        self.permission_classes = self.permissions
        if self.pagination_class:
            try:
                rest_settings = settings.REST_FRAMEWORK
            except AttributeError:
                rest_settings = {}
            page_size = rest_settings.get('PAGE_SIZE', 50)
            self.pagination_class.page_size = page_size

```

## Examples

Using the **`DjangoMessageDRFAuthMixin`** as a base we can now start creating our own views without
thinking about replicating the `permission_classes`.

### With DjangoMessageDRFAuthMixin

```python
from rest_framework.views import APIView

from django_messages_drf.permissions import DjangoMessageDRFAuthMixin
from my_app.permissions import MyPermission


class MyCustomView(DjangoMessageDRFAuthMixin, APiView):
  """
  My Custom view that will do things
  """
  permissions = [MyPermission]

```

Importing the `APIView` is optional since the `DjangoMessageDRFAuthMixin` already implements it.

Behind the scenes, Django Messages DRF is appending the `permissions` to `permission_classes` of
Django Rest Framework, which means that if we query for the `permission_classes` we would have:

```shell
permission_classes = [IsAuthenticated, MyPermission]
```

### Without DjangoMessageDRFAuthMixin

```python
from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated
from my_app.permissions import MyPermission


class BaseView(APiView):
  permission_classes = [IsAuthenticated]


class MyCustomView(BaseView):
  """
  My Custom view that will do things
  """
  permission_classes = [MyPermission]

```

This won't have the same result as the `DjangoMessageDRFAuthMixin` because what is doing is actually
reassigning the `permission_classes` from the `BaseView` to the `MyCustomView`.

# Serializers

Django Messages DRF like with the views, also comes with a set of serializers that allows you
to apply in your project but you can and should build your own with your own use cases.

The way the serializers are built are the default ones from Django Rest Framework.

## Inbox

A simple example for an inbox serializer.

```python
class InboxSerializer(serializers.ModelSerializer):
    """
    Serializer for the inbox.
    """
    sent_at = serializers.DateTimeField(source='first_message.sent_at')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.useruser = self.context.get('user')

    class Meta:
        model = Thread
        fields = ('uuid', 'subject', 'sent_at')

```

## Sender

A sender for Django Messages DRF is a Django **`user`** and can be whatever you decided that u.

```python
class SenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email')
```

# Serializer Settings

Django Messages DRF allows overriding some settings for the views, which means, instead of creating
a new view just to apply your own serializer, you can simply override the setting and
Django Messages DRF will apply it on the current views.

None of the below settings are required to be added to your `settings.py`. This is only if
you wish to override the current defaults.

## Overriding

In your **`settings.py`**.

| Setting Name                                    | View               | Default               |
| :---------------------------------------------- | :----------------- | :-------------------- |
| **DJANGO_MESSAGES_DRF_INBOX_SERIALIZER**        | InboxListApiView   | InboxSerializer       |
| **DJANGO_MESSAGES_DRF_THREAD_SERIALIZER**       | ThreadListApiView  | ThreadSerializer      |
| **DJANGO_MESSAGES_DRF_MESSAGE_SERIALIZER**      | ThreadCRUDApiView  | ThreadReplySerializer |
| **DJANGO_MESSAGES_DRF_EDIT_MESSAGE_SERIALIZER** | EditMessageApiView | EditMessageSerializer |

## Usage

Overriding is based on `import_string` from your **`settings.py`**.

### Examples

```python
# settings.py

DJANGO_MESSAGES_DRF_INBOX_SERIALIZER = 'myapp.serializers.MyCustomInboxSerializer'
DJANGO_MESSAGES_DRF_THREAD_SERIALIZER = 'myapp.serializers.MyCustomThreadSerializer'
```

If none of the settings is overridden or is **`None`** , then it will default to the original.

# Behaviour Settings

Django Messages DRF allows overriding some behaviours.

## Overriding

In your **`settings.py`**.

| Setting Name                                           | Behaviour                              | Type    | Default |
| :----------------------------------------------------- | :------------------------------------- | :------ | :------ |
| **DJANGO_MESSAGES_MARK_NEW_THREAD_MESSAGE_AS_DELETED** | Mark the first message sent as deleted | Boolean | True    |

# Utils

Some useful utils are provided with the project to make it easier to reuse across.

## AuditModel

```python
class AuditModel(models.Model):
    """A common audit model for tracking"""
    created_at = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    modified_at = models.DateTimeField(null=False, blank=False, auto_now=True)

```

Adding the **`AuditModel`** to a model will add an audit trailing to it making it easier
to filter by dates.

This can be extended and add more information such as **`created_by`** or **`modified_by`**
where those are users of the application.

# Signals

## Message sent

We only provide one signal at the moment. This signal fires off after every message.

```python
message_sent = Signal(providing_args=["message", "thread", "reply"])
```

<!-- Creating new threads also fires it off? -->

# Release Notes

## 1.0.6

- Preparing to drop support for python 3.6.
- Fix `providing_args` from signals as it is deprecated in Django 4.

## 1.0.5

- Added `id` field to the ThreadSerializer.

## 1.0.4

- [Bugfix #10](https://github.com/tarsil/django-messages-drf/pull/10). Thank you [kamikaz1k](https://github.com/kamikaz1k)
- [Bugfix #9](https://github.com/tarsil/django-messages-drf/pull/9). Thank you [kamikaz1k](https://github.com/kamikaz1k)

## 1.0.3

### Added

- Settings to override the serializers on the views by using a custom.
- `EditMessageApiView` allowing editing a message sent from a user of a given thread.
- `CurrentThreadDefault` similar to `CurrentUserDefault` from Django Rest Framework but for threads.

### Fixed

- Show sender when a message sent is from the same sender and receiver - [Issue](https://github.com/tarsil/django-messages-drf/issues/5)
- Issue with `display_name` for InboxSerializer - [Issue](https://github.com/tarsil/django-messages-drf/issues/4).
- `ThreadCRUDApiView` `post` where wasn't using the data from the serializer.

## 1.0.2

### Added

- Support for python 3.9
- CircleCI config

### Fixed

- Tests naming conflicts.
- Migration issues.

### Updated

- README.

## 1.0.0

- Initial release

## License

Copyright (c) 2020-present Tiago Silva and contributors under the [MIT license](https://opensource.org/licenses/MIT).
