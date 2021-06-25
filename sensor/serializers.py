from account.serializers import UserSerializer
from data.serializers import DataSerializer
from equipment.models import Equipment
from sensor.models import Sensor, SensorRecord

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
    data_latest = serializers.SerializerMethodField(read_only=True)
    key = serializers.CharField(read_only=True)

    class Meta:
        model = Sensor
        fields = ('id', 'name', 'abbreviation', 'key', 'type', 'unit',
                  'descript', 'equipment', 'data_latest', 'created_time')
        # depth = 1

    def get_data_latest(self, obj):
        res = []
        if obj.data.all():
            res = DataSerializer(obj.data.latest()).data
        return res

    def update(self, instance, validated_data, modifier):
        equipment_data = validated_data.pop('equipment')
        equipment = get_equipment(id=equipment_data)
        if save_sensor_record('equipment', instance.equipment, equipment, modifier, instance):
            instance.equipment = equipment

        name = validated_data.get('name', instance.name)
        if save_sensor_record('name', instance.name, name, modifier, instance):
            instance.name = name

        abbreviation = validated_data.get(
            'abbreviation', instance.abbreviation)
        if save_sensor_record('abbreviation', instance.abbreviation, abbreviation, modifier, instance):
            instance.abbreviation = abbreviation

        type = validated_data.get('type', instance.type)
        if save_sensor_record('type', instance.type, type, modifier, instance):
            instance.type = type

        unit = validated_data.get('unit', instance.unit)
        if save_sensor_record('unit', instance.unit, unit, modifier, instance):
            instance.unit = unit

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
