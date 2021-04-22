from django.contrib.auth.models import User
from django.db import models


class UserRecord(models.Model):

    record = models.CharField(max_length=256, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.record

    class Meta:
        ordering = ["-created_time"]
        verbose_name = "UserRecord"
        verbose_name_plural = "UserRecords"
