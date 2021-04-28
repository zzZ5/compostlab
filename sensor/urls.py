from sensor.views import SensorViewSet
from rest_framework.routers import SimpleRouter

urlpatterns = [
]

router = SimpleRouter()
router.register(prefix='', viewset=SensorViewSet)
urlpatterns += router.urls
