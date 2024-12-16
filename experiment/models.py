from django.db.models.fields.related import OneToOneField
from equipment.models import Equipment

from django.contrib.auth.models import User
from django.db import models


class Experiment(models.Model):
    """
    实验表。

    Attributes：
        name: 实验名。
        site: 试验地点。
        descript： 实验描述。
        equipment: 实验要用到的设备。
        begin_time: 实验开始时间。
        end_time: 实验结束时间。
        user: 实验参与人员。
        owmer: 实验所有者（实验创建人）。
        status： 实验状态。
        created_time: 创建时间。
    """

    name = models.CharField(max_length=128, unique=True)
    site = models.CharField(max_length=128)
    descript = models.CharField(max_length=256, null=True)
    equipment = models.ManyToManyField(Equipment, blank=True, related_name="%(class)s")
    begin_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    user = models.ManyToManyField(User, related_name="%(class)s_use")
    owner = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name="%(class)s_own"
    )

    # 实验状态包括以下四个
    FAILED = -1
    APPLYING = 0
    DOING = 1
    DONE = 2
    STATUS_CHOICE = (
        (FAILED, "Failed"),
        (APPLYING, "Applying"),
        (DOING, "Doing"),
        (DONE, "Done"),
    )
    status = models.IntegerField(choices=STATUS_CHOICE, default=APPLYING)

    created_time = models.DateTimeField(auto_now_add=True)

    def equipment_display(self):
        return "\n".join([equipment.name for equipment in self.equipment.all()])

    def user_display(self):
        return "\n".join([user.username for user in self.user.all()])

    def __str__(self):
        return self.name

    class Meta:
        db_table = "experiment"
        ordering = ["-created_time"]
        verbose_name = "Experiment"
        verbose_name_plural = "Experiments"
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["created_time"]),
        ]


class ExperimentRecord(models.Model):
    """
    实验修改记录表。

    Attributes：
        record: 具体的修改内容。
        experiment: 修改的实验。
        modifier: 修改人。
        created_time: 修改时间。
    """

    record = models.CharField(max_length=256, blank=True)
    experiment = models.ForeignKey(
        Experiment, null=True, on_delete=models.CASCADE, related_name="%(class)s"
    )
    modifier = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.record

    class Meta:
        db_table = "experiment_record"
        ordering = ["-created_time"]
        verbose_name = "ExperimentRecord"
        verbose_name_plural = "ExperimentRecords"


class Review(models.Model):
    """
    实验审核表。

    Attributes：
        experiment: 审核的实验。
        is_passed: 是否通过。
        reply: 回复。
        user: 审核人。
        created_time: 创建时间。
    """

    experiment = OneToOneField(Experiment, null=False, on_delete=models.CASCADE)
    is_passed = models.BooleanField(null=True)
    reply = models.CharField(max_length=128)
    user = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name="%(class)s"
    )
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.experiment.name

    class Meta:
        db_table = "experiment_review"
        ordering = ["-created_time"]
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
