from account.models import UserRecord
from django.contrib.auth.models import User
from rest_framework import serializers

from compostlab.utils.gravatar import Gravatar


def save_user_record(name, old, new, user):
    '''
    保存用户修改记录.

    Args:
        name: 修改的属性名称。
        old: 修改前的内容。
        new: 修改后的内容。
        user: 要修改的用户。

    Return:
        Bool:  True已保存记录, False修改后和修改前相同，未保存记录。
    '''

    if old != new:
        record = 'Changed the "{}" from "{}" to "{}"'.format(
            name, old, new)
        UserRecord.objects.create(record=record, user=user)
        return True
    else:
        return False


class UserDetailSerializer(serializers.ModelSerializer):
    '''
    序列化详细用户信息。

    将用户表详细信息序列化，包括密码，主要用于新建用户和更新用户信息。
    '''

    id = serializers.UUIDField(read_only=True)
    password = serializers.CharField(write_only=True)
    roles = serializers.SerializerMethodField(read_only=True)
    avatar = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'is_active', 'is_staff',
                  'is_superuser', 'last_login', 'date_joined', 'roles', 'avatar')

    def create(self, validated_data):
        # 新建用户的时候，密码要单独设置。
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    def update(self, instance, validated_data):

        # 每更新一个用户属性的时候，调用一次保存用户信息的方法。

        username = validated_data.get('username', instance.username)
        if save_user_record('username', instance.username, username, instance):
            instance.username = username

        email = validated_data.get('email', instance.email)
        if save_user_record('email', instance.email, email, instance):
            instance.email = email

        instance.save()
        return instance

    def get_roles(self, obj):
        # 获取用户的所有角色，用于传输json信息到前端。
        res = []
        if obj.is_active:
            res.append('active')
        if obj.is_staff:
            res.append('admin')
        if obj.is_superuser:
            res.append('superuser')
        return res

    def get_avatar(self, obj):
        # 通过用户的邮箱获取用户的头像链接，用于传输json信息到前端，这里采用的是Gravatar的头像。
        email = obj.email
        g = Gravatar(email=email)
        return g.get_image()


class UserSerializer(serializers.ModelSerializer):
    '''
    序列化用户信息。

    该类不包括密码等隐私信息，主要用于向前端传输基本账号信息。
    '''

    roles = serializers.SerializerMethodField(read_only=True)
    avatar = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'last_login',
                  'date_joined', 'roles', 'avatar')

    def get_roles(self, obj):
        # 获取用户的所有角色，用于传输json信息到前端。
        res = []
        if obj.is_active:
            res.append('active')
        if obj.is_staff:
            res.append('admin')
        if obj.is_superuser:
            res.append('superuser')
        return res

    def get_avatar(self, obj):
        # 通过用户的邮箱获取用户的头像链接，用于传输json信息到前端，这里采用的是Gravatar的头像。
        email = obj.email
        g = Gravatar(email=email)
        return g.get_image()


class UserRecordSerializer(serializers.ModelSerializer):
    '''
    序列化用户修改记录。
    '''

    user = UserSerializer(required=False)

    class Meta:
        model = UserRecord
        fields = ('record', 'user', 'created_time')
        depth = 1
