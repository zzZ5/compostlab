from django.urls import path
from compostlab.utils.jwt import obtain_jwt_token
from account import views
from rest_framework.routers import SimpleRouter


urlpatterns = [
    path('login/', obtain_jwt_token),
]

router = SimpleRouter()
router.register(prefix='', viewset=views.UserDetail)
urlpatterns += router.urls
