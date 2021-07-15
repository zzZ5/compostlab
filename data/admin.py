from django.contrib import admin
from data.models import Data


class DataAdmin(admin.ModelAdmin):
    list_display = ('value', 'measured_time', 'created_time')
    list_filter = ['sensor', 'measured_time', 'created_time']
    fieldsets = [
        ('sensor', {'fields': ['sensor']}),
        ('value', {'fields': ['value']}),
        ('time', {'fields': ['measured_time', 'created_time']}),
    ]
    readonly_fields = ['measured_time', 'created_time']
    date_hierarchy = 'measured_time'


admin.site.register(Data, DataAdmin)
