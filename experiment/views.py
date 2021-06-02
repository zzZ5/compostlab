from compostlab.utils.pagination import RecordPagination
from experiment.models import Experiment
from experiment.serializers import ExperimentDetailSerializer, ExperimentSerializer

import django_filters.rest_framework
from rest_framework import filters
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


class ExperimentViewSet(GenericViewSet):
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = RecordPagination
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,
                       filters.OrderingFilter, filters.SearchFilter,)
    filter_fields = ('id', 'name', 'site', 'descript', 'begin_time',
                     'end_time', 'user', 'owner', 'status', 'created_time')
    ordering_fields = ('id', 'name', 'created_time')
    search_fields = ('name', 'site', 'descript')

    @ action(methods=['post'], detail=False, url_path='create', permission_classes=[IsAuthenticated])
    def create_experiment(self, request, version, format=None):
        '''
        Create a new Experiment through post.
        Example:
            "name": "test1"
            "site": "研究院"
            "descript": "this is a test equipment."
            "equipment": "[1 ]"
            "begin_time" : "2021-04-16 13:41:35"
            "end_time" : "2021-05-16 13:40:35"
            "user" : [1, 2]
            "owner" : 1
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
        return Response(data=response_dict, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    @ action(methods=['get'], detail=False, url_path='list', permission_classes=[IsAuthenticated])
    def get_list(self, request, version, format=None):
        '''
        Show all equipments through get.
        Example:
            GET 127.0.0.1:8000/api/1.0/experiment/list/?page=1&size=5
        Return:
            All equipments's information.
        '''
        response_dict = {'code': 200, 'message': 'ok', 'data': []}
        queryset = self.get_queryset()
        experiments = self.filter_queryset(queryset)
        page_list = self.paginate_queryset(experiments)
        serializer = self.get_serializer(page_list, many=True)

        response_dict['code'] = 200
        response_dict['message'] = 'Success'
        data_dict = {'list': serializer.data, 'pagination': {}}
        data_dict['pagination']['current_page'] = self.paginator.page.number
        data_dict['pagination']['num_pages'] = self.paginator.page.paginator.num_pages
        data_dict['pagination']['per_page'] = self.paginator.page.paginator.per_page
        data_dict['pagination']['total_size'] = len(experiments)
        response_dict['data'] = data_dict

        return Response(data=response_dict, status=status.HTTP_200_OK)

    @ action(methods=['get'], detail=False, url_path='use', permission_classes=[IsAuthenticated])
    def get_use(self, request, version, format=None):
        response_dict = {'code': 200, 'message': 'ok', 'data': []}
        experiment = request.user.experiment_use
        serializer = self.get_serializer(experiment, many=True)
        response_dict['message'] = 'Success'
        response_dict['data'] = serializer.data
        return Response(data=response_dict, status=status.HTTP_200_OK)

    @ action(methods=['get'], detail=False, url_path='own', permission_classes=[IsAuthenticated])
    def get_own(self, request, version, format=None):
        response_dict = {'code': 200, 'message': 'ok', 'data': []}
        experiment = request.user.experiment_own
        serializer = self.get_serializer(experiment, many=True)
        response_dict['message'] = 'Success'
        response_dict['data'] = serializer.data
        return Response(data=response_dict, status=status.HTTP_200_OK)

    @ action(methods=['get'], detail=True, url_path='detail', permission_classes=[IsAuthenticated])
    def get(self, request, version, pk, format=None):
        # to judge whether this user can view this experiment or not(just owner or user qualified)
        response_dict = {'code': 200, 'message': 'ok', 'data': []}
        experiment = self.get_object()
        if request.user in experiment.user.all() or request.user == experiment.owner or request.user.is_superuser or request.user.is_staff:
            serializer = ExperimentDetailSerializer(experiment)
            response_dict['message'] = 'Success'
            response_dict['data'] = serializer.data
            return Response(data=response_dict, status=status.HTTP_200_OK)
        else:
            response_dict['code'] = '403'
            response_dict['message'] = 'No access permission'
            return Response(data=response_dict, status=status.HTTP_403_FORBIDDEN)

    @ action(methods=['put'], detail=True, url_path='update', permission_classes=[IsAuthenticated])
    def put(self, request, version, pk, format=None):
        '''
        Update experiment's information.
        Example:
        {
            "name": "test2",
            "site": "t2",
            "descript": "test2",
            "equipment": [
                1
            ],
            "begin_time": "2021-05-6 13:00:35",
            "end_time": "2021-05-16 13:40:35",
            "user": [
                1,
                2
            ],
            "owner": 1
        }
        Return:
            Expeiment's information.
        '''

        response_dict = {'code': 200, 'message': 'ok', 'data': []}
        experiment = self.get_object()
        serializer = self.get_serializer(experiment)

        if request.user == experiment.owner or request.user.is_superuser or request.user.is_staff:
            if experiment.name != request.data['name'] and self.get_queryset().filter(name=request.data['name']):
                response_dict['code'] = 400
                response_dict['message'] = 'Existing name'
                return Response(data=response_dict, status=status.HTTP_400_BAD_REQUEST)
            serializer.update(experiment, request.data, modifier=request.user)
            response_dict['code'] = 200
            response_dict['message'] = 'Updated successfully'
            response_dict['data'] = serializer.data
            return Response(data=response_dict, status=status.HTTP_200_OK)
        else:
            response_dict['code'] = '403'
            response_dict['message'] = 'No access permission'
            return Response(data=response_dict, status=status.HTTP_403_FORBIDDEN)
