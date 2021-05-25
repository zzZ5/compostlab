from django.contrib.auth.models import User
from django.db import models


class Equipment(models.Model):

    name = models.CharField(max_length=128, unique=True)
    abbreviation = models.CharField(max_length=64, null=True)

    REACTOR = 'RE'
    TYPE_CHOICE = (
        (REACTOR, "Reactor"),
    )
    type = models.CharField(
        max_length=32, choices=TYPE_CHOICE, default=REACTOR)

    descript = models.CharField(max_length=256, null=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def sensor_display(self):
        return "\n".join([sensor.name for sensor in self.sensor.all()])

    def __str__(self):
        return self.name

    class Meta:
        db_table = "equipment"
        ordering = ["-created_time"]
        verbose_name = "Equipment"
        verbose_name_plural = "Equipments"


class EquipmentRecord(models.Model):

    record = models.CharField(max_length=256, blank=True)
    equipment = models.ForeignKey(
        Equipment, null=True, on_delete=models.CASCADE, related_name='%(class)s')
    modifier = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.record

    class Meta:
        db_table = "equipment_record"
        ordering = ["-created_time"]
        verbose_name = "EquipmentRecord"
        verbose_name_plural = "EquipmentRecords"
