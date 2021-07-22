from account.serializers import UserRecordSerializer, UserSerializer, UserDetailSerializer
from compostlab.utils.pagination import RecordPagination

from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import User
import django_filters.rest_framework
from rest_framework import filters
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


class UserViewSet(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = RecordPagination
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,
                       filters.OrderingFilter, filters.SearchFilter,)
    filter_fields = ('id', 'username', 'email', 'is_active',
                     'is_staff', 'is_superuser', 'date_joined')
    ordering_fields = ('id', 'name', 'date_joined')
    search_fields = ('id', 'name', 'email')

    @ action(methods=['post'], detail=False, url_path='register', permission_classes=[IsAdminUser])
    def create_user(self, request, version, format=None):
        '''
        Create a new account through post.
        Example:
            "username": "test1"
            "email": "test1@example.com"
            "password": "test123"
            "is_active": "true"
            "is_staff": "false"
            "is_superuser": "false"
        Return:
            if success, return user's profile.
        '''

        response_dict = {'code': 200, 'message': 'ok', 'data': []}
        serializer = UserDetailSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            response_dict['code'] = 201
            response_dict['message'] = 'Created successfully'
            response_dict['data'] = serializer.data
            return Response(data=response_dict, status=status.HTTP_201_CREATED)
        response_dict['code'] = 422
        response_dict['message'] = serializer.errors
        return Response(data=response_dict, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    @ action(methods=['get'], detail=False, url_path='mine')
    def get_myself(self, request, version, format=None):
        response_dict = {'code': 200, 'message': 'ok', 'data': []}
        user = request.user
        serializer = UserDetailSerializer(user)
        response_dict['message'] = 'Success'
        response_dict['data'] = serializer.data
        return Response(data=response_dict, status=status.HTTP_200_OK)

    @ action(methods=['get'], detail=True, url_path='detail')
    def get(self, request, version, pk, format=None):
        response_dict = {'code': 200, 'message': 'ok', 'data': []}
        user = self.get_object()
        serializer = UserDetailSerializer(user)
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

    @ action(methods=['put'], detail=False, url_path='update')
    def update(self, request, version, format=None):
        response_dict = {'code': 200, 'message': 'ok', 'data': []}
        serializer = UserDetailSerializer(request.user)
        if request.data['username'] != request.user.username and self.get_queryset().filter(username=request.data['username']):
            response_dict['code'] = 400
            response_dict['message'] = 'Existing username'
            return Response(data=response_dict, status=status.HTTP_400_BAD_REQUEST)
        serializer.update(request.user, request.data)
        response_dict['message'] = 'Updated successfully'
        response_dict['data'] = serializer.data
        return Response(data=response_dict, status=status.HTTP_200_OK)

    @ action(methods=['get'], detail=False, url_path='logout')
    def log_out(self, request, version, format=None):
        '''
        Logout user.
        '''
        response_dict = {'code': 200, 'message': 'ok', 'data': []}
        logout(request)
        response_dict['message'] = 'Logout seccess'
        return Response(data=response_dict, status=status.HTTP_200_OK)

    @ action(methods=['post'], detail=False, url_path='changepassword')
    def change_password(self, request, version, format=None):
        '''
        Change user's password.
        '''
        response_dict = {'code': 200, 'message': 'ok', 'data': []}

        user = authenticate(
            username=request.user.username, password=request.data['password'])
        if request.user != user:
            response_dict['code'] = 400
            response_dict['message'] = 'Password error'
            return Response(data=response_dict, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(request.data['new_password'])
        user.save()

        serializer = UserDetailSerializer(user)
        response_dict['message'] = 'Success, please log in again'
        response_dict['data'] = serializer.data
        return Response(data=response_dict, status=status.HTTP_200_OK)

    @ action(methods=['get'], detail=False, url_path='record')
    def get_record(self, request, version, format=None):
        '''
        Show user's all record through get.
        Example:
            GET 127.0.0.1:8000/api/1.0/account/4/record/?page=1&size=3
        Return:
            All records of this user.
        '''

        response_dict = {'code': 200, 'message': 'ok', 'data': []}
        user = request.user
        userRecords = user.userrecord.all()
        page = RecordPagination()
        page_list = page.paginate_queryset(
            userRecords, request, view=self)
        serializer = UserRecordSerializer(page_list, many=True)

        response_dict['code'] = 200
        response_dict['message'] = 'Success'
        data_dict = {'list': serializer.data, 'pagination': {}}
        data_dict['pagination']['current_page'] = page.page.number
        data_dict['pagination']['num_pages'] = page.page.paginator.num_pages
        data_dict['pagination']['per_page'] = page.page.paginator.per_page
        data_dict['pagination']['total_size'] = len(userRecords)
        response_dict['data'] = data_dict

        return Response(data=response_dict, status=status.HTTP_200_OK)
