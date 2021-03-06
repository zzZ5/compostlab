import datetime
import hashlib
import random
import time

from compostlab.utils.pagination import RecordPagination
from data.serializers import DataSerializer
from experiment.models import Experiment
from sensor.models import Sensor
from sensor.serializers import SensorSerializer, SensorRecordSerializer

import django_filters.rest_framework
from rest_framework import filters
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


def get_random_secret_key(length=15, allowed_chars=None, secret_key=None):
    '''
    创建一串随机字符串。

    Args:
        length(int): 随机字符串长度。
        allowed_chars(string): 随机字符串的范围。
        secret_key(string): 随机字符串种子。
    Return:
        string: 随机字符串。.
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
    '''
    提供传感器表相关接口。
    '''

    # 默认查询传感器表
    queryset = Sensor.objects.all()
    # 默认序列化类为传感器序列化类
    serializer_class = SensorSerializer
    # 默认需要已认证权限
    permission_classes = (IsAuthenticated,)
    # 默认的分页类为记录分页
    pagination_class = RecordPagination

    # 设置默认的筛选、排序、搜索标的。
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,
                       filters.OrderingFilter, filters.SearchFilter,)
    filter_fields = ('id', 'name', 'abbreviation', 'key',
                     'type', 'descript', 'equipment', 'created_time')
    ordering_fields = ('id', 'name', 'created_time')
    search_fields = ('name', 'abbreviation', 'descript')

    @ action(methods=['post'], detail=False, url_path='create', permission_classes=[IsAdminUser])
    def create_sensor(self, request, version, format=None):
        '''
        通过post方法创建一个传感器，需要管理员权限。

        Example:
            {
                "name": "test1"
                "abbreviation": "t1"
                "type": "T"
                "descript": "this is a test sensor."
                "equipment": "{"id": "4"}"
            }

        Return:
            如果成功返回该传感器的信息。
        '''

        # 每一个传感器都有一个唯一key。
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

    @ action(methods=['get'], detail=True, url_path='detail', permission_classes=[IsAuthenticated])
    def get(self, request, version, pk, format=None):
        '''
        通过get方法和传感器的id获取传感器的信息，需要提供传感器id。

        Example:
            GET 127.0.0.1:8000/api/1.0/sensor/1/detail/

        Return:
            如果成功，则返回传感器信息。
        '''

        response_dict = {'code': 200, 'message': 'ok', 'data': []}
        sensor = self.get_object()
        serializer = self.get_serializer(sensor)
        response_dict['message'] = 'Success'
        response_dict['data'] = serializer.data
        return Response(data=response_dict, status=status.HTTP_200_OK)

    @ action(methods=['get'], detail=False, url_path='list', permission_classes=[IsAuthenticated])
    def get_list(self, request, version, format=None):
        '''
        通过get方法获取所有传感器的信息（分页获取）。

        Example:
            GET 127.0.0.1:8000/api/1.0/sensor/list/?page=1&size=5&ordering=-id

        Return:
            所有传感器信息。
        '''

        response_dict = {'code': 200, 'message': 'ok', 'data': []}
        queryset = self.get_queryset()
        sensors = self.filter_queryset(queryset)
        page_list = self.paginate_queryset(sensors)
        serializer = self.get_serializer(page_list, many=True)

        response_dict['code'] = 200
        response_dict['message'] = 'Success'
        data_dict = {'list': serializer.data, 'pagination': {}}
        data_dict['pagination']['current_page'] = self.paginator.page.number
        data_dict['pagination']['num_pages'] = self.paginator.page.paginator.num_pages
        data_dict['pagination']['per_page'] = self.paginator.page.paginator.per_page
        data_dict['pagination']['total_size'] = len(sensors)
        response_dict['data'] = data_dict

        return Response(data=response_dict, status=status.HTTP_200_OK)

    @ action(methods=['get'], detail=True, url_path='record', permission_classes=[IsAuthenticated])
    def get_record(self, request, version, pk, format=None):
        '''
        通过get方法获取传感器的所有修改记录（分页）。

        Example:
            GET 127.0.0.1:8000/api/1.0/sensor/1/record/?page=1&size=10

        Return:
            该传感器的所有修改记录。
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

    @ action(methods=['put'], detail=True, url_path='update', permission_classes=[IsAdminUser])
    def put(self, request, version, pk, format=None):
        '''
        通过put方法更新传感器信息。

        Example:
            PUT 127.0.0.1:8000/api/1.0/equipment/4/update/
            {
                "name": "test1",
                "abbreviation": "t123",
                "type": "RE",
                "descript": "test1",
                "equipment": "{"id": "4"}"
            }

        Return:
            最新的传感器信息。
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
        通过get方法该传感器的数据，需要传感器id.

        Example:
            GET 127.0.0.1:8000/api/1.0/sensor/4/data/
            experiment:4    //所属实验
            step:2  //步长
            begin_time:2021-04-23 13:00:35  //开始时间
            end_time:2021-04-24 16:35:36    //结束时间

        Return:
            该传感器的数据
        '''

        response_dict = {'code': 200, 'message': 'ok', 'data': []}
        sensor = self.get_object()

        experiment_id = request.query_params.get('experiment')
        experiment = Experiment.objects.get(pk=experiment_id)

        # 先判断实验是否正在进行或已完成
        if experiment.status <= 0:
            response_dict['code'] = 403
            response_dict['message'] = 'Access prohibited due to status of this experiment'
            return Response(data=response_dict, status=status.HTTP_403_FORBIDDEN)

        # 判断传感器所属设备是否在这个实验中
        if sensor.equipment not in experiment.equipment.all():
            response_dict['code'] = 403
            response_dict['message'] = 'Access prohibited because the sensor is not in this experiment'
            return Response(data=response_dict, status=status.HTTP_403_FORBIDDEN)

        # 判断用户是否有权限
        if request.user in experiment.user.all() or request.user == experiment.owner or request.user.is_superuser or request.user.is_staff:
            # 调整实验状态
            if experiment.status == 1:
                if experiment.end_time < datetime.datetime.now():
                    experiment.status = 2

            step = int(request.query_params.get('step')
                       ) if request.query_params.get('step') else 1
            begin_time = datetime.datetime.strptime(request.query_params.get(
                'begin_time'), "%Y-%m-%d %H:%M:%S") if request.query_params.get('begin_time') else experiment.begin_time
            end_time = datetime.datetime.strptime(request.query_params.get(
                'end_time'), "%Y-%m-%d %H:%M:%S") if request.query_params.get('end_time') else experiment.end_time

            if begin_time < experiment.begin_time or end_time > experiment.end_time:
                response_dict['code'] = 403
                response_dict['message'] = 'Access prohibited for this datetime'
                return Response(data=response_dict, status=status.HTTP_403_FORBIDDEN)

            data_all = sensor.data.filter(
                measured_time__range=(begin_time, end_time))
            datas = data_all[::step]
            sensorSerializer = self.get_serializer(sensor)
            page_list = self.paginate_queryset(datas)
            serializer = DataSerializer(page_list, many=True)
            response_dict['message'] = 'Success'
            data_dict = {'list': serializer.data, 'pagination': {}}
            data_dict.update(sensorSerializer.data)
            data_dict['pagination']['current_page'] = self.paginator.page.number
            data_dict['pagination']['num_pages'] = self.paginator.page.paginator.num_pages
            data_dict['pagination']['per_page'] = self.paginator.page.paginator.per_page
            data_dict['pagination']['total_size'] = len(datas)
            response_dict['data'] = data_dict
            return Response(data=response_dict, status=status.HTTP_200_OK)

        response_dict['code'] = 403
        response_dict['message'] = 'Access prohibited for this user'
        return Response(data=response_dict, status=status.HTTP_403_FORBIDDEN)
