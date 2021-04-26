from django.contrib import admin
from data.models import Sensor


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
    readonly_fields = ['created_time', 'key']


admin.site.register(Sensor, SensorAdmin)
