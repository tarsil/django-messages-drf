import uuid

from django.contrib.auth import get_user_model
from django.urls import reverse

from django_webtest import WebTest

import django_messages_drf.tests.factories
from django_messages_drf.models import Message, Thread, UserThread

from ..models import Message, Thread


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

    def test_can_get_thread_endpoint(self):
        """User can get to the thread endpoint"""
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
