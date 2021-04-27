from django.contrib.auth.models import User
from django.db import models


class UserRecord(models.Model):

    record = models.CharField(max_length=256, blank=True)
    user = models.ForeignKey(
        User, null=True, on_delete=models.CASCADE, related_name='%(class)s')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.record

    class Meta:
        db_table = "user_record"
        ordering = ["-created_time"]
        verbose_name = "UserRecord"
        verbose_name_plural = "UserRecords"
