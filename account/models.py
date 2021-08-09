from django.contrib.auth.models import User
from django.db import models


'''
由于采用了Django框架自带的用户表， 所以并没有再新建一个用户表。
'''


class UserRecord(models.Model):
    '''
    用户修改记录表。
    Attributes：
        user: 修改人。
        record: 具体的修改内容。
        created_time: 修改时间。
    '''

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
