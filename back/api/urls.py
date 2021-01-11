from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path, re_path

from .views import PollViewSet, register_response, question_answer, UserResponseList, UserResponseDetail


router = routers.DefaultRouter()
router.register(r'polls', PollViewSet, basename='polls')


urlpatterns = router.urls

urlpatterns += [
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    re_path('user-statistics/(?P<user_id>.+)/$', UserResponseList.as_view()),
    re_path('user-detail/(?P<response_id>.+)/$', UserResponseDetail.as_view(), name='user-detail'),
    path('user-response/<int:pk>/', register_response, name='response'),
    path('user-response/<int:pk>/question/<int:question_pk>', question_answer, name='question'),
]
