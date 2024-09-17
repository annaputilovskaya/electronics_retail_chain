from rest_framework.routers import DefaultRouter

from suppliers.apps import SuppliersConfig
from suppliers.views import OrganizationViewSet

app_name = SuppliersConfig.name

router = DefaultRouter()
router.register("", OrganizationViewSet, basename="organization")

urlpatterns = []
urlpatterns += router.urls
