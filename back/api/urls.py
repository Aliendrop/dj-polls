from rest_framework import routers
from django.urls import path

from .views import PollViewSet, register_response, question_answer


router = routers.DefaultRouter()
router.register(r'polls', PollViewSet, basename='polls')


urlpatterns = router.urls

urlpatterns += [
    path('response/<int:pk>/', register_response, name='response'),
    path('response/<int:pk>/question/<int:question_pk>', question_answer, name='question'),
]
