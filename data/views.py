import hashlib
import random
import time

from compostlab.utils.pagination import RecordPagination
from data.models import Sensor, Data
from data.serializers import DataSerializer, SensorSerializer

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


def get_random_secret_key(length=15, allowed_chars=None, secret_key=None):
    '''
    Generate random string.

    Parameter:
        length(int): the length of this string.
        allowed_chars(string): the range chars of this string.
        secret_key(string): random seed.
    Return:
        string: random string.
    '''

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


class DataViewSet(GenericViewSet):
    queryset = Sensor.objects.all()
    serializer_class = DataSerializer
    permission_classes = (IsAuthenticated,)

    def get_sensor_by_key(key):
        Sensor.objects.get(key=key)

    @ action(methods=['post'], detail=False, url_path='upload', permission_classes=[AllowAny])
    def upload_data(self, request, version, format=None):
        '''
        Create a new Data through post.
        Example:
            "value": "25.0"
            "unit": "℃"
            "key": "Sensor's key"
            "measured_time": "2021-04-23 16:21:35"
        '''

        # Every equipment have a unique key.
        response_dict = {'code': 200, 'message': 'ok', 'data': []}
        try:
            sensor = self.get_sensor_by_key(request.data['key'])
        except:
            response_dict['code'] = 400
            response_dict['message'] = 'Useless key'
            return Response(response_dict, status=status.status.HTTP_400_BAD_REQUEST)

        serializer = DataSerializer(data=request.data)

        if serializer.is_valid():
            # Successfully created
            serializer.save(sensor=sensor)
            response_dict['code'] = 201
            return Response(response_dict, status=status.HTTP_201_CREATED)

        response_dict['code'] = 422
        response_dict['message'] = serializer.errors
        return Response(response_dict, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class SensorViewSet(GenericViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = (IsAuthenticated,)

    @ action(methods=['post'], detail=False, url_path='create', permission_classes=[IsAdminUser])
    def create_sensor(self, request, version, format=None):
        '''
        Create a new Equipment through post.
        Example:
            "name": "test1"
            "name_brief": "t1"
            "type": "T"
            "descript": "this is a test sensor."
            "equipment": "{"id": "4"}"
        Return:
            if success, return sensor's information.
        '''

        # Every equipment have a unique key.
        key = get_random_secret_key()
        while Sensor.objects.filter(key=key):
            key = get_random_secret_key()

        serializer = self.get_serializer(data=request.data)

        response_dict = {'code': 200, 'message': 'ok', 'data': []}
        if serializer.is_valid():
            # Successfully created
            serializer.save(key=key)
            response_dict['code'] = 201
            response_dict['message'] = 'Created successfully'
            response_dict['data'] = serializer.data
            return Response(response_dict, status=status.HTTP_201_CREATED)

        response_dict['code'] = 422
        response_dict['message'] = serializer.errors
        return Response(response_dict, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    @ action(methods=['get'], detail=True, url_path='info', permission_classes=[IsAuthenticated])
    def get(self, request, version, pk, format=None):
        response_dict = {'code': 200, 'message': 'ok', 'data': []}
        sensor = self.get_object()
        serializer = self.get_serializer(sensor)
        response_dict['message'] = 'Success'
        response_dict['data'] = serializer.data
        return Response(response_dict)

    @ action(methods=['put'], detail=True, url_path='modifyinfo', permission_classes=[IsAdminUser])
    def put(self, request, version, pk, format=None):
        '''
        Update sensor's infomation.
        Example:
                "name": "test1",
                "name_brief": "t123",
                "type": "RE",
                "descript": "test1",
                "equipment": "{"id": "4"}"
        Return:
            All sensor's infomation.
        '''

        response_dict = {'code': 200, 'message': 'ok', 'data': []}
        sensor = self.get_object()
        serializer = self.get_serializer(sensor)

        if sensor.name != request.data['name'] and self.get_queryset().filter(name=request.data['name']):
            response_dict['code'] = 400
            response_dict['message'] = 'Existing name'
            return Response(data=response_dict, status=status.HTTP_400_BAD_REQUEST)
        serializer.update(sensor, request.data, modifier=request.user)
        response_dict['code'] = 201
        response_dict['message'] = 'Updated successfully'
        response_dict['data'] = serializer.data
        return Response(response_dict)
