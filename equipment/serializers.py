from rest_framework import serializers
from account.serializers import BriefUserSerializer
from django.contrib.auth.models import User
from equipment.models import Equipment, EquipmentRecordUsage, EquipmentRecordModify


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


def _save_equipment_record(name, old, new, modifier, equipment):
    if old != new:
        record = 'Changed the "{}" from "{}" to "{}"'.format(
            name, old, new)
        EquipmentRecordModify.objects.create(
            modifier=modifier, equipment=equipment, record=record)
        return True
    else:
        return False


class EquipmentSerializer(serializers.ModelSerializer):
    owner = BriefUserSerializer(required=False)
    users = BriefUserSerializer(required=False, many=True)

    class Meta:
        model = Equipment
        fields = ('id', 'name', 'name_brief', 'key',
                  'type', 'descript', 'begin_time', 'end_time',
                  'created_time', 'users', 'owner')
        depth = 1

    def update(self, instance, validated_data, modifier):

        owner_data = validated_data.pop('owner')
        owner = _get_user(**owner_data)
        if _save_equipment_record('owner', instance.owner, owner, modifier, instance):
            instance.owner = owner

        users_data = validated_data.pop('users')
        users = []
        for i in users_data:
            users.append(_get_user(**i))
        if _save_equipment_record('users', list(instance.users.all()), users, modifier, instance):
            instance.users.set(users)

        name = validated_data.get('name', instance.name)
        if _save_equipment_record('name', instance.name, name, modifier, instance):
            instance.name = name

        name_brief = validated_data.get('name_brief', instance.name_brief)
        if _save_equipment_record('name_brief', instance.name_brief, name_brief, modifier, instance):
            instance.name_brief = name_brief

        # key = validated_data.get('key', instance.key)
        # if _save_equipment_record('key', instance.key, key, modifier, instance):
        #     instance.key = key

        type = validated_data.get('type', instance.type)
        if _save_equipment_record('type', instance.type, type, modifier, instance):
            instance.type = type

        descript = validated_data.get('descript', instance.descript)
        if _save_equipment_record('descript', instance.descript, descript, modifier, instance):
            instance.descript = descript

        begin_time = validated_data.get('begin_time', instance.begin_time)
        if _save_equipment_record('begin_time', instance.begin_time, begin_time, modifier, instance):
            instance.begin_time = begin_time

        end_time = validated_data.get('end_time', instance.end_time)
        if _save_equipment_record('end_time', instance.end_time, end_time, modifier, instance):
            instance.end_time = end_time

        instance.save()
        return instance


class EquipmentUsageRecordSerializer(serializers.ModelSerializer):
    users = BriefUserSerializer(required=False, many=True)
    equipment = EquipmentSerializer(required=False)

    class Meta:
        model = EquipmentRecordUsage
        fields = ('begin_time', 'end_time', 'user', 'equpment')
        depth = 1


class EquipmentModifyRecordSerializer(serializers.ModelSerializer):
    modifier = BriefUserSerializer(required=False)
    # equipment = EquipmentSerializer(required=False)

    class Meta:
        model = EquipmentRecordModify
        fields = ('record', 'modifier', 'created_time')
        depth = 1
