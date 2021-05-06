from django.contrib.auth.models import User

from account.serializers import UserSerializer
from compostlab.utils.relatedfield import RelatedFieldAlternative
from experiment.models import Experiment, ExperimentRecord, Review
from equipment.models import Equipment
from equipment.serializers import EquipmentSerializer

from rest_framework import serializers


def save_experiment_record(name, old, new, modifier, experiment):
    if old != new:
        record = 'Changed the "{}" from "{}" to "{}"'.format(
            name, old, new)
        ExperimentRecord.objects.create(
            modifier=modifier, experiment=experiment, record=record)
        return True
    else:
        return False


class ExperimentSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data, modifier):

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
            instance.begin_time = begin_time

        end_time = validated_data.get('end_time', instance.end_time)
        if save_experiment_record('end_time', instance.end_time, end_time, modifier, instance):
            instance.end_time = end_time

        instance.save()
        return instance

    equipment = RelatedFieldAlternative(
        queryset=Equipment.objects.all(), serializer=EquipmentSerializer,  required=False, many=True)

    user = RelatedFieldAlternative(
        queryset=User.objects.all(), serializer=UserSerializer, required=False, many=True)

    owner = RelatedFieldAlternative(
        queryset=User.objects.all(), serializer=UserSerializer)

    class Meta:
        model = Experiment
        fields = ('id', 'name', 'site', 'descript', 'equipment', 'begin_time',
                  'end_time', 'user', 'owner', 'status', 'created_time')
        depth = 1


class ReviewSerializer(serializers.ModelSerializer):
    experiment = RelatedFieldAlternative(
        queryset=Experiment.objects.all(), serializer=ExperimentSerializer)
    user = RelatedFieldAlternative(
        queryset=User.objects.all(), serializer=UserSerializer)

    class Meta:
        model = Review
        fields = ('experiment', 'is_passed', 'reply', 'user', 'created_time')
