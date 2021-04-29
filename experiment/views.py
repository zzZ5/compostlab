from compostlab.utils.pagination import RecordPagination
from equipment.models import Equipment
from equipment.serializers import EquipmentSerializer, EquipmentRecordSerializer

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


class ExperimentViewSet(GenericViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    permission_classes = (IsAuthenticated,)

    @ action(methods=['post'], detail=False, url_path='create', permission_classes=[IsAdminUser])
    def create_equipment(self, request, version, format=None):
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

        serializer = self.get_serializer(data=request.data)

        response_dict = {'code': 200, 'message': 'ok', 'data': []}
        if serializer.is_valid():
            # Successfully created
            serializer.save()
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
        equipment = self.get_object()
        serializer = EquipmentSerializer(equipment)
        response_dict['message'] = 'Success'
        response_dict['data'] = serializer.data
        return Response(response_dict)

    @ action(methods=['get'], detail=False, url_path='list', permission_classes=[IsAuthenticated])
    def get_list(self, request, version, format=None):
        '''
        Show all equipments through get.
        Example:
            GET 127.0.0.1:8000/api/1.0/equipment/list/?page=1&size=5
        Return:
            All equipments's infomation.
        '''
        response_dict = {'code': 200, 'message': 'ok', 'data': []}
        equipments = self.get_queryset()

        # paginate
        page = RecordPagination()
        page_list = page.paginate_queryset(
            equipments, request, view=self)
        serializer = self.get_serializer(page_list, many=True)

        response_dict['code'] = 200
        response_dict['message'] = 'Success'
        response_dict['current_page'] = page.page.number
        response_dict['num_pages'] = page.page.paginator.num_pages
        response_dict['per_page'] = page.page.paginator.per_page
        response_dict['total_size'] = len(equipments)
        response_dict['data'] = serializer.data
        return Response(response_dict)

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
        response_dict['current_page'] = page.page.number
        response_dict['num_pages'] = page.page.paginator.num_pages
        response_dict['per_page'] = page.page.paginator.per_page
        response_dict['total_size'] = len(equipmentRecords)
        response_dict['data'] = serializer.data
        return Response(response_dict)

    @ action(methods=['put'], detail=True, url_path='modifyinfo', permission_classes=[IsAdminUser])
    def put(self, request, version, pk, format=None):
        '''
        Update equpment's infomation.
        Example:
                "name": "test1",
                "name_brief": "t123",
                "type": "RE",
                "descript": "test1",
        Return:
            All equipments's infomation.
        '''

        response_dict = {'code': 200, 'message': 'ok', 'data': []}
        equipment = self.get_object()
        serializer = self.get_serializer(equipment)

        if equipment.name != request.data['name'] and self.get_queryset().filter(name=request.data['name']):
            response_dict['code'] = 400
            response_dict['message'] = 'Existing name'
            return Response(data=response_dict, status=status.HTTP_400_BAD_REQUEST)
        serializer.update(equipment, request.data, modifier=request.user)
        response_dict['code'] = 201
        response_dict['message'] = 'Updated successfully'
        response_dict['data'] = serializer.data
        return Response(response_dict)