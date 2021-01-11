from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import generics, status
from django.http import Http404

from polls.models import Poll, Question
from .serializers import PollSerializer, QuestionForPollSerializer
from .permissions import IsAdminUserOrReadOnly


class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all().order_by('-start_at', '-end_at')
    serializer_class = PollSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    @action(detail=True, methods=["post"])
    def question(self, request, pk=None):
        serializer = QuestionForPollSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(poll_id=pk)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["put", "patch", "delete"], url_path='question/(?P<question_pk>[^/.]+)')
    def question_actions(self, request, question_pk, pk):
        question = generics.get_object_or_404(Question, pk=question_pk)
        if question.poll.id != int(pk):
            raise Http404
        if request.method == 'DELETE':
            question.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            serializer = QuestionForPollSerializer(question, data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
