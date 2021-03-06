from django.contrib import admin
from sensor.models import Sensor, SensorRecord


class SensorAdmin(admin.ModelAdmin):
    '''
    django自带的管理员界面设置, 传感器表。
    '''

    list_display = ('name', 'abbreviation', 'pk', 'key',
                    'type', 'unit', 'descript', 'equipment', 'created_time')
    list_filter = ['equipment', 'created_time']
    fieldsets = [
        ('sensor name', {'fields': ['name', 'abbreviation']}),
        ('sensor information', {'fields': [
         'type', 'unit', 'descript', 'key', 'equipment']}),
        ('created_time', {'fields': ['created_time']}),
    ]
    readonly_fields = ['created_time']


class SensorRecordAdmin(admin.ModelAdmin):
    '''
    django自带的管理员界面设置, 传感器修改记录表。
    '''

    list_display = ('sensor',  'record', 'modifier', 'created_time')
    list_filter = ['sensor', 'modifier', 'created_time']
    fieldsets = [
        ('modify information', {'fields': ['sensor', 'record']}),
        ('modifier', {'fields': ['modifier']}),
        ('created_time', {'fields': ['created_time']}),
    ]
    readonly_fields = ['created_time']


admin.site.register(Sensor, SensorAdmin)
admin.site.register(SensorRecord, SensorRecordAdmin)
