# Serializers

Django Messages DRF like with the views, also comes with a set of serializers that allows you
to apply in your project but you can and should build your own with your own use cases.

The way the serializers are built are the default ones from Django Rest Framework.

## Examples

### Inbox

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

### Sender

A sender for Django Messages DRF is a Django **`user`** and can be whatever you decided that u.

```python
class SenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email')
```
