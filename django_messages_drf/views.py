import logging

from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .mixins import RequireUserContextView, ThreadMixin
from .models import Message, Thread
from .pagination import Pagination
from .permissions import DjangoMessageDRFAuthMixin
from .serializers import MessageSerializer
from .settings import (
    EDIT_MESSAGE_SERIALIZER,
    INBOX_SERIALIZER,
    THREAD_REPLY_SERIALIZER,
    THREAD_SERIALIZER,
)

log = logging.getLogger(__name__)


class InboxListApiView(DjangoMessageDRFAuthMixin, RequireUserContextView, ListAPIView):
    """
    Returns the Inbox the logged in User
    """
    serializer_class = INBOX_SERIALIZER
    pagination_class = Pagination

    def get_queryset(self):
        queryset = Thread.inbox(self.request.user)
        return Thread.ordered(queryset)

class SentboxListApiView(DjangoMessageDRFAuthMixin, RequireUserContextView, ListAPIView):
    """
    Returns the sentbox for the logged-in user
    """
    serializer_class = INBOX_SERIALIZER
    pagination_class = Pagination

    def get_queryset(self):
        queryset = Thread.sentbox(self.request.user)
        return Thread.ordered(queryset)


class ThreadListApiView(DjangoMessageDRFAuthMixin, ThreadMixin, RequireUserContextView, ListAPIView):
    """
    Gets all the messages from a given thread
    """
    serializer_class = THREAD_SERIALIZER

    def get(self, request, *args, **kwargs):
        instance = self.get_thread()
        if not instance:
            raise NotFound()

        serializer = self.serializer_class(instance, context=self.get_serializer_context())
        return Response(serializer.data, status=status.HTTP_200_OK)


class ThreadCRUDApiView(DjangoMessageDRFAuthMixin, ThreadMixin, RequireUserContextView, APIView):
    """
    Creating, Deleting and Following up on existing thread. 
    If a UUID is passed, then a Thread is validated and parameters are used to create a reply-message.
    If only a user_id is passed, then new thread is created (conversation which can be followed up has started).
    """
    serializer_class = THREAD_REPLY_SERIALIZER

    def post(self, request, uuid=None, *args, **kwargs):
        """
        Replies a message in a given thread. 
        """
        thread = self.get_thread() if uuid else None
        user = self.get_user()

        if not user:
            raise NotFound()

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        subject = serializer.data.get('subject') or thread.subject
        if not thread:
            msg = Message.new_message(
                from_user=self.request.user, to_users=[user], subject=subject,
                content=serializer.data.get('message')
            )

        else:
            msg = Message.new_reply(thread, self.request.user, serializer.data.get('message'))
            thread.sent_by = self.request.user
            thread.subject = subject
            thread.save()

        message = MessageSerializer(msg, context=self.get_serializer_context())
        return Response(message.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        """
        Flags a thread as deleted from the system.
        To remove completely, another permanent view can be added to execute the action.
        """
        thread = self.get_thread()
        if not thread:
            raise NotFound()

        thread.userthread_set.filter(user=request.user).update(deleted=True)
        return Response(status=status.HTTP_200_OK)


class EditMessageApiView(DjangoMessageDRFAuthMixin, ThreadMixin, RequireUserContextView, APIView):
    """
    Edits a message sent from a user in a given thread
    """
    serializer_class = EDIT_MESSAGE_SERIALIZER

    def get_instance(self, user, message_uuid):
        """
        Checks of the message exists
        """
        try:
            return Message.objects.get(sender=user, uuid=message_uuid)
        except Message.DoesNotExist:
            return

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'thread': self.get_thead_by_id(),
        })
        return context

    def put(self, request, user_id, thread_uuid, *args, **kwargs):
        """
        Edits a mensage in given thread.

        1. Gets the user_id from the URL.
        2. From the request.data gets the uuid of the message
        3. Validates
        4. Saves and returns
        """
        user = self.get_user()

        if not user:
            raise NotFound()

        if (not user.pk == request.user.pk):
            raise PermissionDenied()

        # Get the instance of the message for a given user
        instance = self.get_instance(user, request.data.get('uuid'))
        if not instance:
            raise NotFound()

        serializer = self.serializer_class(instance, data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        message = MessageSerializer(instance, context=self.get_serializer_context())
        return Response(message.data, status=status.HTTP_200_OK)
