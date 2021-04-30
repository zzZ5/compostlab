from django.contrib.auth.models import User

from account.serializers import UserSerializer
from compostlab.utils.relatedfield import RelatedFieldAlternative
from experiment.models import Experiment, Review
from equipment.models import Equipment
from equipment.serializers import EquipmentSerializer

from rest_framework import serializers


class ExperimentSerializer(serializers.ModelSerializer):

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
