from experiment.models import Experiment

from django import forms
from django.contrib import admin


class ExperimentModelForm(forms.ModelForm):
    descript = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Experiment
        fields = ['descript']


class ExperimentAdmin(admin.ModelAdmin):
    form = ExperimentModelForm
    list_display = ('name', 'pk', 'site', 'descript', 'equipment_display', 'begin_time',
                    'end_time', 'owner', 'user_display', 'status', 'review', 'created_time')
    list_filter = ['created_time']
    fieldsets = [
        ('experiment name', {'fields': ['name']}),
        ('experiment information', {'fields': [
         'site', 'descript', 'equipment']}),
        ('experiment time', {'fields': [
         'begin_time', 'end_time']}),
        ('experiment user', {'fields': [
         'owner', 'user']}),
        ('experiment review', {'fields': [
         'status', 'review']}),
        ('created_time', {'fields': ['created_time']}),
    ]

    readonly_fields = ['created_time']


admin.site.register(Experiment, ExperimentAdmin)
