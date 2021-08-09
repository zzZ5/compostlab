from django.contrib import admin
from account.models import UserRecord


class UserRecordAdmin(admin.ModelAdmin):
    '''
    django自带的管理员界面设置, 这个是账号表。
    '''

    list_display = ('user',  'record', 'created_time')
    list_filter = ['user', 'created_time']
    fieldsets = [
        ('modify information', {'fields': ['user', 'record']}),
        ('created_time', {'fields': ['created_time']}),
    ]
    readonly_fields = ['created_time']


# 将账号表注册到管理员界面。
admin.site.register(UserRecord, UserRecordAdmin)
