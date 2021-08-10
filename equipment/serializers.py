from account.serializers import UserSerializer
from compostlab.utils.relatedfield import RelatedFieldAlternative
from data.models import Sensor
from sensor.serializers import SensorSerializer
from equipment.models import Equipment,  EquipmentRecord

from rest_framework import serializers


def get_sensor(id='', key=''):
    '''
    通过id或者key获取sensor对象

    Args:
        id: sensor的id。
        key: sensor的key。

    Return:
        sensor对象。
    '''

    sensor = None
    if id != '':
        sensor = Sensor.objects.get(pk=id)
    elif key != '':
        sensor = Sensor.objects.get(key=key)
    return sensor


def save_equipment_record(name, old, new, modifier, equipment):
    '''
    保存设备修改记录.

    Args:
        name: 修改的属性名称。
        old: 修改前的内容。
        new: 修改后的内容。
        modifier: 修改人。
        equipment: 要修改的设备。

    Return:
        Bool: True已保存记录, False修改后和修改前相同，未保存记录。
    '''

    if old != new:
        record = 'Changed the "{}" from "{}" to "{}"'.format(
            name, old, new)
        EquipmentRecord.objects.create(
            modifier=modifier, equipment=equipment, record=record)
        return True
    else:
        return False


class EquipmentSerializer(serializers.ModelSerializer):
    '''
    序列化设备信息。

    将设备信息序列化，但不包括传感器，主要用于传输信息到前端。
    '''

    class Meta:
        model = Equipment
        fields = ('id', 'name', 'abbreviation', 'type', 'key',
                  'descript', 'created_time')
        depth = 1


class EquipmentDetailSerializer(serializers.ModelSerializer):
    '''
    序列化设备信息。

    将设备详细信息序列化，包括传感器，主要用于设备的创建和修改。
    '''

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
        # 更新设备信息时调用该方法，每个属性只要有改变都会记录下来。

        try:
            sensor_data = validated_data.pop('sensor')
            sensors = []
            for i in sensor_data:
                sensors.append(get_sensor(id=i))
            if save_equipment_record('sensor', list(instance.sensor.all()), sensors, modifier, instance):
                instance.sensor.set(sensors)
        except:
            pass
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
    '''
    序列化设备修改信息。
    '''

    modifier = UserSerializer(required=False)
    equipment = EquipmentSerializer(required=False)

    class Meta:
        model = EquipmentRecord
        fields = ('record', 'equipment', 'modifier', 'created_time')
        depth = 1
