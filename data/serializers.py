from data.models import Data
from sensor.models import Sensor
from sensor.serializers import SensorSerializer

from rest_framework import serializers


class DataSerializer(serializers.ModelSerializer):
    sensor = serializers.PrimaryKeyRelatedField(read_only=True)
    key = serializers.CharField(write_only=True)

    def validate_key(self, value):
        """
        Check that the sensor.
        """
        try:
            sensor = Sensor.objects.get(key=value)
        except:
            raise serializers.ValidationError("Invalidate key")
        return sensor

    def create(self, validated_data):
        sensor = validated_data.pop('key')
        data = Data.objects.create(**validated_data, sensor=sensor)
        return data

    class Meta:
        model = Data
        fields = ('sensor', 'key', 'value', 'unit',
                  'measured_time')
        # depth = 1
