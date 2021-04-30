from experiment.views import ExperimentViewSet

from rest_framework.routers import SimpleRouter

urlpatterns = [
]

router = SimpleRouter()
router.register(prefix='', viewset=ExperimentViewSet)
urlpatterns += router.urls
