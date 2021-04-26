from django.urls import path
from equipment.views import EquipmentViewSet
from rest_framework.routers import SimpleRouter

urlpatterns = [
]

router = SimpleRouter()
router.register(prefix='', viewset=EquipmentViewSet)
urlpatterns += router.urls
