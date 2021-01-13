import json
import uuid

from django.contrib.auth import get_user_model
from django.db import transaction
from django.test import RequestFactory, TestCase
from django.urls import reverse

import django_messages_drf.tests.factories
import django_messages_drf.tests.utils
import django_messages_drf.views
from django_downloadview.test import setup_view
from django_webtest import WebTest
from rest_framework.exceptions import ValidationError

from ..models import Message, Thread, UserThread
from ..serializers import InboxSerializer, ThreadSerializer


class BaseTest(WebTest):
    csrf_checks = False

    def tearDown(self) -> None:
        get_user_model().objects.all().delete()
        Message.objects.all().delete()
        UserThread.objects.all().delete()
        Thread.objects.all().delete()

    def test_user_not_logged_in_cannot_access_inbox(self):
        """If a user is not logged in, it cannot access an inbox url"""
        url = reverse("django_messages_drf:inbox")

        response = self.app.get(url, expect_errors=True)

        self.assertEqual(403, response.status_code)

    def test_can_get_inbox_view(self):
        """User can get into inbox URL view if logged in"""
        user = django_messages_drf.tests.factories.UserFactory()
        url = reverse("django_messages_drf:inbox")

        response = self.app.get(url, user=user)

        self.assertEqual(200, response.status_code)

    def test_can_get_thread_endpoint(self):
        """User can get to the thread endpoint"""
        user = django_messages_drf.tests.factories.UserFactory()
        thread = django_messages_drf.tests.factories.ThreadFactory()
        url = reverse("django_messages_drf:thread", kwargs={'uuid': thread.uuid})

        response = self.app.get(url, user=user)

        self.assertEqual(200, response.status_code)

    def test_cannot_get_thread_endpoint(self):
        """User cannot get to the thread endpoint"""
        thread = django_messages_drf.tests.factories.ThreadFactory()
        url = reverse("django_messages_drf:thread", kwargs={'uuid': thread.uuid})

        response = self.app.get(url, expect_errors=True)

        self.assertEqual(403, response.status_code)

    def test_cannot_get_thread_create_endpoint(self):
        """User cannot get to the thread create endpoint"""
        user = django_messages_drf.tests.factories.UserFactory()
        url = reverse("django_messages_drf:thread-create", kwargs={'user_id': user.id})

        response = self.app.post(url, expect_errors=True)

        self.assertEqual(403, response.status_code)

    def test_can_get_thread_post_endpoint(self):
        """User can get to the thread post endpoint"""
        user = django_messages_drf.tests.factories.UserFactory()
        user_to_send = django_messages_drf.tests.factories.UserFactory()
        url = reverse("django_messages_drf:thread-create", kwargs={'user_id': user_to_send.id})

        params = {
            'subject': 'test',
            'message': 'message',
        }

        response = self.app.post(url, user=user, params=params)

        threads = Thread.objects.all()

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, threads.count())

    def test_returns_400_when_missing_subject_param(self):
        """If subject not send, throws 400"""
        user = django_messages_drf.tests.factories.UserFactory()
        user_to_send = django_messages_drf.tests.factories.UserFactory()
        url = reverse("django_messages_drf:thread-create", kwargs={'user_id': user_to_send.id})

        params = {
            'subject': '',
            'message': 'message',
        }

        response = self.app.post(url, user=user, params=params, expect_errors=True)

        threads = Thread.objects.all()

        self.assertEqual(400, response.status_code)
        self.assertEqual(0, threads.count())

    def test_returns_400_when_missing_message_param(self):
        """If message not send, throws 400"""
        user = django_messages_drf.tests.factories.UserFactory()
        user_to_send = django_messages_drf.tests.factories.UserFactory()
        url = reverse("django_messages_drf:thread-create", kwargs={'user_id': user_to_send.id})

        params = {
            'subject': 'test',
            'message': '',
        }

        response = self.app.post(url, user=user, params=params, expect_errors=True)

        threads = Thread.objects.all()

        self.assertEqual(400, response.status_code)
        self.assertEqual(0, threads.count())

    def test_cannot_get_thread_send_reply_endpoint(self):
        """User cannot get to the thread create endpoint"""
        user = django_messages_drf.tests.factories.UserFactory()
        thread = django_messages_drf.tests.factories.ThreadFactory()
        url = reverse("django_messages_drf:thread-send", kwargs={
            'uuid': thread.uuid,
            'user_id': user.id
        })

        response = self.app.post(url, expect_errors=True)

        self.assertEqual(403, response.status_code)

    def test_can_get_thread_send_reply_endpoint(self):
        """User can get to the thread endpoint"""
        user = django_messages_drf.tests.factories.UserFactory()
        thread = django_messages_drf.tests.factories.ThreadFactory()
        url = reverse("django_messages_drf:thread-send", kwargs={
            'uuid': thread.uuid,
            'user_id': user.id
        })

        params = {
            'subject': 'test',
            'message': 'message',
        }

        response = self.app.post(url, user=user, params=params)

        threads = Thread.objects.all()

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, threads.count())

    def test_returns_400_when_missing_subject_on_reply_param(self):
        """If subject not send, throws 400"""
        user = django_messages_drf.tests.factories.UserFactory()
        thread = django_messages_drf.tests.factories.ThreadFactory()
        url = reverse("django_messages_drf:thread-send", kwargs={
            'uuid': thread.uuid,
            'user_id': user.id
        })

        params = {
            'subject': '',
            'message': 'message',
        }

        response = self.app.post(url, user=user, params=params, expect_errors=True)

        self.assertEqual(400, response.status_code)

    def test_returns_400_when_missing_message_on_reply_param(self):
        """If message not send, throws 400"""
        user = django_messages_drf.tests.factories.UserFactory()
        thread = django_messages_drf.tests.factories.ThreadFactory()
        url = reverse("django_messages_drf:thread-send", kwargs={
            'uuid': thread.uuid,
            'user_id': user.id
        })

        params = {
            'subject': 'test',
            'message': '',
        }

        response = self.app.post(url, user=user, params=params, expect_errors=True)

        self.assertEqual(400, response.status_code)

    def test_cannot_get_thread_delete_endpoint(self):
        """User cannot get to the thread delete endpoint"""
        thread = django_messages_drf.tests.factories.ThreadFactory()
        url = reverse("django_messages_drf:thread-delete", kwargs={
            'uuid': thread.uuid,
        })

        response = self.app.delete(url, expect_errors=True)

        self.assertEqual(403, response.status_code)

    def test_can_get_thread_delete_endpoint(self):
        """User can get to the thread delete endpoint"""
        user = django_messages_drf.tests.factories.UserFactory()
        thread = django_messages_drf.tests.factories.ThreadFactory()
        Message.new_reply(thread, user, "content")

        url = reverse("django_messages_drf:thread-delete", kwargs={
            'uuid': thread.uuid,
        })

        response = self.app.delete(url, user=user)

        self.assertEqual(200, response.status_code)

    def test_throws_404_delete_endpoint(self):
        """When a hread not found, throws a 404 not found"""
        user = django_messages_drf.tests.factories.UserFactory()
        django_messages_drf.tests.factories.ThreadFactory()

        url = reverse("django_messages_drf:thread-delete", kwargs={
            'uuid': str(uuid.uuid4()),
        })

        response = self.app.delete(url, user=user, expect_errors=True)

        self.assertEqual(404, response.status_code)


    def test_can_get_edit_endpoint(self):
        """User can get to the edit message endpoint"""
        user = django_messages_drf.tests.factories.UserFactory()
        thread = django_messages_drf.tests.factories.ThreadFactory()

        with transaction.atomic():
            message = Message.new_reply(thread, user, "content")

            url = reverse("django_messages_drf:message-edit",
                          kwargs={
                              'user_id': user.id,
                              'thread_id': thread.id
                              }
                          )

            params = {
                'uuid': str(message.uuid),
                'content': 'message',
            }

            response = self.app.put(url, user=user, params=params)

            threads = Thread.objects.all()

            self.assertEqual(200, response.status_code)
            self.assertEqual(1, threads.count())

    def test_returns_400_when_missing_content_param(self):
        """If content not send, throws 400"""
        user = django_messages_drf.tests.factories.UserFactory()
        thread = django_messages_drf.tests.factories.ThreadFactory()

        with transaction.atomic():
            message = Message.new_reply(thread, user, "content")

            url = reverse("django_messages_drf:message-edit",
                          kwargs={
                              'user_id': user.id,
                              'thread_id': thread.id
                              }
                          )

            params = {
                'uuid': str(message.uuid),
                'content': '',
            }

            response = self.app.put(url, user=user, params=params, expect_errors=True)

            threads = Thread.objects.all()

            self.assertEqual(400, response.status_code)
            self.assertEqual(1, threads.count())

    def test_raises_exception_when_missing_uuid_param(self):
        """If uuid not send, throws an exception"""
        user = django_messages_drf.tests.factories.UserFactory()
        thread = django_messages_drf.tests.factories.ThreadFactory()

        with transaction.atomic():
            Message.new_reply(thread, user, "content")

            url = reverse("django_messages_drf:message-edit",
                          kwargs={
                              'user_id': user.id,
                              'thread_id': thread.id
                              }
                          )

            params = {
                'uuid': "",
                'content': 'content',
            }

            with self.assertRaises(Exception) as raised:
                self.app.put(url, user=user, params=params, expect_errors=True)

                threads = Thread.objects.all()

                self.assertEqual(raised.exception, type(ValidationError))
                self.assertEqual(1, threads.count())

    def test_message_is_change_only_by_the_user_who_send(self):
        """The message is only changed by the user who sent it"""
        user = django_messages_drf.tests.factories.UserFactory()
        user_two = django_messages_drf.tests.factories.UserFactory()
        thread = django_messages_drf.tests.factories.ThreadFactory()

        with transaction.atomic():
            message = Message.new_reply(thread, user, "content")

            url = reverse("django_messages_drf:message-edit",
                          kwargs={
                              'user_id': user.id,
                              'thread_id': thread.id
                              }
                          )

            params = {
                'uuid': str(message.uuid),
                'content': 'new content',
            }

            self.assertEqual(message.sender_id, user.id)
            self.assertEqual(message.content, 'content')
            self.assertEqual(message.thread_id, thread.id)

            # SEND MESSAGE
            self.app.put(url, user=user, params=params)
            saved_message = Message.objects.get(thread=thread, uuid=message.uuid)

            threads = Thread.objects.all()

            self.assertEqual(saved_message.sender_id, user.id)
            self.assertEqual(saved_message.content, 'new content')
            self.assertNotEqual(saved_message.content, 'content')
            self.assertEqual(1, threads.count())

            # SEND DIFFERENT
            response = self.app.put(url, user=user_two, params=params, expect_errors=True)
            self.assertEqual(403, response.status_code)


class SerializerViewTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get(reverse('django_messages_drf:inbox'))

    def xtest_serializer_is_original(self):
        """Check the original serializer passed"""
        inbox_view = setup_view(django_messages_drf.views.InboxListApiView(), self.request)
        serializer = inbox_view.serializer_class

        self.assertEqual(serializer.__name__.lower(), InboxSerializer.__name__.lower())

    def test_settings_serializer(self):
        """The serializer used is loaded from the settings"""
        inbox_view = setup_view(django_messages_drf.views.ThreadListApiView(), self.request)
        serializer = inbox_view.serializer_class

        self.assertEqual(serializer.__name__.lower(), django_messages_drf.tests.utils.SerializerTest.__name__.lower())

    def test_override_serializer(self):
        """The serializer used is not the original but the overridden"""
        inbox_view = setup_view(django_messages_drf.views.ThreadListApiView(), self.request)
        serializer = inbox_view.serializer_class

        self.assertNotEqual(serializer.__name__.lower(), ThreadSerializer.__name__.lower())


class IssueTests(BaseTest):

    def test_create_thread_assert_contents_send_to_itself(self):
        """
        Bug: https://github.com/tarsil/django-messages-drf/issues/5

        1. Create a thread for a user
        2. Post a message with a given content
        3. Returns successfully with the data validated
        4. Fetch the inbox to see the results
        """
        user = django_messages_drf.tests.factories.UserFactory(first_name='', last_name='')
        user_to_send = django_messages_drf.tests.factories.UserFactory()
        url = reverse("django_messages_drf:thread-create", kwargs={'user_id': user.id})

        params = {
            'subject': 'a thread subject',
            'message': 'this is a message!\n\nveronica@mars.com',
        }

        response = self.app.post(url, user=user, params=params)

        data = json.loads(response.content)

        self.assertEqual(data.get('content'), "this is a message!\n\nveronica@mars.com")
        self.assertEqual(data.get('sender').get("display_name"), " ")
        self.assertTrue(data.get('sender').get("is_user"))

        # FETCH INBOX
        url_inbox = reverse("django_messages_drf:inbox")
        response_inbox = self.app.get(url_inbox, user=user)

        results = json.loads(response_inbox.content).get('results')
        result = list(results)[0]

        self.assertEqual(data.get('content'), "this is a message!\n\nveronica@mars.com")
        self.assertIsNotNone(result.get('sender'))
