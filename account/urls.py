from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from account import views

urlpatterns = [
    path('login/', obtain_jwt_token),
    path('logout/', views.log_out),
    path('register/', views.CreateUser.as_view()),
    path('changepassword/', views.change_password),
    path('<pk>/', views.UserView.as_view()),
]
