# Pinax Messages DRF

## About Django Messages DRF

Django Messages DRF is an alternative of django_messages_drf but using
Django Rest Framework making it easier to integrate with your existing project.

Django Messages DRF is based on django_messages_drf way of implementing
but applying DRF.

A special thanks to pinax for inspiring me to do this and use some ideas.

### Overview

`django-messages-drf` is an app for providing private user-to-user threaded
messaging.

#### Supported Django and Python Versions

Django / Python | 3.6 | 3.7 | 3.8
--------------- | --- | --- | ---
2.2  |  *  |  *  |  *
3.0  |  *  |  *  |  *
3.1  |  *  |  *  |  *

## Documentation

### Installation

To install django-messages:

```shell
    $ pip install django-messages-drf
```

Add `django_messages_drf` to your `INSTALLED_APPS` setting:

```python
INSTALLED_APPS = [
    # other apps
    "django_messages_drf",
]
```

Run Django migrations to create `django-messages-drf` database tables:

```shell
    $ python manage.py migrate
```

Add `django_messages_drf.urls` to your project urlpatterns:

```python
    urlpatterns = [
        # other urls
        url(r"^messages-drf/", include("django_messages_drf.urls", namespace="django_messages_drf")),
    ]
```

### Reference Guide

#### URL–View–Template Matrix

| URL Name                             | View                  |
| ------------------------------------ | --------------------- |
| `django_messages_drf:inbox`               | `InboxListApiView()`
| `django_messages_drf:thread`      | `ThreadListApiView()`
| `django_messages_drf:thread-create` | `ThreadCRUDApiView()`
| `django_messages_drf:thread-send`       | `ThreadCRUDApiView()`
| `django_messages_drf:thread-delete`       | `ThreadCRUDApiView()`

#### URL Names

These URL names are available when using django_messages_drf urls.py:

`django_messages_drf:inbox` — Inbox view.
`django_messages_drf:thread` — Lists the details of a tread of a User.
Requires a UUID of a thread.
`django_messages_drf:thread-create` — Create new message to specific user.
Requires a User PK (user to send).
`django_messages_drf:thread-send` — Replies to a thread. requires thread UUID.
`django_messages_drf:thread-delete` — Delete message thread, requires thread
UUID.

#### Views

`InboxListApiView` - Display all message threads

`ThreadCRUDApiView` - Create a new message thread/Reply to Thread

`ThreadListApiView` - View specific message thread

`ThreadCRUDApiView` - Delete specific message thread

#### Signals

`message_sent` — `providing_args = ["message", "thread", "reply"]`

## Change Log

### 1.0.0

* initial release

## License

Copyright (c) 2020-present Tiago Silva and contributors under the [MIT license](https://opensource.org/licenses/MIT).
