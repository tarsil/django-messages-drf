from django.contrib.auth import get_user_model
from django.test import TestCase

import django_messages_drf.tests.factories

from ..models import Message, Thread, UserThread


class BaseTest(TestCase):

    def tearDown(self) -> None:
        get_user_model().objects.all().delete()
        Message.objects.all().delete()
        UserThread.objects.all().delete()
        Thread.objects.all().delete()


class MessageModelTestCase(BaseTest):

    def test_can_create_thread(self):
        """System can create a Thread"""
        thread = django_messages_drf.tests.factories.ThreadFactory()

        self.assertIsNotNone(thread)

    def test_can_create_message(self):
        """System can create a message"""
        message = django_messages_drf.tests.factories.MessageFactory()

        self.assertIsNotNone(message)

    def test_user_can_have_one_assign_thread(self):
        """A specific user is assigned to a thread"""
        user = django_messages_drf.tests.factories.UserFactory(
            first_name="test", last_name="user", email="test@user.com"
        )
        user_two = django_messages_drf.tests.factories.UserFactory(
            first_name="test2", last_name="user2", email="test2@user2.com"
        )

        subject = 'subject'
        content = 'content'
        Message.new_message(user, [user_two], subject, content=content)

        total_threads = Thread.objects.all()
        total_messages = Message.objects.all()
        thread = Thread.objects.last()

        self.assertEqual(user.userthread_set.count(), 1)
        self.assertEqual(user.userthread_set.last().thread.uuid, thread.uuid)
        self.assertEqual(user_two.userthread_set.count(), 1)
        self.assertEqual(user_two.userthread_set.last().thread.uuid, thread.uuid)
        self.assertEqual(1, total_threads.count())
        self.assertEqual(1, total_messages.count())
