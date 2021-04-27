from account.serializers import UserSerializer
from data.models import Sensor
from data.serializers import SensorSerializer
from equipment.models import Equipment,  EquipmentRecord

from rest_framework import serializers


def get_sensor(id='', key=''):
    '''
    get Sensor.object by id or key. 
    '''

    sensor = None
    if id != '':
        sensor = Sensor.objects.get(pk=id)
    elif key != '':
        sensor = Sensor.objects.get(key=key)
    return sensor


def save_equipment_record(name, old, new, modifier, equipment):
    if old != new:
        record = 'Changed the "{}" from "{}" to "{}"'.format(
            name, old, new)
        EquipmentRecord.objects.create(
            modifier=modifier, equipment=equipment, record=record)
        return True
    else:
        return False


class EquipmentSerializer(serializers.ModelSerializer):

    sensors = SensorSerializer(required=False, many=True)

    class Meta:
        model = Equipment
        fields = ('id', 'name', 'name_brief', 'type',
                  'descript', 'sensors', 'created_time')
        depth = 1

    def update(self, instance, validated_data, modifier):
        sensors_data = validated_data.pop('sensors')
        sensors = []
        for i in sensors_data:
            sensors.append(get_sensor(**i))
        if save_equipment_record('sensors', list(instance.sensors.all()), sensors, modifier, instance):
            instance.sensors.set(sensors)

        name = validated_data.get('name', instance.name)
        if save_equipment_record('name', instance.name, name, modifier, instance):
            instance.name = name

        name_brief = validated_data.get('name_brief', instance.name_brief)
        if save_equipment_record('name_brief', instance.name_brief, name_brief, modifier, instance):
            instance.name_brief = name_brief

        type = validated_data.get('type', instance.type)
        if save_equipment_record('type', instance.type, type, modifier, instance):
            instance.type = type

        descript = validated_data.get('descript', instance.descript)
        if save_equipment_record('descript', instance.descript, descript, modifier, instance):
            instance.descript = descript

        instance.save()
        return instance


class EquipmentRecordSerializer(serializers.ModelSerializer):
    modifier = UserSerializer(required=False)
    equipment = EquipmentSerializer(required=False)

    class Meta:
        model = EquipmentRecord
        fields = ('record', 'equipment', 'modifier', 'created_time')
        depth = 1
