# Installation

```shell
$ pip install django-messages-drf
```

Add `django_messages_drf` to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
  ...
  "django_messages_drf",
  ...
]
```

Run Django migrations to create `django-messages-drf` database tables:

```shell
$ python manage.py migrate
```

You'll also want to add ``django_messages_drf.urls` into your main urlpatterns.

```python
urlpatterns = [
    # other urls
    path(r"^messages-drf/", include("django_messages_drf.urls", namespace="django_messages_drf")),
]
```
