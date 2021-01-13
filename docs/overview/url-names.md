# URLs

## Names

These URL names are available when using django_messages_drf `urls.py`:

| View  | Description   |
| :-------- | :----- |
| __django_messages_drf:inbox__ | Inbox view. |
| __django_messages_drf:thread__ | Lists the details of a tread of a User. Requires a UUID of a thread. |
| __django_messages_drf:thread-create__ | Create new message to specific user. Requires a User PK (user to send). |
| __django_messages_drf:thread-send__ | Replies to a thread. Requires thread UUID. |
| __django_messages_drf:thread-delete__ | Delete message thread, requires thread UUID. |
| __django_messages_drf:message-edit__ | Edits a message sent in a thread. |

## django_messages_drf:inbox

It doesn't require parameters

## __django_messages_drf:thread__

| Parameter | Description | Method
| :-------- | :----- | :----- |
| uuid | The UUID of a thread | GET |

## __django_messages_drf:thread-create__

Creates a thread.

| Parameter | Description | Method |
| :-------- | :----- | :----- |
| user_id | The user id | GET |
| message | The content of the message | POST |
| subject | The subject of the message | POST |

## __django_messages_drf:thread-send__

Replies to the thread.

| Parameter | Description | Method |
| :-------- | :----- | :----- |
| uuid | The UUID of a thread | GET |
| user_id | The user id | GET |
| message | The content of the message | POST |
| subject | The subject of the message | POST |

## __django_messages_drf:thread-delete__

Replies to the thread.

| Parameter | Description | Method |
| :-------- | :----- | :----- |
| uuid | The UUID of a thread | DELETE |

## __django_messages_drf:message-edit__

Edits a message sent by a given user.

| Parameter | Description | Method |
| :-------- | :----- | :----- |
| user_id | The UUID of a thread | GET |
| thread_id | The UUID of a thread | GET |
| uuid | The UUID of the message to edit | PUT |
| content | The content of the message | PUT |
