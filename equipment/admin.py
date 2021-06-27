from data.models import Sensor
from equipment.models import Equipment, EquipmentRecord

from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms import ModelMultipleChoiceField, ModelForm


class SensorAdminForm(ModelForm):
    sensor = ModelMultipleChoiceField(
        queryset=Sensor.objects.all(),
        widget=FilteredSelectMultiple(verbose_name='sensor', is_stacked=False), required=False)

    class Meta:
        model = Sensor
        fields = ['name', 'abbreviation', 'type']

    def __init__(self, *args, **kwargs):
        super(SensorAdminForm, self).__init__(*args, **kwargs)
        if self.instance:
            # fill initial related values
            self.fields['sensor'].initial = self.instance.sensor.all()


class EquipmentAdmin(admin.ModelAdmin):
    form = SensorAdminForm
    list_display = ('name', 'abbreviation', 'pk', 'key', 'type',
                    'descript', 'sensor_display', 'created_time')
    list_filter = ['created_time']
    fieldsets = [
        ('equipment name', {'fields': ['name', 'abbreviation']}),
        ('equipment information', {'fields': [
         'type', 'key', 'descript', 'sensor']}),
        ('created_time', {'fields': ['created_time']}),
    ]

    def save_model(self, request, obj, form, change):
        original_sensors = obj.sensor.all()
        new_sensors = form.cleaned_data['sensor']
        remove_qs = original_sensors.exclude(id__in=new_sensors.values('id'))
        add_qs = new_sensors.exclude(id__in=original_sensors.values('id'))
        for item in remove_qs:
            obj.sensor.remove(item)
        for item in add_qs:
            obj.sensor.add(item)
        obj.save()

    readonly_fields = ['created_time']


class EquipmentRecordAdmin(admin.ModelAdmin):
    list_display = ('equipment',  'record', 'modifier', 'created_time')
    list_filter = ['equipment', 'modifier', 'created_time']
    fieldsets = [
        ('modify information', {'fields': ['equipment', 'record']}),
        ('modifier', {'fields': ['modifier']}),
        ('created_time', {'fields': ['created_time']}),
    ]
    readonly_fields = ['created_time']


admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(EquipmentRecord, EquipmentRecordAdmin)
