from django.contrib import admin
from account.models import UserRecord


class UserRecordAdmin(admin.ModelAdmin):
    list_display = ('user',  'record', 'created_time')
    list_filter = ['user', 'created_time']
    fieldsets = [
        ('modify information', {'fields': ['user', 'record']}),
        ('created_time', {'fields': ['created_time']}),
    ]
    readonly_fields = ['created_time']


admin.site.register(UserRecord, UserRecordAdmin)
