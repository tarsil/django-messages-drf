# URLs

## Names

These URL names are available when using django_messages_drf urls.py:

- `django_messages_drf:inbox` — Inbox view.
- `django_messages_drf:thread` — Lists the details of a tread of a User.
Requires a UUID of a thread.
- `django_messages_drf:thread-create` — Create new message to specific user.
Requires a User PK (user to send).
- `django_messages_drf:thread-send` — Replies to a thread. requires thread UUID.
- `django_messages_drf:thread-delete` — Delete message thread, requires thread
UUID.