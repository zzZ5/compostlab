from account.serializers import UserSerializer
from compostlab.utils.relatedfield import RelatedFieldAlternative
from data.models import Sensor
from sensor.serializers import SensorSerializer
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

    class Meta:
        model = Equipment
        fields = ('id', 'name', 'abbreviation', 'type', 'key',
                  'descript', 'created_time')
        depth = 1


class EquipmentDetailSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    sensor = RelatedFieldAlternative(queryset=Sensor.objects.all(
    ), serializer=SensorSerializer,  required=False, many=True)
    key = serializers.CharField(read_only=True)

    class Meta:
        model = Equipment
        fields = ('id', 'name', 'abbreviation', 'type', 'key',
                  'descript', 'sensor', 'created_time')
        depth = 1

    def update(self, instance, validated_data, modifier):
        sensor_data = validated_data.pop('sensor')
        sensors = []
        for i in sensor_data:
            sensors.append(get_sensor(id=i))
        if save_equipment_record('sensor', list(instance.sensor.all()), sensors, modifier, instance):
            instance.sensor.set(sensors)

        name = validated_data.get('name', instance.name)
        if save_equipment_record('name', instance.name, name, modifier, instance):
            instance.name = name

        abbreviation = validated_data.get(
            'abbreviation', instance.abbreviation)
        if save_equipment_record('abbreviation', instance.abbreviation, abbreviation, modifier, instance):
            instance.abbreviation = abbreviation

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
