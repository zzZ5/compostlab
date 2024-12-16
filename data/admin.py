from django.contrib import admin
from data.models import Data
from compostlab.utils.LargeTablePaginator import LargeTablePaginator


class DataAdmin(admin.ModelAdmin):
    """
    django自带的管理员界面设置, 数据表。
    """

    show_full_result_count = False
    list_per_page = 50

    list_display = ("value", "measured_time")
    list_filter = ["sensor", "measured_time"]
    fieldsets = [
        ("sensor", {"fields": ["sensor"]}),
        ("value", {"fields": ["value"]}),
        ("time", {"fields": ["measured_time"]}),
    ]


# 将数据表注册到管理员界面。
admin.site.register(Data, DataAdmin)
