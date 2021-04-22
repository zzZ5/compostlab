from account import views
from rest_framework.routers import SimpleRouter


urlpatterns = [
]

router = SimpleRouter()
router.register(prefix='', viewset=views.UserViewSet)
urlpatterns += router.urls
