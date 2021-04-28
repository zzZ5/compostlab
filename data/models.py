from sensor.models import Sensor

from django.db import models


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
