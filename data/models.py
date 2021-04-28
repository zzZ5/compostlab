from equipment.models import Equipment

from django.contrib.auth.models import User
from django.db import models


class Sensor(models.Model):
    name = models.CharField(max_length=128, unique=True)
    name_brief = models.CharField(max_length=64, null=True)
    key = models.CharField(max_length=16, unique=True, null=True)

    TEMPERQTURE = 'T'
    HUMIDITY = 'H'
    TYPE_CHOICE = (
        (TEMPERQTURE, "Temperature sensor"),
        (HUMIDITY, "Humidity sensor")
    )

    type = models.CharField(
        max_length=32, choices=TYPE_CHOICE, default=TEMPERQTURE)

    descript = models.CharField(max_length=256, null=True)

    equipment = models.ForeignKey(
        Equipment, null=True, on_delete=models.SET_NULL, related_name='%(class)ss')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "sensor"
        ordering = ["-created_time"]
        verbose_name = "Sensor"
        verbose_name_plural = "Sensors"


class SensorRecord(models.Model):

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


class Data(models.Model):
    sensor = models.ForeignKey(
        Sensor, null=True, on_delete=models.CASCADE)
    value = models.FloatField()
    unit = models.CharField(max_length=32, null=True, blank=True)
    measured_time = models.DateTimeField(null=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(round(self.value, 2))

    class Meta:
        db_table = "data"
        ordering = ["-measured_time"]
        verbose_name = "Data"
        verbose_name_plural = "Data"
