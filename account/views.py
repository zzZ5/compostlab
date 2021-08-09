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
    '''
    提供用户表相关接口。
    '''

    # 默认查询用户表
    queryset = User.objects.all()
    # 默认序列化类为用户序列化类
    serializer_class = UserSerializer
    # 默认需要已认证权限
    permission_classes = (IsAuthenticated,)
    # 默认的分页类为记录分页
    pagination_class = RecordPagination

    # 设置默认的筛选、排序、搜索标的。
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,
                       filters.OrderingFilter, filters.SearchFilter,)
    filter_fields = ('id', 'username', 'email', 'is_active',
                     'is_staff', 'is_superuser', 'date_joined')
    ordering_fields = ('id', 'name', 'date_joined')
    search_fields = ('id', 'name', 'email')

    @ action(methods=['post'], detail=False, url_path='register', permission_classes=[IsAdminUser])
    def create_user(self, request, version, format=None):
        '''
        通过post方法新建一个账户。

        Example:
            POST 127.0.0.1:8000/api/1.0/account/register/
            {
                "username": "test1"
                "email": "test1@example.com"
                "password": "test123"
                "is_active": "true"
                "is_staff": "false"
                "is_superuser": "false"
            }
        Return:
            如果新建成功，则返回账号信息。
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
        '''
        通过get方法获取当前已登陆账户的信息。
        Example:
            GET 127.0.0.1:8000/api/1.0/account/mine/
        Return:
            如果成功，则返回当前已登陆账号信息。
        '''

        response_dict = {'code': 200, 'message': 'ok', 'data': []}
        user = request.user
        serializer = UserDetailSerializer(user)
        response_dict['message'] = 'Success'
        response_dict['data'] = serializer.data
        return Response(data=response_dict, status=status.HTTP_200_OK)

    @ action(methods=['get'], detail=True, url_path='detail')
    def get(self, request, version, pk, format=None):
        '''
        通过get方法和账户的id获取账户的信息，需要提供账户id。
        Example:
            GET 127.0.0.1:8000/api/1.0/account/mine/
        Return:
            如果成功，则返回当前已登陆账号信息。
        '''

        response_dict = {'code': 200, 'message': 'ok', 'data': []}
        user = self.get_object()
        serializer = UserDetailSerializer(user)
        response_dict['message'] = 'Success'
        response_dict['data'] = serializer.data
        return Response(data=response_dict, status=status.HTTP_200_OK)

    @ action(methods=['put'], detail=False, url_path='update')
    def put(self, request, version, format=None):
        '''
        通过get方法和账户的id获取账户的信息，需要提供账户id。
        Example:
            GET 127.0.0.1:8000/api/1.0/account/mine/
        Return:
            如果成功，则返回当前已登陆账号信息。
        '''

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
