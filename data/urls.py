from data.views import DataViewSet, SensorViewSet
from rest_framework.routers import SimpleRouter

urlpatterns = [
]

router = SimpleRouter()
router.register(prefix='data', viewset=DataViewSet)
router.register(prefix='sensor', viewset=SensorViewSet)
urlpatterns += router.urls
