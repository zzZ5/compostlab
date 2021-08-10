from equipment.models import Equipment

from django.contrib.auth.models import User
from django.db import models


class Sensor(models.Model):
    '''
    传感器表。

    Attributes：
        name: 传感器名。
        abbreviation: 传感器名缩写。
        key: 传感器key(传感器标识)。
        unit： 传感器单位。
        type： 传感器类型。
        descript： 传感器描述。
        created_time: 创建时间。
    '''

    name = models.CharField(max_length=128, unique=True)
    abbreviation = models.CharField(max_length=64, null=True)
    key = models.CharField(max_length=16, unique=True, null=True)

    TEMPERQTURE = 'T'
    HUMIDITY = 'H'
    TYPE_CHOICE = (
        (TEMPERQTURE, "Temperature Sensor"),
        (HUMIDITY, "Humidity Sensor")
    )

    CELSIUS = '℃'
    PERCENT = '%'

    UNIT_CHOICE = (
        (CELSIUS, "Celsius"),
        (PERCENT, "Percent")
    )

    unit = models.CharField(
        max_length=32, choices=UNIT_CHOICE, default=CELSIUS)
    type = models.CharField(
        max_length=32, choices=TYPE_CHOICE, default=TEMPERQTURE)

    descript = models.CharField(max_length=256, null=True)

    equipment = models.ForeignKey(
        Equipment, null=True, on_delete=models.SET_NULL, related_name='%(class)s')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "sensor"
        ordering = ["-created_time"]
        verbose_name = "Sensor"
        verbose_name_plural = "Sensors"


class SensorRecord(models.Model):
    '''
    传感器修改记录表。

    Attributes：
        record: 具体的修改内容。
        sensor: 修改的传感器。
        modifier: 修改人。
        created_time: 修改时间。
    '''

    record = models.CharField(max_length=256, blank=True)
    sensor = models.ForeignKey(
        Sensor, null=True, on_delete=models.CASCADE, related_name='%(class)s')
    modifier = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.record

    class Meta:
        db_table = "sensor_record"
        ordering = ["-created_time"]
        verbose_name = "SensorRecord"
        verbose_name_plural = "SensorRecords"
