from rest_framework import routers

from .views import PollViewSet


router = routers.DefaultRouter()
router.register(r'polls', PollViewSet, basename='polls')


urlpatterns = router.urls
