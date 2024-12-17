import datetime
import json


from compostlab.utils.pagination import RecordPagination
from compostlab.utils.mqtt import Mqtt

from equipment.models import Equipment
from experiment.models import Experiment
from experiment.serializers import (
    ExperimentDetailSerializer,
    ExperimentSerializer,
    ReviewSerializer,
)

import django_filters.rest_framework
from rest_framework import filters
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


class ExperimentViewSet(GenericViewSet):
    """
    提供实验表相关接口。
    """

    # 默认查询实验表
    queryset = Experiment.objects.all()
    # 默认序列化类为实验序列化类
    serializer_class = ExperimentSerializer
    # 默认需要已认证权限
    permission_classes = (IsAuthenticated,)
    # 默认的分页类为记录分页
    pagination_class = RecordPagination

    # 设置默认的筛选、排序、搜索标的。
    filter_backends = (
        django_filters.rest_framework.DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    )
    filter_fields = (
        "id",
        "name",
        "site",
        "descript",
        "begin_time",
        "end_time",
        "user",
        "owner",
        "status",
        "created_time",
    )
    ordering_fields = ("id", "name", "created_time")
    search_fields = ("name", "site", "descript")

    @action(
        methods=["post"],
        detail=False,
        url_path="create",
        permission_classes=[IsAuthenticated],
    )
    def create_experiment(self, request, version, format=None):
        """
        通过post方法新建一个实验。

        Example:
            POST 127.0.0.1:8000/api/1.0/experiment/create/
            {
                "name": "test4",
                "site": "t4",
                "descript": "test4",
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
            如果成功，返回该实验信息。
        """

        serializer = ExperimentDetailSerializer(data=request.data)

        response_dict = {"code": 200, "message": "ok", "data": []}
        if serializer.is_valid():
            # Successfully created
            serializer.save()
            response_dict["code"] = 201
            response_dict["message"] = "Created successfully"
            response_dict["data"] = serializer.data
            return Response(response_dict, status=status.HTTP_201_CREATED)

        response_dict["code"] = 422
        response_dict["message"] = serializer.errors
        return Response(data=response_dict, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    @action(
        methods=["get"],
        detail=False,
        url_path="list",
        permission_classes=[IsAuthenticated],
    )
    def get_list(self, request, version, format=None):
        """
        通过get方法获取所有实验简略信息（分页）。

        Example:
            GET 127.0.0.1:8000/api/1.0/experiment/list/?page=1&size=5

        Return:
            所有实验的信息。
        """
        response_dict = {"code": 200, "message": "ok", "data": []}
        queryset = self.get_queryset()
        experiments = self.filter_queryset(queryset)
        page_list = self.paginate_queryset(experiments)
        serializer = self.get_serializer(page_list, many=True)

        response_dict["code"] = 200
        response_dict["message"] = "Success"
        data_dict = {"list": serializer.data, "pagination": {}}
        data_dict["pagination"]["current_page"] = self.paginator.page.number
        data_dict["pagination"]["num_pages"] = self.paginator.page.paginator.num_pages
        data_dict["pagination"]["per_page"] = self.paginator.page.paginator.per_page
        data_dict["pagination"]["total_size"] = len(experiments)
        response_dict["data"] = data_dict

        return Response(data=response_dict, status=status.HTTP_200_OK)

    @action(
        methods=["get"],
        detail=False,
        url_path="use",
        permission_classes=[IsAuthenticated],
    )
    def get_use(self, request, version, format=None):
        """
        通过get方法获取所有自己所在实验的简略信息（分页）。

        Example:
            GET 127.0.0.1:8000/api/1.0/experiment/use/?page=1&size=5

        Return:
            所有自己所在实验的简略信息。
        """

        # TODO 将该方法和get_list()合并

        response_dict = {"code": 200, "message": "ok", "data": []}
        experiments = request.user.experiment_use
        page_list = self.paginate_queryset(experiments)
        serializer = self.get_serializer(page_list, many=True)

        response_dict["code"] = 200
        response_dict["message"] = "Success"
        data_dict = {"list": serializer.data, "pagination": {}}
        data_dict["pagination"]["current_page"] = self.paginator.page.number
        data_dict["pagination"]["num_pages"] = self.paginator.page.paginator.num_pages
        data_dict["pagination"]["per_page"] = self.paginator.page.paginator.per_page
        data_dict["pagination"]["total_size"] = len(experiments)
        response_dict["data"] = data_dict
        return Response(data=response_dict, status=status.HTTP_200_OK)

    @action(
        methods=["get"],
        detail=False,
        url_path="own",
        permission_classes=[IsAuthenticated],
    )
    def get_own(self, request, version, format=None):
        """
        通过get方法获取所有自己所创建实验的简略信息（分页）。

        Example:
            GET 127.0.0.1:8000/api/1.0/experiment/use/?page=1&size=5

        Return:
            所有自己所创建实验的简略信息。
        """

        # TODO 将该方法和get_list()合并

        response_dict = {"code": 200, "message": "ok", "data": []}
        experiments = request.user.experiment_own
        page_list = self.paginate_queryset(experiments)
        serializer = self.get_serializer(page_list, many=True)

        response_dict["code"] = 200
        response_dict["message"] = "Success"
        data_dict = {"list": serializer.data, "pagination": {}}
        data_dict["pagination"]["current_page"] = self.paginator.page.number
        data_dict["pagination"]["num_pages"] = self.paginator.page.paginator.num_pages
        data_dict["pagination"]["per_page"] = self.paginator.page.paginator.per_page
        data_dict["pagination"]["total_size"] = len(experiments)
        response_dict["data"] = data_dict
        return Response(data=response_dict, status=status.HTTP_200_OK)

    @action(
        methods=["get"],
        detail=True,
        url_path="detail",
        permission_classes=[IsAuthenticated],
    )
    def get(self, request, version, pk, format=None):
        """
        通过get方法获取单个实验的详细信息（需要提供实验id）。

        Example:
            GET 127.0.0.1:8000/api/1.0/experiment/2/detail/

        Return:
            实验的详细信息。
        """

        response_dict = {"code": 200, "message": "ok", "data": []}
        experiment = self.get_object()

        # 调整实验的状态
        if experiment.status == 1:
            if experiment.end_time < datetime.datetime.now():
                experiment.status = 2
                experiment.save()
        # 判断该用户是否可以查看该实验信息
        if (
            request.user in experiment.user.all()
            or request.user == experiment.owner
            or request.user.is_superuser
            or request.user.is_staff
        ):
            serializer = ExperimentDetailSerializer(experiment)
            response_dict["message"] = "Success"
            response_dict["data"] = serializer.data
            return Response(data=response_dict, status=status.HTTP_200_OK)
        else:
            response_dict["code"] = "403"
            response_dict["message"] = "No access permission"
            return Response(data=response_dict, status=status.HTTP_403_FORBIDDEN)

    @action(
        methods=["put"],
        detail=True,
        url_path="update",
        permission_classes=[IsAuthenticated],
    )
    def put(self, request, version, pk, format=None):
        """
        通过put方法修改实验信息。

        Example:
            PUT 127.0.0.1:8000/api/1.0/experiment/2/update/
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
                    1
                ],
                "owner": 1
            }
        Return:
            最新的实验信息。
        """

        response_dict = {"code": 200, "message": "ok", "data": []}
        experiment = self.get_object()
        serializer = ExperimentDetailSerializer(experiment)

        if (
            request.user == experiment.owner
            or request.user.is_superuser
            or request.user.is_staff
        ):
            if experiment.name != request.data["name"] and self.get_queryset().filter(
                name=request.data["name"]
            ):
                response_dict["code"] = 400
                response_dict["message"] = "Existing name"
                return Response(data=response_dict, status=status.HTTP_400_BAD_REQUEST)
            serializer.update(experiment, request.data, modifier=request.user)
            response_dict["code"] = 200
            response_dict["message"] = "Updated successfully"
            response_dict["data"] = serializer.data
            return Response(data=response_dict, status=status.HTTP_200_OK)
        else:
            response_dict["code"] = "403"
            response_dict["message"] = "No access permission"
            return Response(data=response_dict, status=status.HTTP_403_FORBIDDEN)

    @action(
        methods=["post"],
        detail=True,
        url_path="review",
        permission_classes=[IsAdminUser],
    )
    def review(self, request, version, pk, format=None):
        """
        审核实验，需要管理员权限。

        Example:
            POST 127.0.0.1:8000/api/1.0/experiment/2/review/
            {
                "is_passed": true,
                "reply": "ok"
            }

        Return:
            审核信息。
        """

        response_dict = {"code": 200, "message": "ok", "data": []}
        experiment = self.get_object()

        # 先删除已有的审核表。
        try:
            experiment.review.delete()
        except:
            pass

        serializer = ReviewSerializer(
            data={**request.data, "user": request.user.id, "experiment": experiment.id}
        )

        if serializer.is_valid():
            # Successfully created
            serializer.save()
            response_dict["code"] = 200
            response_dict["message"] = "Success"
            response_dict["data"] = serializer.data
            return Response(response_dict, status=status.HTTP_200_OK)

        response_dict["code"] = 422
        response_dict["message"] = serializer.errors
        return Response(data=response_dict, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    @action(
        methods=["post"],
        detail=True,
        url_path="cmd",
        permission_classes=[IsAuthenticated],
    )
    def public_cmd(self, request, version, pk, format=None):
        """
        批量发送指令给设备。

        Example:
            POST 127.0.0.1:8000/api/1.0/experiment/4/cmd/
            {
                equipments: [1, 2]    //要发送指令的设备。
                cmd: reset
                heater: on
            }

        Return:
            成功与否。
        """

        response_dict = {"code": 200, "message": "ok", "data": []}
        experiment = self.get_object()
        equipments = []
        data = request.data.copy()

        # 判断设备是否都合理
        try:
            equipment_id = data.pop("equipment")
            for i in equipment_id:
                equipments.append(Equipment.objects.get(id=i))
        except:
            response_dict["code"] = 400
            response_dict["message"] = "Error equipment"
            return Response(data=response_dict, status=status.HTTP_400_BAD_REQUEST)

        # 判断实验是否正在进行
        if experiment.status != 1:
            response_dict["code"] = 403
            response_dict["message"] = (
                "Access prohibited due to status of this experiment"
            )
            return Response(data=response_dict, status=status.HTTP_403_FORBIDDEN)

        # 判断用户是否有权限
        if (
            request.user in experiment.user.all()
            or request.user == experiment.owner
            or request.user.is_superuser
            or request.user.is_staff
        ):
            if experiment.status == 1:
                if experiment.end_time < datetime.datetime.now():
                    experiment.status = 2

            for equipment in equipments:
                if equipment not in experiment.equipment.all():
                    response_dict["code"] = 403
                    response_dict["message"] = (
                        "Access prohibited because the exquipment is not in this experiment"
                    )
                    return Response(
                        data=response_dict, status=status.HTTP_403_FORBIDDEN
                    )
                equipmentKey = equipment.key
                mqtt = Mqtt()
                mqtt.public_message(equipmentKey, json.dumps(data))

            response_dict["message"] = "Success"
            return Response(data=response_dict, status=status.HTTP_200_OK)

        response_dict["code"] = 403
        response_dict["message"] = "Access prohibited for this user"
        return Response(data=response_dict, status=status.HTTP_403_FORBIDDEN)
