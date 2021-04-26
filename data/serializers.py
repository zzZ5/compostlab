from rest_framework import serializers
from account.serializers import BriefUserSerializer
from data.models import Sensor, Sensor_Record


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ('id', 'name', 'name_brief', 'key',
                  'type', 'descript', 'equipment', 'created_time')
        depth = 1


class SensorRecordSerializer(serializers.ModelSerializer):
    modifier = BriefUserSerializer(required=False)
    sensor = SensorSerializer(required=False)

    class Meta:
        model = Sensor_Record
        fields = ('record', 'sensor', 'modifier', 'created_time')
        depth = 1


class DataSerializer(serializers.ModelSerializer):
    sensor = SensorSerializer(required=False)

    class Meta:
        model = Sensor_Record
        fields = ('sensor', 'value', 'unit', 'measured_time', 'created_time')
        depth = 1
