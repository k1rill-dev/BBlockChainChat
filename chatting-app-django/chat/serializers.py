from django.contrib.auth.models import User
from rest_framework import serializers
from chat.models import Message


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())
    receiver = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())
    full_name_send = serializers.CharField(max_length=255, required=False)
    full_name_receiver = serializers.CharField(max_length=255, required=False)

    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'message', 'hash_bloks', 'timestamp', 'full_name_send', 'full_name_receiver']