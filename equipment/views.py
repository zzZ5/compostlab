from re import error
from equipment.admin import EquipmentAdmin
import hashlib
import random
import time

from account.serializers import UserSerializer
from django.contrib.auth.models import User
from django.shortcuts import render
from equipment.models import Equipment
from equipment.serializers import EquipmentSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, mixins, permissions, status


def _get_random_secret_key(length=15, allowed_chars=None, secret_key=None):
    """
    Generate random string.

    Parameter:
        length(int): the length of this string.
        allowed_chars(string): the range chars of this string.
        secret_key(string): random seed.
    Return:
        string: random string.
    """
    if allowed_chars is None:
        allowed_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    if secret_key is None:
        secret_key = "n&^-9#k*-6pwzsjt-qsc@s3$l46k(7e%f80e7gx^f#vouf3yvz"

    random.seed(
        hashlib.sha256(
            ("%s%s%s" % (
                random.getstate(),
                time.time(),
                secret_key)).encode('utf-8')
        ).digest())
    ret = ''.join(random.choice(allowed_chars) for i in range(length))
    return ret


class CreateEquipment(mixins.CreateModelMixin,
                      generics.GenericAPIView):
    '''
    Create a new Equipment, must have administrator privileges.
    '''

    permission_classes = (permissions.IsAdminUser,)

    def post(self, request, version, format=None):
        '''
        Create a new Equipment through post.
        Example:
            name: test1
            name_brief: t1
            type: RE
            descript: this is a test equipment.
        Return:
            if success, return equipment's information.
        '''
        key = _get_random_secret_key()
        while Equipment.objects.filter(key=key):
            key = _get_random_secret_key()
        serializer = EquipmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=self.request.user, key=key)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class EquipmentView(APIView):
    '''
    Get equipment's information or update equipment's information through equipment's id.
    '''

    def get_object(self, pk):
        try:
            return Equipment.objects.get(pk=pk)
        except Equipment.DoesNotExist:
            return None

    permission_classes = (permissions.IsAuthenticated,)
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer

    def get(self, request, version, pk, format=None):
        equipment = self.get_object(pk)
        serializer = EquipmentSerializer(equipment)
        return Response(serializer.data)

    def put(self, request, version, pk, *args, **kwargs):
        response_dict = {'code': 200, 'message': 'ok', 'data': {}}
        equipment = self.get_object(pk)

        if request.user.is_superuser or equipment.owner == request.user:
            serializer = EquipmentSerializer(equipment)
            serializer.update(equipment, request.data)
            response_dict['code'] = 201
            response_dict['message'] = 'Updated successfully!'
            response_dict['data'] = serializer.data
            return Response(response_dict)
        elif request.user in equipment.users.all():
            request_data = request.data
            equipment.name_brief = request_data['name_brief']
            equipment.descript = request_data['descript']
            equipment.save()
            serializer = EquipmentSerializer(equipment)
            response_dict['code'] = 201
            response_dict['message'] = 'Updated successfully!'
            response_dict['data'] = serializer.data
            return Response(response_dict)
        return Response(data={'detail': 'Inconsistent users'}, status=status.status.HTTP_400_BAD_REQUEST)
