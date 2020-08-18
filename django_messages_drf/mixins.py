from django.contrib.auth import get_user_model

from rest_framework.generics import GenericAPIView

from .models import Thread


class RequireUserContextView(GenericAPIView):
    """
    Handles with Generics of views
    """

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'request': self.request,
            'user': self.request.user,
        })
        return context


class ThreadMixin:
    """
    Everything related with a thread, is placed here.
    """
    def get_thread(self):
        """Gets the thread"""
        try:
            return Thread.objects.get(uuid=self.kwargs.get('uuid'))
        except Thread.DoesNotExist:
            return

    def get_user(self):
        """Gets a User to whom which the message will be sent"""
        try:
            return get_user_model().objects.get(pk=self.kwargs.get('user_id'))
        except get_user_model().DoesNotExist:
            return
