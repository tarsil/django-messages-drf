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

    def setUp(self) -> None:
        self.brosner = django_messages_drf.tests.factories.UserFactory()
        self.jtauber = django_messages_drf.tests.factories.UserFactory()


class TestMessages(BaseTest):

    def test_message_methods(self):
        """
        Test Message and Thread methods.
        """
        message_string = "You can't be serious"
        Message.new_message(
            self.brosner, [self.jtauber], "Really?", message_string)

        self.assertEqual(Thread.inbox(self.brosner).count(), 0)
        self.assertEqual(Thread.inbox(self.jtauber).count(), 1)
        self.assertEqual(Thread.unread(self.jtauber).count(), 1)

        thread = Thread.inbox(self.jtauber)[0]

        Message.new_reply(thread, self.jtauber, "Yes, I am.")

        self.assertEqual(Thread.inbox(self.brosner).count(), 1)
        self.assertEqual(Thread.inbox(self.jtauber).count(), 1)
        self.assertEqual(Thread.unread(self.jtauber).count(), 0)

        Message.new_reply(thread, self.brosner, "If you say so...")
        reply_string = "Indeed I do"
        Message.new_reply(thread, self.jtauber, reply_string)

        self.assertEqual(
            Thread.objects.get(pk=thread.pk).latest_message.content,
            reply_string)
        self.assertEqual(
            Thread.objects.get(pk=thread.pk).first_message.content,
            message_string)

    def test_ordered(self):
        """
        Ensure Thread ordering is last-sent-first (LIFO).
        """
        t1 = Message.new_message(
            self.brosner, [self.jtauber], "Subject",
            "A test message").thread
        t2 = Message.new_message(
            self.brosner, [self.jtauber], "Another",
            "Another message").thread
        t3 = Message.new_message(
            self.brosner, [self.jtauber], "Pwnt",
            "Haha I'm spamming your inbox").thread
        self.assertEqual(Thread.ordered([t2, t1, t3]), [t3, t2, t1])
