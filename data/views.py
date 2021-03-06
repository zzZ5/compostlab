from data.models import Data
from data.serializers import DataSerializer

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


class DataViewSet(GenericViewSet):
    '''
    提供数据表相关接口。
    '''

    queryset = Data.objects.all()
    serializer_class = DataSerializer
    permission_classes = (IsAuthenticated,)

    @ action(methods=['post'], detail=False, url_path='upload', permission_classes=[AllowAny])
    def upload_data(self, request, version, format=None):
        '''
        通过post新建一个数据.

        Example:
            {
                "value": "25.0"
                "unit": "℃"
                "key": "Sensor's key"
                "measured_time": "2021-04-23 16:21:35"
            }

        Return:
            如果新建成功，返回数据信息。
        '''

        response_dict = {'code': 200, 'message': 'ok', 'data': []}

        if "data" in request.data:
            serializer = DataSerializer(data=request.data['data'], many=True)
        else:
            serializer = DataSerializer(data=request.data)

        if serializer.is_valid():
            # Successfully created
            serializer.save()
            response_dict['code'] = 201
            response_dict['message'] = "success"
            response_dict['data'] = serializer.data
            return Response(data=response_dict, status=status.HTTP_201_CREATED)
        response_dict['code'] = 422
        response_dict['message'] = serializer.errors
        return Response(data=response_dict, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
