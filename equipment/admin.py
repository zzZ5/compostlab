from django.contrib import admin
from equipment.models import Equipment


class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'name_brief', 'key',
                    'type', 'descript', 'begin_time',
                    'end_time', 'created_time', 'owner', 'users_display', 'is_inuse')
    list_filter = ['created_time']
    fieldsets = [
        ('equipment_name', {'fields': ['name']}),
        ('equipment_name_brief', {'fields': ['name_brief']}),
        ('type', {'fields': ['type']}),
        ('descript', {'fields': ['descript']}),
        ('key', {'fields': ['key']}),
        ('begin_time', {'fields': ['begin_time']}),
        ('end_time', {'fields': ['end_time']}),
        ('users', {'fields': ['users']}),
        ('owner', {'fields': ['owner']}),
        ('created_time', {'fields': ['created_time']}),
    ]
    readonly_fields = ['created_time']


admin.site.register(Equipment, EquipmentAdmin)
