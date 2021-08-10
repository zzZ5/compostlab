from experiment.views import ExperimentViewSet

from rest_framework.routers import SimpleRouter

urlpatterns = [
]

# 使用rest_framework的SimpleRouter将路由和views.py中的方法绑定。
router = SimpleRouter()
router.register(prefix='', viewset=ExperimentViewSet)
urlpatterns += router.urls
