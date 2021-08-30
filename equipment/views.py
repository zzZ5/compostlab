import datetime
import hashlib
import json
import random
import numpy as np
import statsmodels.stats.api as sms
import time

from compostlab.utils.pagination import RecordPagination
from compostlab.utils.mqtt import Mqtt
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


class EquipmentViewSet(GenericViewSet):
    '''
    提供设备表相关接口。
    '''

    # 默认查询设备表
    queryset = Equipment.objects.all()
    # 默认序列化类为设备序列化类
    serializer_class = EquipmentSerializer
    # 默认需要已认证权限
    permission_classes = (IsAuthenticated,)
    # 默认的分页类为记录分页
    pagination_class = RecordPagination

    # 设置默认的筛选、排序、搜索标的。
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
        通过post方法新建一个设备。

        Example:
            POST 127.0.0.1:8000/api/1.0/equipment/create/
            {
                "name": "test1",
                "name_brief": "t1",
                "type": "RE",
                "descript": "this is a test equipment.",
                "sensor": [
                    1
                ]
            }
        Return:
            如果成功，返回该设备的信息。
        '''

        # 获取一个不重复的随机key。
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
        '''
        通过get方法和设备的id获取设备的信息，需要提供设备id。

        Example:
            GET 127.0.0.1:8000/api/1.0/equipment/1/detail/

        Return:
            如果成功，则返回设备信息。
        '''

        response_dict = {'code': 200, 'message': 'ok', 'data': []}
        equipment = self.get_object()
        serializer = EquipmentDetailSerializer(equipment)
        response_dict['message'] = 'Success'
        response_dict['data'] = serializer.data
        return Response(data=response_dict, status=status.HTTP_200_OK)

    @ action(methods=['get'], detail=False, url_path='list', permission_classes=[IsAuthenticated])
    def get_list(self, request, version, format=None):
        '''
        通过get方法获取所有设备的信息（分页获取）。

        Example:
            GET 127.0.0.1:8000/api/1.0/equipment/list/?page=1&size=5&ordering=-id

        Return:
            所有设备信息。
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
        通过get方法获取设备的所有修改记录（分页）。

        Example:
            GET 127.0.0.1:8000/api/1.0/equipment/4/record/?page=1&size=10

        Return:
            该设备的所有修改记录。
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
        通过put方法更新设备信息。

        Example:
            PUT 127.0.0.1:8000/api/1.0/equipment/4/update/
            {
                "name":"test1",
                "name_brief": "t1",
                "type": "RE",
                "descript": "test1-changed",
                "sensor": []
            }

        Return:
            最新的设备信息。
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
        获取设备内部传感器的所有数据信息.

        Example:
            GET 127.0.0.1:8000/api/1.0/equipment/4/data/

            parameters:
                experiment:4    //所属实验
                step:2  //步长
                begin_time:2021-04-23 13:00:35  //开始时间
                end_time:2021-04-24 16:35:36    //结束时间
                count:100 //数据量(可选)，和步长冲突时优先数据量
        Return:
            该设备的属于这个实验的全部数据。
        '''

        response_dict = {'code': 200, 'message': 'ok', 'data': {}}
        equipment = self.get_object()

        experiment_id = request.query_params.get('experiment')
        experiment = Experiment.objects.get(pk=experiment_id)

        # 先判断实验是否正在进行或已完成
        if experiment.status <= 0:
            response_dict['code'] = 403
            response_dict['message'] = 'Access prohibited due to status of this experiment'
            return Response(data=response_dict, status=status.HTTP_403_FORBIDDEN)

        # 判断该设备是否在该实验中
        if equipment not in experiment.equipment.all():
            response_dict['code'] = 403
            response_dict['message'] = 'Access prohibited because the exquipment is not in this experiment'
            return Response(data=response_dict, status=status.HTTP_403_FORBIDDEN)

        # 判断该用户是否有权限查看
        if request.user in experiment.user.all() or request.user == experiment.owner or request.user.is_superuser or request. user.is_staff:
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

            data_conf = []
            for i in range(len(data[0]['data'])):
                temp = []
                numbers = [j['data'][i]['value'] for j in data]
                temp.append(data[0]['data'][i]['measured_time'])
                mean = np.mean(numbers)
                temp.append(mean)
                conf = sms.DescrStatsW(numbers).tconfint_mean()
                temp.append(conf[0])
                temp.append(conf[1])
                data_conf.append(temp)
            serializer = EquipmentDetailSerializer(equipment)
            response_dict['data'] = serializer.data
            response_dict['data']['begin_time'] = begin_time.strftime(
                "%Y-%m-%d %H:%M:%S")
            response_dict['data']['end_time'] = end_time.strftime(
                "%Y-%m-%d %H:%M:%S")
            response_dict['message'] = 'Success'
            response_dict['data']['unit'] = data[0]['unit']
            response_dict['data']['data'] = data_conf
            return Response(data=response_dict, status=status.HTTP_200_OK)

        response_dict['code'] = 403
        response_dict['message'] = 'Access prohibited for this user'
        return Response(data=response_dict, status=status.HTTP_403_FORBIDDEN)

    @ action(methods=['post'], detail=True, url_path='cmd', permission_classes=[IsAuthenticated])
    def public_cmd(self, request, version, pk, format=None):
        '''
        发送指令给设备。

        Example:
            POST 127.0.0.1:8000/api/1.0/equipment/4/cmd/
            {
                experiment: 4    //所属实验
                cmd: reset
                heater: on
            }

        Return:
            成功与否。
        '''

        response_dict = {'code': 200, 'message': 'ok', 'data': []}
        equipment = self.get_object()
        data = request.data.copy()
        try:
            experiment_id = data.pop('experiment')
            experiment = Experiment.objects.get(pk=experiment_id)
        except:
            response_dict['code'] = 400
            response_dict['message'] = 'Error experiment'
            return Response(data=response_dict, status=status.HTTP_400_BAD_REQUEST)

        # 先判断实验是否正在进行或已完成
        if experiment.status <= 0:
            response_dict['code'] = 403
            response_dict['message'] = 'Access prohibited due to status of this experiment'
            return Response(data=response_dict, status=status.HTTP_403_FORBIDDEN)

        # 判断该设备是否在该实验中
        if equipment not in experiment.equipment.all():
            response_dict['code'] = 403
            response_dict['message'] = 'Access prohibited because the exquipment is not in this experiment'
            return Response(data=response_dict, status=status.HTTP_403_FORBIDDEN)

        # 判断该用户是否有权限查看
        if request.user in experiment.user.all() or request.user == experiment.owner or request.user.is_superuser or request.user.is_staff:
            if experiment.status == 1:
                if experiment.end_time < datetime.datetime.now():
                    experiment.status = 2
            equipmentKey = equipment.key
            # 创建一个Mqtt对象，该Mqtt对象为单例模式，只会存在一个对象。
            mqtt = Mqtt()
            # 发送指令给设备
            try:
                mqtt.public_message(equipmentKey, json.dumps(data))
                response_dict['message'] = 'Success'
                # response_dict['data'] = data
                return Response(data=response_dict, status=status.HTTP_200_OK)
            except:
                response_dict['message'] = 'Error'
                response_dict['code'] = 404
                return Response(data=response_dict, status=status.HTTP_404_NOT_FOUND)

        response_dict['code'] = 403
        response_dict['message'] = 'Access prohibited for this user'
        return Response(data=response_dict, status=status.HTTP_403_FORBIDDEN)
