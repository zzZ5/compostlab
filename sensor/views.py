import datetime
import hashlib
import random
import time

from compostlab.utils.pagination import RecordPagination
from data.serializers import DataSerializer
from experiment.models import Experiment
from sensor.models import Sensor
from sensor.serializers import SensorSerializer, SensorRecordSerializer

from rest_framework import status
from rest_framework.decorators import action, api_view
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
        return Response(data=response_dict, status=status.HTTP_200_OK)

    @ action(methods=['get'], detail=False, url_path='list', permission_classes=[IsAuthenticated])
    def get_list(self, request, version, format=None):
        '''
        Show all equipments through get.
        Example:
            GET 127.0.0.1:8000/api/1.0/equipment/list/?page=1&size=5
        Return:
            All equipments's information.
        '''
        response_dict = {'code': 200, 'message': 'ok', 'data': []}
        sensors = self.get_queryset()

        # paginate
        page = RecordPagination()
        page_list = page.paginate_queryset(
            sensors, request, view=self)
        serializer = self.get_serializer(page_list, many=True)

        response_dict['code'] = 200
        response_dict['message'] = 'Success'
        data_dict = {'list': serializer.data, 'pagination': {}}
        data_dict['pagination']['current_page'] = page.page.number
        data_dict['pagination']['num_pages'] = page.page.paginator.num_pages
        data_dict['pagination']['per_page'] = page.page.paginator.per_page
        data_dict['pagination']['total_size'] = len(sensors)
        response_dict['data'] = data_dict
        return Response(data=response_dict, status=status.HTTP_200_OK)

    @ action(methods=['get'], detail=True, url_path='record', permission_classes=[IsAuthenticated])
    def get_record(self, request, version, pk, format=None):
        '''
        Show sensor's all Record through get.
        Example:
            GET 127.0.0.1:8000/api/1.0/sensor/4/record/?page=1&size=3
        Return:
            All records of this equipments.
        '''

        response_dict = {'code': 200, 'message': 'ok', 'data': []}
        sensor = self.get_object()
        sensorRecords = sensor.sensorrecord.all()

        page = RecordPagination()
        page_list = page.paginate_queryset(
            sensorRecords, request, view=self)
        serializer = SensorRecordSerializer(page_list, many=True)

        response_dict['code'] = 200
        response_dict['message'] = 'Success'
        data_dict = {'list': serializer.data, 'pagination': {}}
        data_dict['pagination']['current_page'] = page.page.number
        data_dict['pagination']['num_pages'] = page.page.paginator.num_pages
        data_dict['pagination']['per_page'] = page.page.paginator.per_page
        data_dict['pagination']['total_size'] = len(sensorRecords)
        response_dict['data'] = data_dict
        return Response(data=response_dict, status=status.HTTP_200_OK)

    @ action(methods=['put'], detail=True, url_path='modifyinfo', permission_classes=[IsAdminUser])
    def put(self, request, version, pk, format=None):
        '''
        Update sensor's information.
        Example:
                "name": "test1",
                "name_brief": "t123",
                "type": "RE",
                "descript": "test1",
                "equipment": "{"id": "4"}"
        Return:
            All sensor's information.
        '''

        response_dict = {'code': 200, 'message': 'ok', 'data': []}
        sensor = self.get_object()
        serializer = self.get_serializer(sensor)

        if sensor.name != request.data['name'] and self.get_queryset().filter(name=request.data['name']):
            response_dict['code'] = 400
            response_dict['message'] = 'Existing name'
            return Response(data=response_dict, status=status.HTTP_400_BAD_REQUEST)
        serializer.update(sensor, request.data, modifier=request.user)
        response_dict['code'] = 200
        response_dict['message'] = 'Updated successfully'
        response_dict['data'] = serializer.data
        return Response(data=response_dict, status=status.HTTP_200_OK)

    @ action(methods=['get'], detail=True, url_path='data', permission_classes=[IsAuthenticated])
    def get_data(self, request, version, pk, format=None):
        '''
        Get data of this sensor(important).
        '''

        response_dict = {'code': 200, 'message': 'ok', 'data': []}
        sensor = self.get_object()

        experiment_id = request.query_params.get('experiment')
        experiment = Experiment.objects.get(pk=experiment_id)
        if experiment.status <= 0:
            response_dict['code'] = 403
            response_dict['message'] = 'Access prohibited due to status of this experiment'
            return Response(data=response_dict, status=status.HTTP_403_FORBIDDEN)
        if sensor.equipment not in experiment.equipment.all():
            response_dict['code'] = 403
            response_dict['message'] = 'Access prohibited because the sensor is not in this experiment'
            return Response(data=response_dict, status=status.HTTP_403_FORBIDDEN)
        if request.user not in experiment.user.all() and request.user != experiment.owner:
            response_dict['code'] = 403
            response_dict['message'] = 'Access prohibited for this user'
            return Response(data=response_dict, status=status.HTTP_403_FORBIDDEN)

        if experiment.status == 1:
            if experiment.end_time < datetime.datetime.now():
                experiment.status = 2

        step = int(request.query_params.get('step')
                   ) if request.query_params.get('step') else 1
        begin_time = datetime.datetime.strptime(request.query_params.get(
            'begin_time'), "%Y-%m-%d %H:%M:%S") if request.query_params.get('begin_time') else experiment.begin_time
        end_time = datetime.datetime.strptime(request.query_params.get(
            'end_time'), "%Y-%m-%d %H:%M:%S") if request.query_params.get('end_time') else experiment.end_time
        count = int(request.query_params.get('count')
                    ) if request.query_params.get('count') else 0

        if begin_time < experiment.begin_time or end_time > experiment.end_time:
            response_dict['code'] = 403
            response_dict['message'] = 'Access prohibited for this datetime'
            return Response(data=response_dict, status=status.HTTP_403_FORBIDDEN)

        data_all = sensor.data.filter(
            measured_time__range=(begin_time, end_time))
        if count != 0:
            step = data_all.count() // count + 1
        datas = data_all[::step]

        serializer = DataSerializer(datas, many=True)
        response_dict['message'] = 'Success'
        response_dict['data'] = serializer.data
        return Response(data=response_dict, status=status.HTTP_200_OK)
