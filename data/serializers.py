import equipment
from account.serializers import UserSerializer
from data.models import Sensor, SensorRecord
from equipment.models import Equipment

from rest_framework import serializers


def get_equipment(id='', name=''):
    '''
    get Equipment.object by id or name. 
    '''

    equipment = None
    if id != '':
        equipment = Equipment.objects.get(pk=id)
    elif name != '':
        equipment = Equipment.objects.get(name=name)
    return equipment


def save_sensor_record(name, old, new, modifier, sensor):
    if old != new:
        record = 'Changed the "{}" from "{}" to "{}"'.format(
            name, old, new)
        SensorRecord.objects.create(
            record=record, sensor=sensor, modifier=modifier)
        return True
    else:
        return False


class SensorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sensor
        fields = ('id', 'name', 'name_brief', 'key', 'type',
                  'descript', 'equipment', 'created_time')
        # depth = 1

    def update(self, instance, validated_data, modifier):
        equipment_data = validated_data.pop('equipment')
        equipment = get_equipment(id=equipment_data)
        if save_sensor_record('equipment', instance.equipment, equipment, modifier, instance):
            instance.equipment = equipment

        name = validated_data.get('name', instance.name)
        if save_sensor_record('name', instance.name, name, modifier, instance):
            instance.name = name

        name_brief = validated_data.get('name_brief', instance.name_brief)
        if save_sensor_record('name_brief', instance.name_brief, name_brief, modifier, instance):
            instance.name_brief = name_brief

        type = validated_data.get('type', instance.type)
        if save_sensor_record('type', instance.type, type, modifier, instance):
            instance.type = type

        descript = validated_data.get('descript', instance.descript)
        if save_sensor_record('descript', instance.descript, descript, modifier, instance):
            instance.descript = descript

        instance.save()
        return instance


class SensorRecordSerializer(serializers.ModelSerializer):
    modifier = UserSerializer(required=False)
    sensor = SensorSerializer(required=False)

    class Meta:
        model = SensorRecord
        fields = ('record', 'sensor', 'modifier', 'created_time')
        depth = 1


class DataSerializer(serializers.ModelSerializer):
    sensor = SensorSerializer(required=False)

    class Meta:
        model = SensorRecord
        fields = ('sensor', 'value', 'unit', 'measured_time', 'created_time')
        depth = 1
