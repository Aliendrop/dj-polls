from rest_framework import routers
from django.urls import path, re_path

from .views import PollViewSet, register_response, question_answer, UserResponseList, UserResponseDetail


router = routers.DefaultRouter()
router.register(r'polls', PollViewSet, basename='polls')


urlpatterns = router.urls

urlpatterns += [
    re_path('user-statistics/(?P<user_id>.+)/$', UserResponseList.as_view()),
    re_path('user-detail/(?P<response_id>.+)/$', UserResponseDetail.as_view(), name='user-detail'),
    path('user-response/<int:pk>/', register_response, name='response'),
    path('user-response/<int:pk>/question/<int:question_pk>', question_answer, name='question'),
]
