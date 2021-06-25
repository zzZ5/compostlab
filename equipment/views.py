import datetime
import hashlib
import random
from sensor.models import Sensor
import time

from compostlab.utils.pagination import RecordPagination
from equipment.models import Equipment
from equipment.serializers import EquipmentDetailSerializer, EquipmentSerializer, EquipmentRecordSerializer
from experiment.models import Experiment
from data.serializers import DataSerializer
from sensor.serializers import SensorSerializer

import django_filters.rest_framework
from rest_framework import filters
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


def get_random_secret_key(length=10, allowed_chars=None, secret_key=None):
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


class EquipmentViewSet(GenericViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = RecordPagination
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,
                       filters.OrderingFilter, filters.SearchFilter,)
    filter_fields = ('id', 'name', 'abbreviation', 'type',
                     'descript', 'created_time')
    ordering_fields = ('id', 'name', 'created_time')
    search_fields = ('id', 'name', 'abbreviation', 'type',
                     'descript')

    @ action(methods=['post'], detail=False, url_path='create', permission_classes=[IsAdminUser])
    def create_equipment(self, request, version, format=None):
        '''
        Create a new Equipment through post.
        Example:
            "name": "test1"
            "abbreviation": "t1"
            "type": "RE"
            "descript": "this is a test equipment."
        Return:
            if success, return equipment's information.
        '''

        key = get_random_secret_key()
        while Equipment.objects.filter(key=key):
            key = get_random_secret_key()

        serializer = EquipmentDetailSerializer(data=request.data)

        response_dict = {'code': 200, 'message': 'ok', 'data': []}
        if serializer.is_valid():
            # Successfully created
            serializer.save(key=key)
            response_dict['code'] = 201
            response_dict['message'] = 'Created successfully'
            response_dict['data'] = serializer.data
            return Response(data=response_dict, status=status.HTTP_201_CREATED)

        response_dict['code'] = 422
        response_dict['message'] = serializer.errors
        return Response(data=response_dict, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    @ action(methods=['get'], detail=True, url_path='detail', permission_classes=[IsAuthenticated])
    def get(self, request, version, pk, format=None):
        response_dict = {'code': 200, 'message': 'ok', 'data': []}
        equipment = self.get_object()
        serializer = EquipmentDetailSerializer(equipment)
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
        queryset = self.get_queryset()
        equipments = self.filter_queryset(queryset)
        page_list = self.paginate_queryset(equipments)

        serializer = self.get_serializer(page_list, many=True)

        response_dict['code'] = 200
        response_dict['message'] = 'Success'
        data_dict = {'list': serializer.data, 'pagination': {}}
        data_dict['pagination']['current_page'] = self.paginator.page.number
        data_dict['pagination']['num_pages'] = self.paginator.page.paginator.num_pages
        data_dict['pagination']['per_page'] = self.paginator.page.paginator.per_page
        data_dict['pagination']['total_size'] = len(equipments)
        response_dict['data'] = data_dict

        return Response(data=response_dict, status=status.HTTP_200_OK)

    @ action(methods=['get'], detail=True, url_path='record', permission_classes=[IsAuthenticated])
    def get_record(self, request, version, pk, format=None):
        '''
        Show equipment's all Record through get.
        Example:
            GET 127.0.0.1:8000/api/1.0/equipment/4/record/?page=1&size=3
        Return:
            All records of this equipments.
        '''

        response_dict = {'code': 200, 'message': 'ok', 'data': []}
        equipment = self.get_object()
        equipmentRecords = equipment.equipmentrecord.all()

        page = RecordPagination()
        page_list = page.paginate_queryset(
            equipmentRecords, request, view=self)
        serializer = EquipmentRecordSerializer(page_list, many=True)

        response_dict['code'] = 200
        response_dict['message'] = 'Success'
        data_dict = {'list': serializer.data, 'pagination': {}}
        data_dict['pagination']['current_page'] = page.page.number
        data_dict['pagination']['num_pages'] = page.page.paginator.num_pages
        data_dict['pagination']['per_page'] = page.page.paginator.per_page
        data_dict['pagination']['total_size'] = len(equipmentRecords)
        response_dict['data'] = data_dict

        return Response(data=response_dict, status=status.HTTP_200_OK)

    @ action(methods=['put'], detail=True, url_path='update', permission_classes=[IsAdminUser])
    def put(self, request, version, pk, format=None):
        '''
        Update equpment's information.
        Example:
                "name": "test1",
                "abbreviation": "t123",
                "type": "RE",
                "descript": "test1",
        Return:
            All equipments's information.
        '''

        response_dict = {'code': 200, 'message': 'ok', 'data': []}
        equipment = self.get_object()
        serializer = EquipmentDetailSerializer(equipment)

        if equipment.name != request.data['name'] and self.get_queryset().filter(name=request.data['name']):
            response_dict['code'] = 400
            response_dict['message'] = 'Existing name'
            return Response(data=response_dict, status=status.HTTP_400_BAD_REQUEST)
        serializer.update(equipment, request.data, modifier=request.user)
        response_dict['code'] = 200
        response_dict['message'] = 'Updated successfully'
        response_dict['data'] = serializer.data
        return Response(response_dict, status=status.HTTP_200_OK)

    @ action(methods=['get'], detail=True, url_path='data', permission_classes=[IsAuthenticated])
    def get_data(self, request, version, pk, format=None):
        '''
        Get data of this sensor(important).
        Example:
            experiment:4    //所属实验
            step:2  //步长
            begin_time:2021-04-23 13:00:35  //开始时间
            end_time:2021-04-24 16:35:36    //结束时间
            count:3 //数据量，和步长冲突时优先数据量
        Return:
            Datas
        '''

        response_dict = {'code': 200, 'message': 'ok', 'data': []}
        equipment = self.get_object()

        experiment_id = request.query_params.get('experiment')
        experiment = Experiment.objects.get(pk=experiment_id)
        if experiment.status <= 0:
            response_dict['code'] = 403
            response_dict['message'] = 'Access prohibited due to status of this experiment'
            return Response(data=response_dict, status=status.HTTP_403_FORBIDDEN)
        if equipment not in experiment.equipment.all():
            response_dict['code'] = 403
            response_dict['message'] = 'Access prohibited because the exquipment is not in this experiment'
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

        data = []
        for sensor in equipment.sensor.all():
            temp = {}
            sensorSerializer = SensorSerializer(sensor)
            temp.update(sensorSerializer.data)
            data_all = sensor.data.filter(
                measured_time__range=(begin_time, end_time))
            if count != 0:
                step = data_all.count() // count + 1
            datas = data_all[::step]
            dataSerializer = DataSerializer(datas, many=True)
            temp.update({'data': dataSerializer.data})
            data.append(temp)

        response_dict['message'] = 'Success'
        response_dict['data'] = data
        return Response(data=response_dict, status=status.HTTP_200_OK)
