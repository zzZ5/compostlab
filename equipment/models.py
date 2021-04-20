from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Equipment(models.Model):

    name = models.CharField(max_length=128, unique=True)
    name_brief = models.CharField(max_length=64, unique=True, null=True)
    key = models.CharField(max_length=16, unique=True, null=True)

    REACTOR = 'RE'
    TYPE_CHOICE = (
        (REACTOR, "Reactor"),
    )
    type = models.CharField(
        max_length=32, choices=TYPE_CHOICE, default=REACTOR)
    descript = models.CharField(max_length=256, null=True)
    created_time = models.DateTimeField(auto_now_add=True)
    begin_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    owner = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.DO_NOTHING, related_name='%(class)s_created')
    users = models.ManyToManyField(
        User, null=True, blank=True,  related_name='%(class)s_inuse')

    def users_display(self):
        return str(self.users)

    def is_inuse(self):
        if self.end_time:
            return self.end_time >= timezone.now()
        return False

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-created_time"]
        verbose_name = "Equipment"
        verbose_name_plural = "Equipments"


class EquipmentUsageRecord():

    users = models.ManyToManyField(
        User, null=True, related_name='%(class)s_used')
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    begin_time = models.DateTimeField(null=False)
    end_time = models.DateTimeField(null=False)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-created_time"]
        verbose_name = "EquipmentUsageRecord"
        verbose_name_plural = "EquipmentUsageRecords"


class EquipmentHistoricalRecord():

    modifier = models.ForeignKey(
        User, null=True, on_delete=models.DO_NOTHING, related_name='%(class)s_modified')
    name = models.CharField(max_length=128, unique=True)
    name_brief = models.CharField(max_length=64, unique=True, null=True)
    key = models.CharField(max_length=16, unique=True, null=True)
    descript = models.CharField(max_length=256, null=True)
    created_time = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, null=True)
    equipment = models.ForeignKey(
        Equipment, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-created_time"]
        verbose_name = "EquipmentHistoricalRecord"
        verbose_name_plural = "EquipmentHistoricalRecords"


class Sensor(models.Model):
    name = models.CharField(max_length=128, unique=True)
    name_brief = models.CharField(max_length=64, unique=True, null=True)
    key = models.CharField(max_length=16, unique=True, null=True)
    descript = models.CharField(max_length=256, null=True)
    equipment = models.ForeignKey(
        Equipment, null=True, on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-created_time"]
        verbose_name = "Sensor"
        verbose_name_plural = "Sensors"


class SensorHistoricalRecord(models.Model):

    modifier = models.ForeignKey(
        User, null=True, on_delete=models.DO_NOTHING, related_name='%(class)s_modified')
    name = models.CharField(max_length=128, unique=True)
    key = models.CharField(max_length=16, unique=True, null=True)
    descript = models.CharField(max_length=256, null=True)
    equipment = models.ForeignKey(
        Equipment, null=True, on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True)
    sensor = models.ForeignKey(Sensor, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-created_time"]
        verbose_name = "SensorHistoricalRecord"
        verbose_name_plural = "SensorHistoricalRecords"
