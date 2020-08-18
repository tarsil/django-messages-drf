"""
All Utils used on this package module live here
"""
from django.db import models
from functools import wraps


def cached_attribute(func):
    cache_name = f"_{func.__name__}"

    @wraps(func)
    def inner(self, *args, **kwargs):
        if hasattr(self, cache_name):
            return getattr(self, cache_name)
        val = func(self, *args, **kwargs)
        setattr(self, cache_name, val)
        return val
    return


class AuditModel(models.Model):
    """A common audit model for tracking"""
    created_at = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    modified_at = models.DateTimeField(null=False, blank=False, auto_now=True)
