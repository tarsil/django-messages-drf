# Permissions

A small set of permissions are set in the app to make sure the data is safer and secure and those
can be also extended.

---

1. [AccessMixin](#accessmixin)
1. [DjangoMessageDRFAuthMixin](#djangomessagedrfauthmixin)

---

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
