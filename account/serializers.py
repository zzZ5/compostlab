from rest_framework import serializers
from django.contrib.auth.models import User
from account.models import UserRecord


def _save_user_record(name, old, new, user):
    if old != new:
        record = 'Changed the "{}" from "{}" to "{}"'.format(
            name, old, new)
        UserRecord.objects.create(record=record, user=user)
        return True
    else:
        return False


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password',
                  'is_staff', 'is_superuser', 'last_login', 'date_joined')

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class BriefUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_staff',
                  'is_superuser', 'last_login', 'date_joined')

    def update(self, instance, validated_data):

        username = validated_data.get('username', instance.username)
        if _save_user_record('username', instance.username, username, instance):
            instance.username = username

        email = validated_data.get('email', instance.email)
        if _save_user_record('email', instance.email, email, instance):
            instance.email = email

        instance.save()
        return instance


class UserRecordSerializer(serializers.ModelSerializer):
    user = BriefUserSerializer(required=False)

    class Meta:
        model = UserRecord
        fields = ('record', 'user', 'created_time')
        depth = 1
