from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Stats


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(**validated_data)
        return user

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stats
        field = ["id","username","avg_wpm","last_wpm"]
        extra_kwargs = {"username" : {"read_only" : True}}