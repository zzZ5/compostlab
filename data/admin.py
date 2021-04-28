from django.contrib import admin
from data.models import Data, Sensor, SensorRecord


class SensorAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_brief', 'pk', 'key',
                    'type', 'descript', 'equipment', 'created_time')
    list_filter = ['equipment', 'created_time']
    fieldsets = [
        ('sensor name', {'fields': ['name', 'name_brief']}),
        ('sensor information', {'fields': [
         'type', 'descript', 'key', 'equipment']}),
        ('created_time', {'fields': ['created_time']}),
    ]
    readonly_fields = ['created_time']


class SensorRecordAdmin(admin.ModelAdmin):
    list_display = ('sensor',  'record', 'modifier', 'created_time')
    list_filter = ['sensor', 'modifier', 'created_time']
    fieldsets = [
        ('modify information', {'fields': ['sensor', 'record']}),
        ('modifier', {'fields': ['modifier']}),
        ('created_time', {'fields': ['created_time']}),
    ]
    readonly_fields = ['created_time']


class DataAdmin(admin.ModelAdmin):
    list_display = ('sensor', 'value', 'unit', 'measured_time', 'created_time')
    list_filter = ['sensor', 'measured_time', 'created_time']
    fieldsets = [
        ('sensor', {'fields': ['sensor']}),
        ('value', {'fields': ['value', 'unit']}),
        ('time', {'fields': ['measured_time', 'created_time']}),
    ]
    readonly_fields = ['measured_time', 'created_time']


admin.site.register(Data, DataAdmin)
admin.site.register(Sensor, SensorAdmin)
admin.site.register(SensorRecord, SensorRecordAdmin)
