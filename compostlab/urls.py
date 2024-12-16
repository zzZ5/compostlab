"""compostlab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from compostlab.utils.jwt import obtain_jwt_token

# 分配路由
urlpatterns = [
    path("admin/", admin.site.urls),
    # 首页直接使用vue.js生成的index.html文件
    path("", TemplateView.as_view(template_name="index.html")),
    # 登陆并获取token使用jwt自带的方法
    path("api/<version>/login/", obtain_jwt_token),
    path("api/<version>/account/", include("account.urls")),
    path("api/<version>/data/", include("data.urls")),
    path("api/<version>/equipment/", include("equipment.urls")),
    path("api/<version>/experiment/", include("experiment.urls")),
    path("api/<version>/sensor/", include("sensor.urls")),
]
