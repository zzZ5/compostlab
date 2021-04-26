from account.views import UserViewSet
from rest_framework.routers import SimpleRouter


urlpatterns = [
]

router = SimpleRouter()
router.register(prefix='', viewset=UserViewSet)
urlpatterns += router.urls
