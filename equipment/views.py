import hashlib
import random
import time

from equipment.models import Equipment, EquipmentHistoricalRecord
from equipment.serializers import EquipmentSerializer, EquipmentHistoricalRecordSerializer
from rest_framework import permissions, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView


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


class RecordPagination(PageNumberPagination):
    page_size = 10
    # url/?page=1&size=5
    page_query_param = 'page'
    page_size_query_param = 'size'

    max_page_size = 100


class CreateEquipment(APIView):
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

    def _get_object(self, pk):
        try:
            return Equipment.objects.get(pk=pk)
        except Equipment.DoesNotExist:
            return None

    permission_classes = (permissions.IsAuthenticated,)
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer

    def get(self, request, version, pk, format=None):
        equipment = self._get_object(pk)
        serializer = EquipmentSerializer(equipment)
        return Response(serializer.data)

    def put(self, request, version, pk, *args, **kwargs):
        response_dict = {'code': 200, 'message': 'ok', 'data': {}}
        equipment = self._get_object(pk)

        if request.user.is_superuser or equipment.owner == request.user:
            serializer = EquipmentSerializer(equipment)
            serializer.update(equipment, request.data, modifier=request.user)
            response_dict['code'] = 201
            response_dict['message'] = 'Updated successfully!'
            response_dict['data'] = serializer.data
            return Response(response_dict)
        elif request.user in equipment.users.all():
            serializer = EquipmentSerializer(equipment)
            equipment_data = serializer.data
            equipment_data['name_brief'] = request.data['name_brief']
            equipment_data['descript'] = request.data['descript']
            serializer.update(equipment, equipment_data, modifier=request.user)
            response_dict['code'] = 201
            response_dict['message'] = 'Updated successfully!'
            response_dict['data'] = serializer.data
            return Response(response_dict)
        return Response(data={'detail': 'Inconsistent users'}, status=status.status.HTTP_400_BAD_REQUEST)


class EquipmentHistoricalRecordView(APIView):
    '''

    '''
    permission_classes = (permissions.IsAuthenticated,)

    def _get_object(self, pk):
        try:
            return Equipment.objects.get(pk=pk)
        except Equipment.DoesNotExist:
            return None

    def get(self, request, version, pk, format=None):
        response_dict = {'code': 200, 'message': 'ok', 'data': {}}
        equipment = self._get_object(pk)
        equipmentHistoricalRecords = equipment.equipmenthistoricalrecord_set.all()
        page = RecordPagination()
        page_list = page.paginate_queryset(
            equipmentHistoricalRecords, request, view=self)
        serializer = EquipmentHistoricalRecordSerializer(page_list, many=True)
        response_dict['code'] = 200
        response_dict['message'] = 'Updated successfully!'
        response_dict['current_page'] = page.page.number
        response_dict['num_pages'] = page.page.paginator.num_pages
        response_dict['data'] = serializer.data
        return Response(response_dict)
