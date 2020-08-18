"""
All the permissions used by Pinax Messages DRF are placed and treated here
"""

from django.conf import settings

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


class DjangoMessageDRFAuthMeta(type):
    """
    Metaclass to create/read from permissions property. Django Rest Framework doesn't implement this
    directly where `permission_classes` instead of inheriting the super classes, just overrides so
    DjangoMessageDRF will be adding an extra level of functionality by creating a permissions
    attribute.
    """
    def __new__(cls, name, bases, attrs):
        permissions = []
        for base in bases:
            if hasattr(base, 'permissions'):
                permissions.extend(base.permissions)
        attrs['permissions'] = permissions + attrs.get('permissions', [])
        return type.__new__(cls, name, bases, attrs)


class AccessMixin(metaclass=DjangoMessageDRFAuthMeta):
    """
    Django rest framework doesn't append permission_classes on inherited models which can cause
    issues when it comes to call an API programmatically, this way we create a metaclass that will
    read from a property custom from our subclasses and will append to the default
    `permission_classes` on the subclasses of AccessMixin.
    """
    pass


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
