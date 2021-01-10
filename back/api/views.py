from rest_framework import viewsets

from polls.models import Poll
from .serializers import PollSerializer
from .permissions import IsAdminUserOrReadOnly


class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all().order_by('-start_at', '-end_at')
    serializer_class = PollSerializer
    permission_classes = [IsAdminUserOrReadOnly]
