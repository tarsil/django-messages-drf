from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from .mixins import CurrentThreadDefault
from .models import Message, Thread


class SenderReceiverSerializer(serializers.ModelSerializer):
    display_name = serializers.SerializerMethodField()
    is_user = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = self.context.get('user')

    class Meta:
        model = get_user_model()
        fields = ('display_name', 'is_user')

    def get_is_user(self, instance):
        return instance.pk == self.user.pk

    def get_display_name(self, instance):
        return f"{instance.first_name} {instance.last_name}"


class InboxSerializer(serializers.ModelSerializer):
    """
    Serializer for the list of messages
    """
    sender = serializers.SerializerMethodField()
    sent_at = serializers.DateTimeField(source='first_message.sent_at')
    total_unread = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = self.context.get('user')

    class Meta:
        model = Thread
        fields = ('uuid', 'subject', 'sender', 'sent_at', 'total_unread', 'last_message')

    def get_last_message(self, instance): # pragma: no cover
        message = instance.last_message()
        if message:
            return message.content[:50]

    @property
    def sender_receiver_klass(self):
        from .settings import SENDER_RECEIVER_SERIALIZER
        return SENDER_RECEIVER_SERIALIZER

    def get_sender(self, instance): # pragma: no cover
        serializer = self.sender_receiver_klass(context=self.context)
        message = instance.last_message()
        if message:
            return serializer.to_representation(message.sender)

    def get_total_unread(self, instance):
        return instance.unread_messages(self.user).count()


class MessageSerializer(serializers.ModelSerializer):
    """
    Renders the messages from a given thread
    """
    uuid = serializers.UUIDField()
    sender = serializers.SerializerMethodField()

    class Meta:
        model = Message
        exclude = ('id', 'thread',)

    @property
    def sender_receiver_klass(self):
        from .settings import SENDER_RECEIVER_SERIALIZER
        return SENDER_RECEIVER_SERIALIZER

    def get_sender(self, instance):
        serializer = self.sender_receiver_klass(context=self.context)
        return serializer.to_representation(instance.sender)


class ThreadSerializer(serializers.ModelSerializer): # pragma: no cover
    """
    Serializer for the thread
    """
    subject = serializers.CharField()
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        fields = ('id', 'uuid', 'subject', 'messages')

    def get_messages(self, instance):
        serializer = MessageSerializer(many=True, context=self.context)
        return serializer.to_representation(instance.messages.all())


class ThreadReplySerializer(serializers.Serializer):
    """
    Serializer for a given message
    """
    message = serializers.CharField(
        required=True, allow_null=False, allow_blank=False, error_messages={
            'blank': _("The message cannot be empty"),
        }
    )
    subject = serializers.CharField(
        required=True, allow_null=False, allow_blank=False, error_messages={
            'blank': _("The subject cannot be empty"),
        }
    )


class EditMessageSerializer(serializers.ModelSerializer):
    """
    Specifically edits a message
    """
    uuid = serializers.UUIDField(
        required=True, error_messages={
            'blank': _("The message cannot be empty"),
            'null': _("The message cannot be empty")
        }
    )
    content = serializers.CharField(
        required=True, allow_null=False, allow_blank=False, error_messages={
            'blank': _("The message cannot be empty"),
        }
    )
    sender = serializers.HiddenField(default=serializers.CurrentUserDefault())
    thread = serializers.HiddenField(default=CurrentThreadDefault())

    class Meta:
        model = Message
        exclude = ('id',)

    def update(self, instance, validated_data):
        instance.content = validated_data.get('content', instance.content)
        instance.sender = validated_data.get('sender', instance.sender)
        instance.thread = validated_data.get('thread', instance.thread)
        instance.save()
        return instance
