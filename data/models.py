import django.utils.timezone as timezone

from sensor.models import Sensor

from django.db import models


class Data(models.Model):
    """
    数据表。

    Attributes：
        sensor: 数据所属的传感器。
        value(float): 数据值。
        measured_time： 数据测量时间。
        created_time: 创建时间。
    """

    sensor = models.ForeignKey(
        Sensor, null=True, on_delete=models.CASCADE, related_name="%(class)s"
    )
    value = models.FloatField()
    measured_time = models.DateTimeField(default=timezone.now)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(round(self.value, 2))

    class Meta:
        db_table = "data"
        ordering = ["-measured_time"]
        verbose_name = "Data"
        verbose_name_plural = "Data"
        get_latest_by = "measured_time"
        unique_together = ["sensor", "measured_time"]  # 组合唯一索引
        indexes = [
            models.Index(fields=["sensor"]),
            models.Index(fields=["measured_time"]),
            models.Index(fields=["created_time"]),
        ]
