from ..settings import (
    get_serializer_by_settings,
    InboxSerializer,
    ThreadSerializer,
    ThreadReplySerializer,
    EditMessageSerializer
)
from django.test import TestCase
from django.test import override_settings


class SettingsTest(TestCase):

    def test_return_class_from_settings(self):
        """Returns class associtated"""
        klass = get_serializer_by_settings(EditMessageSerializer, 'DJANGO_MESSAGES_DRF_EDIT_MESSAGE_SERIALIZER')

        self.assertEqual(klass.__name__.lower(), EditMessageSerializer.__name__.lower())
