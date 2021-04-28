from data.views import DataViewSet
from rest_framework.routers import SimpleRouter

urlpatterns = [
]

router = SimpleRouter()
router.register(prefix='', viewset=DataViewSet)
urlpatterns += router.urls
