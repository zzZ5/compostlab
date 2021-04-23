from django.contrib import admin
from equipment.models import Equipment, EquipmentRecordModify


class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_brief', 'pk', 'key',
                    'type', 'descript', 'begin_time',
                    'end_time', 'created_time', 'owner', 'users_display', 'is_inuse')
    list_filter = ['owner', 'created_time']
    fieldsets = [
        ('equipment name', {'fields': ['name', 'name_brief']}),
        ('equipment information', {'fields': ['type', 'descript', 'key']}),
        ('usage information', {'fields': ['begin_time', 'end_time', 'users']}),
        ('owner', {'fields': ['owner']}),
        ('created_time', {'fields': ['created_time']}),
    ]
    readonly_fields = ['created_time', 'key']


class EquipmentModifyRecordAdmin(admin.ModelAdmin):
    list_display = ('equipment',  'record', 'modifier', 'created_time')
    list_filter = ['equipment', 'modifier', 'created_time']
    fieldsets = [
        ('modify information', {'fields': ['equipment', 'record']}),
        ('modifier', {'fields': ['modifier']}),
        ('created_time', {'fields': ['created_time']}),
    ]
    readonly_fields = ['created_time']


admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(EquipmentRecordModify, EquipmentModifyRecordAdmin)
