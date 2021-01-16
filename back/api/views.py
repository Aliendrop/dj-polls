from rest_framework import viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from django.http import Http404

from polls.models import Answer, Poll, Question
from polls.models import Response as Responce_
from .serializers import AnswerSerializer, PollSerializer, QuestionForPollSerializer, ResponseSerializer
from .serializers import ResponseForUserSerializer, ResponseDetailForUserSerializer
from .permissions import IsStaffUserOrReadOnly


class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all().order_by('-start_at', '-end_at')
    serializer_class = PollSerializer
    permission_classes = [IsStaffUserOrReadOnly]

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
        if request.method == 'PUT' or request.method == 'PATCH':
            serializer = QuestionForPollSerializer(
                question, data=request.data, context={'request': request}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((permissions.AllowAny, ))
def register_response(request, pk):
    if request.method == 'POST':
        serializer = ResponseSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            if request.user and not request.user.is_anonymous:
                serializer.save(poll_id=pk, user=request.user)
            else:
                serializer.save(poll_id=pk)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((permissions.AllowAny, ))
def question_answer(request, question_pk, pk):
    if request.method == 'POST':
        response = generics.get_object_or_404(Responce_, pk=pk)
        question = generics.get_object_or_404(Question, pk=question_pk)
        if question.poll.id != response.poll.id:
            raise Http404

        serializer = AnswerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(question_id=question_pk, response_id=pk)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserResponseList(generics.ListAPIView):
    queryset = Responce_.objects.all().select_related('poll', 'user')
    serializer_class = ResponseForUserSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        user_id = self.kwargs['user_id']   # TODO:
        return Responce_.objects.filter(user=user_id)


class UserResponseDetail(generics.ListAPIView):
    queryset = Answer.objects.all().select_related('responce', 'question')
    serializer_class = ResponseDetailForUserSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        response_id = self.kwargs['response_id']   # TODO:
        return Answer.objects.filter(response=response_id)
