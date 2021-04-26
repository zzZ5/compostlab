from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms import ModelMultipleChoiceField, ModelForm
from equipment.models import Equipment, EquipmentRecordModify
from data.models import Sensor


class SensorAdminForm(ModelForm):
    sensors = ModelMultipleChoiceField(
        queryset=Sensor.objects.all(),
        widget=FilteredSelectMultiple(verbose_name='sensors', is_stacked=False))

    class Meta:
        model = Sensor
        fields = ['name', 'name_brief', 'type']

    def __init__(self, *args, **kwargs):
        super(SensorAdminForm, self).__init__(*args, **kwargs)
        if self.instance:
            # fill initial related values
            self.fields['sensors'].initial = self.instance.sensors.all()


class EquipmentAdmin(admin.ModelAdmin):
    form = SensorAdminForm
    list_display = ('name', 'name_brief', 'pk', 'key',
                    'type', 'descript', 'sensors_display', 'begin_time',
                    'end_time', 'created_time', 'owner', 'users_display', 'is_inuse')
    list_filter = ['owner', 'created_time']
    fieldsets = [
        ('equipment name', {'fields': ['name', 'name_brief']}),
        ('equipment information', {'fields': [
         'type', 'descript', 'key', 'sensors']}),
        ('usage information', {'fields': ['begin_time', 'end_time', 'users']}),
        ('owner', {'fields': ['owner']}),
        ('created_time', {'fields': ['created_time']}),
    ]
    filter_horizontal = ('users',)

    def save_model(self, request, obj, form, change):
        original_sensors = obj.sensors.all()
        new_sensors = form.cleaned_data['sensors']
        remove_qs = original_sensors.exclude(id__in=new_sensors.values('id'))
        add_qs = new_sensors.exclude(id__in=original_sensors.values('id'))
        for item in remove_qs:
            obj.sensors.remove(item)
        for item in add_qs:
            obj.sensors.add(item)
        obj.save()

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
