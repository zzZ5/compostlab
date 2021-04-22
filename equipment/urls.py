from django.urls import path
from equipment import views
from rest_framework.routers import SimpleRouter

urlpatterns = [
]

router = SimpleRouter()
router.register(prefix='', viewset=views.EquipmentViewSet)
urlpatterns += router.urls
