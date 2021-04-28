from django.contrib import admin
from data.models import Data


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
