"""
Settings used specifically for django_messages_drf
"""
# pragma: no cover
from django.conf import settings
from django.utils.module_loading import import_string
from typing import Any

from .serializers import (InboxSerializer, ThreadSerializer, ThreadReplySerializer, EditMessageSerializer)


def get_serializer_by_settings(default: Any, setting_name: str):
    """
    Loads the serializer from the given settings or sets the default otherwise.
    """
    path: str = None

    if hasattr(settings, setting_name):
        path = getattr(settings, setting_name)

    if not path:
        return default
    try:
        return import_string(path)
    except ImportError as e :
        raise e

# Default settings for the serializers
INBOX_SERIALIZER = get_serializer_by_settings(InboxSerializer, 'DJANGO_MESSAGES_DRF_INBOX_SERIALIZER')
THREAD_SERIALIZER = get_serializer_by_settings(ThreadSerializer, 'DJANGO_MESSAGES_DRF_THREAD_SERIALIZER')
THREAD_REPLY_SERIALIZER = get_serializer_by_settings(ThreadReplySerializer, 'DJANGO_MESSAGES_DRF_MESSAGE_SERIALIZER')
EDIT_MESSAGE_SERIALIZER = get_serializer_by_settings(EditMessageSerializer, 'DJANGO_MESSAGES_DRF_EDIT_MESSAGE_SERIALIZER')
