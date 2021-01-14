# Views

Django Messages DRF comes initially with a set of views that allows you
to apply in your projects. All the views are in Django Rest Framework and allowing customization
up to a certain level.

All of the serializers are provided by the settings and allows overriding from there.

---

## List of Views

1. [InboxListApiView](#inboxlistapiview)
2. [ThreadListApiView](#threadlistapiview)
3. [ThreadCRUDApiView](#threadcrudapiview)
4. [EditMessageApiView](#editmessageapiview)

---

## __InboxListApiView__

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

## __ThreadListApiView__

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

The same logic for __ThreadListApiView__ is the same applied for [InboxListApiView](#tips) by
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

## __ThreadCRUDApiView__

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

The same logic for __ThreadCRUDApiView__ is the same applied for [InboxListApiView](#tips) by
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

## __EditMessageApiView__

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

    def put(self, request, user_id, thread_id, *args, **kwargs):
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
