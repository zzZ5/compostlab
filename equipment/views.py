import hashlib
import random
import time

from equipment.models import Equipment
from equipment.serializers import EquipmentSerializer, EquipmentHistoricalRecordSerializer
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


def _get_random_secret_key(length=15, allowed_chars=None, secret_key=None):
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


class RecordPagination(PageNumberPagination):
    """
    Generate a custom definition pagination.
    """

    page_size = 10
    # url/?page=1&size=5
    page_query_param = 'page'
    page_size_query_param = 'size'

    max_page_size = 100


class EquipmentCreate(APIView):
    '''
    Create a new Equipment, must have administrator privileges.
    '''

    permission_classes = (IsAdminUser,)

    def post(self, request, version, format=None):
        '''
        Create a new Equipment through post.
        Example:
            "name": "test1"
            "name_brief": "t1"
            "type": "RE"
            "descript": "this is a test equipment."
        Return:
            if success, return equipment's information.
        '''

        # Every equipment have a unique key.
        key = _get_random_secret_key()
        while Equipment.objects.filter(key=key):
            key = _get_random_secret_key()

        serializer = EquipmentSerializer(data=request.data)

        response_dict = {'code': 200, 'message': 'ok', 'data': []}
        if serializer.is_valid():
            # Successfully created
            serializer.save(owner=self.request.user, key=key)
            response_dict['code'] = 201
            response_dict['message'] = 'Created successfully'
            response_dict['data'] = serializer.data
            return Response(response_dict, status=status.HTTP_201_CREATED)

        response_dict['code'] = 422
        response_dict['message'] = serializer.errors
        return Response(response_dict, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class EquipmentList(APIView):
    '''
    Show all equipments.
    '''

    permission_classes = (IsAuthenticated,)

    def get(self, request, version, format=None):
        '''
        Show all equipments through get.
        Example:
            GET 127.0.0.1:8000/api/1.0/equipment/list/?page=1&size=5
        Return:
            All equipments's infomation.
        '''
        response_dict = {'code': 200, 'message': 'ok', 'data': []}
        equipments = Equipment.objects.all()

        # paginate
        page = RecordPagination()
        page_list = page.paginate_queryset(
            equipments, request, view=self)
        serializer = EquipmentSerializer(page_list, many=True)

        response_dict['code'] = 200
        response_dict['message'] = 'Success'
        response_dict['current_page'] = page.page.number
        response_dict['num_pages'] = page.page.paginator.num_pages
        response_dict['page_size'] = page.page_size
        response_dict['data'] = serializer.data

        return Response(response_dict)


class EquipmentDetail(APIView):
    '''
    Get or update  equipment's information through equipment's id.
    '''

    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Equipment.objects.get(pk=pk)
        except Equipment.DoesNotExist:
            return None

    def get(self, request, version, pk, format=None):
        response_dict = {'code': 200, 'message': 'ok', 'data': []}
        equipment = self.get_object(pk)
        serializer = EquipmentSerializer(equipment)
        response_dict['message'] = 'Success'
        response_dict['data'] = serializer.data
        return Response(response_dict)

    def put(self, request, version, pk, *args, **kwargs):
        '''
        Update equpment's infomation.
        Example:
                "name": "test1",
                "name_brief": "t123",
                "key": "CKNW6CsWcyApqYs",
                "type": "RE",
                "descript": "test1",
                "begin_time": null,
                "end_time": null,
                "users": [
                    {
                        "id": 4
                    },
                    {
                        "id": 6
                    }
                ],
                "owner": {
                    "id": 4,
                    "username": "test1",
                    "email": "test1@example.com"
                }
        Return:
            All equipments's infomation.
        '''

        response_dict = {'code': 200, 'message': 'ok', 'data': []}
        equipment = self.get_object(pk)

        # Superuser or this equipment's owner can change every info except id of this equipment.
        if request.user.is_superuser or equipment.owner == request.user:
            serializer = EquipmentSerializer(equipment)
            serializer.update(equipment, request.data, modifier=request.user)
            response_dict['code'] = 201
            response_dict['message'] = 'Updated successfully'
            response_dict['data'] = serializer.data
            return Response(response_dict)

        # This equipment's user can change name_brief and descript of this equipment.
        elif request.user in equipment.users.all():
            serializer = EquipmentSerializer(equipment)
            equipment_data = serializer.data
            equipment_data['name_brief'] = request.data['name_brief']
            equipment_data['descript'] = request.data['descript']
            serializer.update(equipment, equipment_data, modifier=request.user)
            response_dict['code'] = 201
            response_dict['message'] = 'Updated successfully'
            response_dict['data'] = serializer.data
            return Response(response_dict)

        # Other user have no permissions.
        response_dict['code'] = 400
        response_dict['message'] = 'No permissions'
        return Response(response_dict, status=status.status.HTTP_400_BAD_REQUEST)


class EquipmentHistoricalRecordView(APIView):
    '''
    Show all HistoricalRecord of this equipment. 
    '''
    permission_classes = (IsAuthenticated,)

    def _get_equipment_object(self, pk):
        try:
            return Equipment.objects.get(pk=pk)
        except Equipment.DoesNotExist:
            return None

    def get(self, request, version, pk, format=None):
        '''
        Show equipment's all HistoricalRecord through get.
        Example:
            GET 127.0.0.1:8000/api/1.0/equipment/historicalRecord/4/?page=1&size=3
        Return:
            All records of this equipments..
        '''

        response_dict = {'code': 200, 'message': 'ok', 'data': []}
        equipment = self._get_equipment_object(pk)
        equipmentHistoricalRecords = equipment.equipmenthistoricalrecord_set.all()

        page = RecordPagination()
        page_list = page.paginate_queryset(
            equipmentHistoricalRecords, request, view=self)
        serializer = EquipmentHistoricalRecordSerializer(page_list, many=True)

        response_dict['code'] = 200
        response_dict['message'] = 'Success'
        response_dict['current_page'] = page.page.number
        response_dict['page_size'] = page.page_size
        response_dict['num_pages'] = page.page.paginator.num_pages
        response_dict['data'] = serializer.data
        return Response(response_dict)
