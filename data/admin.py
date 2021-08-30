from django.contrib import admin
from data.models import Data


class DataAdmin(admin.ModelAdmin):
    '''
    django自带的管理员界面设置, 数据表。
    '''
    list_display = ('value', 'measured_time', 'created_time')
    list_filter = ['sensor', 'measured_time', 'created_time']
    fieldsets = [
        ('sensor', {'fields': ['sensor']}),
        ('value', {'fields': ['value']}),
        ('time', {'fields': ['measured_time', 'created_time']}),
    ]
    readonly_fields = ['created_time']
    date_hierarchy = 'measured_time'


# 将数据表注册到管理员界面。
admin.site.register(Data, DataAdmin)
