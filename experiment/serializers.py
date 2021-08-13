import dateutil.parser
import pytz


from django.contrib.auth.models import User
from django.utils import timezone

from account.serializers import UserSerializer
from compostlab.utils.relatedfield import RelatedFieldAlternative
from experiment.models import Experiment, ExperimentRecord, Review
from equipment.models import Equipment
from equipment.serializers import EquipmentDetailSerializer

from rest_framework import serializers


def save_experiment_record(name, old, new, modifier, experiment):
    '''
    保存实验修改记录.

    Args:
        name: 修改的属性名称。
        old: 修改前的内容。
        new: 修改后的内容。
        modifier: 修改人。
        experiment: 要修改的实验。

    Return:
        Bool: True已保存记录, False修改后和修改前相同，未保存记录。
    '''

    if old != new:
        record = 'Changed the "{}" from "{}" to "{}"'.format(
            name, old, new)
        ExperimentRecord.objects.create(
            modifier=modifier, experiment=experiment, record=record)
        return True
    else:
        return False


class ExperimentDetailSerializer(serializers.ModelSerializer):
    '''
    序列化实验信息。

    将实验详细信息序列化，包括设备，主要用于实验的创建和修改。
    '''

    def update(self, instance, validated_data, modifier):
        # 更新实验信息时调用该方法，每个属性只要有改变都会记录下来。

        user_data = validated_data.pop('user')
        users = []
        for i in user_data:
            users.append(User.objects.get(pk=i))
        if save_experiment_record('user', list(instance.user.all()), users, modifier, instance):
            instance.user.set(users)

        equipment_data = validated_data.pop('equipment')
        equipments = []
        for i in equipment_data:
            equipments.append(Equipment.objects.get(pk=i))
        if save_experiment_record('equipment', list(instance.equipment.all()), equipments, modifier, instance):
            instance.equipment.set(equipments)

        owner_data = validated_data.pop('owner')
        owner = User.objects.get(pk=owner_data)
        if save_experiment_record('owner', instance.owner, owner, modifier, instance):
            instance.owner = owner

        name = validated_data.get('name', instance.name)
        if save_experiment_record('name', instance.name, name, modifier, instance):
            instance.name = name

        site = validated_data.get('site', instance.site)
        if save_experiment_record('site', instance.site, site, modifier, instance):
            instance.site = site

        descript = validated_data.get('descript', instance.descript)
        if save_experiment_record('descript', instance.descript, descript, modifier, instance):
            instance.descript = descript

        begin_time = validated_data.get('begin_time', instance.begin_time)
        if save_experiment_record('begin_time', instance.begin_time, begin_time, modifier, instance):
            begin_time = dateutil.parser.parse(begin_time)
            print(begin_time)
            instance.begin_time = begin_time

        end_time = validated_data.get('end_time', instance.end_time)
        if save_experiment_record('end_time', instance.end_time, end_time, modifier, instance):
            instance.end_time = end_time
        instance.status = 0
        try:
            instance.review.delete()
        except:
            pass
        instance.save()
        return instance

    id = serializers.UUIDField(read_only=True)
    equipment = RelatedFieldAlternative(
        queryset=Equipment.objects.all(), serializer=EquipmentDetailSerializer,  required=False, many=True)
    user = RelatedFieldAlternative(
        queryset=User.objects.all(), serializer=UserSerializer, required=False, many=True)
    owner = RelatedFieldAlternative(
        queryset=User.objects.all(), serializer=UserSerializer)

    class Meta:
        model = Experiment
        fields = ('id', 'name', 'site', 'descript', 'equipment', 'begin_time',
                  'end_time', 'user', 'owner', 'status', 'created_time')
        depth = 1


class ExperimentSerializer(serializers.ModelSerializer):
    '''
    序列化实验信息。

    将实验信息序列化，但不包括设备，主要用于传输信息到前端。
    '''

    user = RelatedFieldAlternative(
        queryset=User.objects.all(), serializer=UserSerializer, required=False, many=True)
    owner = RelatedFieldAlternative(
        queryset=User.objects.all(), serializer=UserSerializer)

    class Meta:
        model = Experiment
        fields = ('id', 'name', 'site', 'descript', 'begin_time',
                  'end_time', 'user', 'owner', 'status', 'created_time')
        depth = 1


class ReviewSerializer(serializers.ModelSerializer):
    '''
    序列化实验审核信息。
    '''

    def create(self, validated_data):
        review = Review(**validated_data)
        if review.is_passed:
            review.experiment.status = 1
        else:
            review.experiment.status = -1
        review.experiment.save()
        review.save()
        return review

    class Meta:
        model = Review
        fields = ('experiment', 'is_passed', 'reply', 'user', 'created_time')
