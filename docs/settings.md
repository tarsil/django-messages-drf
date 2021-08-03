# Serializer Settings

Django Messages DRF allows overriding some settings for the views, which means, instead of creating
a new view just to apply your own serializer, you can simply override the setting and
Django Messages DRF will apply it on the current views.

None of the below settings are required to be added to your `settings.py`. This is only if
you wish to override the current defaults.

## Overriding

In your **`settings.py`**.

| Setting Name  | View | Default |
| :-------- | :----- | :----- |
| __DJANGO_MESSAGES_DRF_INBOX_SERIALIZER__ | InboxListApiView | InboxSerializer |
| __DJANGO_MESSAGES_DRF_THREAD_SERIALIZER__ | ThreadListApiView | ThreadSerializer |
| __DJANGO_MESSAGES_DRF_MESSAGE_SERIALIZER__ | ThreadCRUDApiView | ThreadReplySerializer |
| __DJANGO_MESSAGES_DRF_EDIT_MESSAGE_SERIALIZER__ | EditMessageApiView | EditMessageSerializer |

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

| Setting Name  | Behaviour | Type   | Default |
| :--------     | :-----    | :----- | :-----  |
| __DJANGO_MESSAGES_MARK_NEW_THREAD_MESSAGE_AS_DELETED__ | Mark the first message sent as deleted | Boolean | True |
