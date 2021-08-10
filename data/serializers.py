from data.models import Data
from sensor.models import Sensor

from rest_framework import serializers


class DataSerializer(serializers.ModelSerializer):
    '''
    序列化数据信息。
    '''

    sensor = serializers.PrimaryKeyRelatedField(read_only=True)
    key = serializers.CharField(write_only=True)

    def validate_key(self, value):
        """
        每一次新建数据之前都要检验该数据的snesor是否合法。
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
        fields = ('sensor', 'key', 'value', 'measured_time')
        # depth = 1
