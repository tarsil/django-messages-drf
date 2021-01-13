from rest_framework import serializers


class SerializerTest(serializers.Serializer):
    """
    Test Serializer
    """
    name = serializers.CharField(required=False)
