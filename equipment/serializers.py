from rest_framework import serializers
from account.serializers import BriefUserSerializer
from django.contrib.auth.models import User
from equipment.models import Equipment, EquipmentUsageRecord, EquipmentHistoricalRecord, Sensor, SensorHistoricalRecord


def _get_user(id='', username='', email='', *args, **kwargs):
    '''
    get User.object  by id, username or email. 
    '''

    user = None
    if id != '':
        user = User.objects.get(pk=id)
    elif username != '':
        user = User.objects.get(username=username)
    elif email != '':
        user = User.objects.get(email=email)
    return user


class EquipmentSerializer(serializers.ModelSerializer):
    owner = BriefUserSerializer(required=False)
    users = BriefUserSerializer(required=False, many=True)

    class Meta:
        model = Equipment
        fields = ('id', 'name', 'name_brief', 'key',
                  'type', 'descript', 'begin_time', 'end_time', 'users', 'owner')
        depth = 1

    def update(self, instance, validated_data):
        owner_data = validated_data.pop('owner')
        owner = _get_user(**owner_data)
        users_data = validated_data.pop('users')
        users = []
        for i in users_data:
            users.append(_get_user(**i))

        instance.name = validated_data.get('name', instance.name)
        instance.name_brief = validated_data.get('email', instance.name_brief)
        instance.key = validated_data.get('key', instance.key)
        instance.type = validated_data.get('type', instance.type)
        instance.descript = validated_data.get('descript', instance.descript)
        instance.begin_time = validated_data.get(
            'begin_time', instance.begin_time)
        instance.end_time = validated_data.get('end_time', instance.end_time)
        instance.owner = owner
        instance.users.set(users)
        instance.save()
        return instance


class EquipmentUsageRecordSerializer(serializers.ModelSerializer):
    users = BriefUserSerializer(required=False, many=True)
    equipment = EquipmentSerializer(required=False)

    class Meta:
        model = EquipmentUsageRecord
        fields = ('id', 'begin_time', 'end_time', 'user', 'equpment')
        depth = 1

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create(**validated_data)
        Profile.objects.create(user=user, **profile_data)
        return user


class EquipmentHistoryRecordSerializer(serializers.ModelSerializer):
    owner = BriefUserSerializer(required=False)
    modifier = BriefUserSerializer(required=False)
    equipment = EquipmentSerializer(required=False)

    class Meta:
        model = EquipmentHistoricalRecord
        fields = ('id', 'name', 'name_brief', 'key',
                  'type', 'descript', 'equipment', 'owner', 'modifier')
        depth = 1


class SensorSerializer(serializers.ModelSerializer):
    equipment = EquipmentSerializer(required=False)

    class Meta:
        model = Sensor
        fields = ('id', 'name', 'name_brief', 'key',
                  'type', 'descript', 'equipment')
        depth = 1


class SensorHistoricalRecordSerializer(serializers.ModelSerializer):
    modifier = BriefUserSerializer(required=False)
    sensor = SensorSerializer(required=False)
    equipment = EquipmentSerializer(required=False)

    class Meta:
        model = SensorHistoricalRecord
        fields = ('id', 'name', 'name_brief', 'key',
                  'type', 'descript', 'equipment', 'sensor', 'modifier')
        depth = 1
