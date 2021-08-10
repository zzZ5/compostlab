from data.views import DataViewSet
from rest_framework.routers import SimpleRouter

urlpatterns = [
]

# 使用rest_framework的SimpleRouter将路由和views.py中的方法绑定。
router = SimpleRouter()
router.register(prefix='', viewset=DataViewSet)
urlpatterns += router.urls
