from account.models import UserRecord
from django.contrib.auth.models import User
from rest_framework import serializers

from libgravatar import Gravatar


def save_user_record(name, old, new, user):
    if old != new:
        record = 'Changed the "{}" from "{}" to "{}"'.format(
            name, old, new)
        UserRecord.objects.create(record=record, user=user)
        return True
    else:
        return False


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'is_active',
                  'is_staff', 'is_superuser', 'last_login', 'date_joined')

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField(read_only=True)
    avatar = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email',
                  'last_login', 'date_joined', 'roles', 'avatar')

    def get_roles(self, obj):
        res = []
        if obj.is_active:
            res.append('active')
        if obj.is_staff:
            res.append('admin')
        if obj.is_superuser:
            res.append('superuser')
        return res

    def get_avatar(self, obj):
        email = obj.email
        default = "mp"
        size = 128
        g = Gravatar(email=email)
        return g.get_image(default=default, size=size)

    def update(self, instance, validated_data):
        username = validated_data.get('username', instance.username)
        if save_user_record('username', instance.username, username, instance):
            instance.username = username

        email = validated_data.get('email', instance.email)
        if save_user_record('email', instance.email, email, instance):
            instance.email = email

        instance.save()
        return instance


class UserRecordSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)

    class Meta:
        model = UserRecord
        fields = ('record', 'user', 'created_time')
        depth = 1
