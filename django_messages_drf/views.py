import logging

from django.utils.translation import ugettext_lazy as _

from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .mixins import RequireUserContextView, ThreadMixin
from .models import Message, Thread
from .pagination import Pagination
from .permissions import DjangoMessageDRFAuthMixin
from .serializers import InboxSerializer, MessageSerializer, ThreadReplySerializer, ThreadSerializer

log = logging.getLogger(__name__)


class InboxListApiView(DjangoMessageDRFAuthMixin, RequireUserContextView, ListAPIView):
    """
    Returns the Inbox the logged in User
    """
    serializer_class = InboxSerializer
    pagination_class = Pagination

    def get_queryset(self):
        queryset = Thread.inbox(self.request.user)
        return Thread.ordered(queryset)


class ThreadListApiView(DjangoMessageDRFAuthMixin, ThreadMixin, RequireUserContextView, ListAPIView):
    """
    Gets all the messages from a given thread
    """
    serializer_class = ThreadSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_thread()
        if not instance:
            raise NotFound(code=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(instance, context=self.get_serializer_context())
        return Response(serializer.data, status=status.HTTP_200_OK)


class ThreadCRUDApiView(DjangoMessageDRFAuthMixin, ThreadMixin, RequireUserContextView, APIView):
    """
    View that allows the reply of a specific message as well as the
    We will apply some pagination to return a list for the results and therefore

    1. This API gets or creates the Thread
    2. If a UUID is passed, then a Thread is validated and created but if only a user_id is
    passed, then it will create a new thread and start a conversation.
    """
    serializer_class = ThreadReplySerializer

    def post(self, request, uuid=None, *args, **kwargs):
        """
        Replies a mensage in given thread
        """
        thread = self.get_thread() if uuid else None
        user = self.get_user()

        if not user:
            raise NotFound(code=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        subject = request.data.get('subject') or thread.subject
        if not thread:
            msg = Message.new_message(
                from_user=self.request.user, to_users=[user], subject=subject,
                content=request.data.get('message')
            )

        else:
            msg = Message.new_reply(thread, self.request.user, request.data.get('message'))
            thread.subject = subject
            thread.save()

        message = MessageSerializer(msg, context=self.get_serializer_context())
        return Response(message.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        """
        Flags a thread as deleted a thread from the system.
        To remove completely, another permanent view can be added to execute the action.
        """
        thread = self.get_thread()
        if not thread:
            raise NotFound(code=status.HTTP_404_NOT_FOUND)

        thread.userthread_set.filter(user=request.user).update(deleted=True)
        return Response(status=status.HTTP_200_OK)
