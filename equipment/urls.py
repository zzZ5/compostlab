from django.urls import path

from equipment import views

urlpatterns = [
    path('list/', views.EquipmentList.as_view()),
    path('create/', views.EquipmentCreate.as_view()),
    path('historicalRecord/<pk>/', views.EquipmentHistoricalRecordView.as_view()),
    path('<pk>/', views.EquipmentDetail.as_view()),
]
