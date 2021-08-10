from account.serializers import UserSerializer
from data.serializers import DataSerializer
from equipment.models import Equipment
from sensor.models import Sensor, SensorRecord

from rest_framework import serializers


def get_equipment(id='', key=''):
    '''
    通过id或者key获取equipment对象

    Args:
        id: equipment的id。
        key: equipment的key。

    Return:
        equipment对象。
    '''

    equipment = None
    if id != '':
        equipment = Equipment.objects.get(pk=id)
    elif key != '':
        equipment = Equipment.objects.get(key=key)
    return equipment


def save_sensor_record(name, old, new, modifier, sensor):
    '''
    保存传感器修改记录.

    Args:
        name: 修改的属性名称。
        old: 修改前的内容。
        new: 修改后的内容。
        modifier: 修改人。
        sensor: 要修改的传感器。

    Return:
        Bool: True已保存记录, False修改后和修改前相同，未保存记录。
    '''

    if old != new:
        record = 'Changed the "{}" from "{}" to "{}"'.format(
            name, old, new)
        SensorRecord.objects.create(
            record=record, sensor=sensor, modifier=modifier)
        return True
    else:
        return False


class SensorSerializer(serializers.ModelSerializer):
    '''
    序列化传感器信息。

    将传感器信息序列化，主要用于传感器的创建、修改以及传输信息到前端。
    '''

    data_latest = serializers.SerializerMethodField(read_only=True)
    key = serializers.CharField(read_only=True)

    class Meta:
        model = Sensor
        fields = ('id', 'name', 'abbreviation', 'key', 'type', 'unit',
                  'descript', 'equipment', 'data_latest', 'created_time')
        # depth = 1

    def get_data_latest(self, obj):
        # 获取传感器最新一个数据。
        res = []
        if obj.data.all():
            res = DataSerializer(obj.data.latest()).data
        return res

    def update(self, instance, validated_data, modifier):
        # 更新传感器信息时调用该方法，每个属性只要有改变都会记录下来。

        try:
            equipment_data = validated_data.pop('equipment')
            equipment = get_equipment(id=equipment_data)
            if save_sensor_record('equipment', instance.equipment, equipment, modifier, instance):
                instance.equipment = equipment
        except:
            pass

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
    '''
    序列化传感器修改信息。
    '''

    modifier = UserSerializer(required=False)
    sensor = SensorSerializer(required=False)

    class Meta:
        model = SensorRecord
        fields = ('record', 'sensor', 'modifier', 'created_time')
        depth = 1
