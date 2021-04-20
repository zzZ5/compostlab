from django.urls import path
from equipment import views

urlpatterns = [
    path('create/', views.CreateEquipment.as_view()),
    path('historicalRecord/<pk>/', views.EquipmentHistoricalRecordView.as_view()),
    path('<pk>/', views.EquipmentView.as_view()),
]
