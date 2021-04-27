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


class SensorSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        equipment_data = validated_data.pop('equipment')
        equipment = get_equipment(id=equipment_data['id'])
        sensor = Sensor.objects.create(**validated_data)
        sensor.equipment = equipment
        return sensor

    class Meta:
        model = Sensor
        fields = ('id', 'name', 'name_brief', 'key', 'type',
                  'descript', 'equipment', 'created_time')
        # depth = 1


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
