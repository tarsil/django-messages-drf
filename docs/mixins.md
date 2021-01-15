# Mixins

Mixins are a super useful tool when it comes to apply the DRY principles or share functionalities
across the platform.

---

1. [RequireUserContextView](#RequireUserContextView)
2. [ThreadMixin](#ThreadMixin)
3. [CurrentThreadDefault](#CurrentThreadDefault)

---

## RequireUserContextView

A simplification of a `get_serializer_context` that can be applied on every serializer that needs
the user in the `context`.

```python hl_lines="18"
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
            return Thread.objects.get(id=self.kwargs.get('thread_id'))
        except Thread.DoesNotExist:
            return
```

## CurrentThreadDefault

Similar to `CurrentThreadDefault`, this mixin allows a similar behaviour to be injected into the 
serializer fields as long as the `thread` is passed into the context.

```python hl_lines="5"
class CurrentThreadDefault:
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context['thread']

    def __repr__(self):
        return '%s()' % self.__class__.__name__
```

### Examples

``` python hl_lines="2 14"
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
