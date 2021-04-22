from django.urls import path
from equipment import views
from rest_framework.routers import SimpleRouter

urlpatterns = [
    path('historicalRecord/<pk>/', views.EquipmentHistoricalRecordView.as_view()),
]

router = SimpleRouter()
router.register(prefix='', viewset=views.EquipmentViewSet)
urlpatterns += router.urls
