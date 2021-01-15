"""
All Utils used on this package module live here
"""
from django.db import models


class AuditModel(models.Model):
    """A common audit model for tracking"""
    created_at = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    modified_at = models.DateTimeField(null=False, blank=False, auto_now=True)
