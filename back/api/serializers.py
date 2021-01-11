from rest_framework import serializers
from django.urls import reverse

from polls.models import Poll, Question, Response, Answer


class QuestionForPollSerializer(serializers.HyperlinkedModelSerializer):
    url_question_actions = serializers.SerializerMethodField()

    def get_url_question_actions(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri('{}{}/'.format(reverse('polls-question', args=[obj.poll.id]), str(obj.id)))

    class Meta:
        model = Question
        fields = ['id', 'text', 'question_type', 'url_question_actions']


class PollSerializer(serializers.ModelSerializer):
    questions = QuestionForPollSerializer(many=True, required=False)
    url_poll_detail = serializers.HyperlinkedIdentityField(view_name='polls-detail')
    url_add_question = serializers.HyperlinkedIdentityField(view_name='polls-question')
    url_register_response = serializers.HyperlinkedIdentityField(view_name='response')

    def create(self, validated_data):
        try:
            questions_data = validated_data.pop('questions')
        except KeyError as err:
            questions_data = {}

        poll = Poll.objects.create(**validated_data)
        for question_data in questions_data:
            Question.objects.create(poll=poll, **question_data)
        return poll

    def update(self, instance, validated_data):
        if 'start_at' in validated_data:
            raise serializers.ValidationError({
                'start_at': 'You must not change this field.',
            })
        return super().update(instance, validated_data)

    class Meta:
        model = Poll
        fields = '__all__'
        extra_field = ['url_detail', 'url_question', ]


class ResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Response
        fields = ['id', 'user', 'identifier', 'created_at', ]


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['text', ]


class ResponseForUserSerializer(serializers.ModelSerializer):
    poll = PollSerializer()
    url_detail = serializers.HyperlinkedIdentityField(view_name='user-detail', lookup_field="id", lookup_url_kwarg="response_id")

    class Meta:
        model = Response
        fields = ['id', 'user', 'identifier', 'created_at', 'poll', 'url_detail', ]


class ResponseDetailForUserSerializer(serializers.ModelSerializer):
    question = QuestionForPollSerializer()

    class Meta:
        model = Answer
        fields = '__all__'
