from django.db import models
from django.conf import settings
import uuid

class CommonModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True


class Poll(CommonModel):
    title = models.CharField(max_length=64)
    description = models.TextField()
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()

    def __str__(self):
        return self.title


class Question(models.Model):
    AS_TEXT = 'text'
    SELECT = 'select-one'
    SELECT_MULTIPLE = 'select-multiple'

    QUESTION_TYPES = (
        (AS_TEXT, 'Answer as text'),
        (SELECT, 'Answer as select one'),
        (SELECT_MULTIPLE, 'Answer as select multiple'),
    )

    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    question_type = models.CharField(max_length=64, choices=QUESTION_TYPES, default=AS_TEXT)

    def __str__(self):
        return f'{self.poll} - {self.get_question_type_display()}'


class Response(CommonModel):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='responses')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    identifier = models.UUIDField(default=uuid.uuid4, editable=False)
    confirm = models.BooleanField(default=False)

    def __str__(self):
        return str(self.identifier)


class Answer(CommonModel):
    response = models.ForeignKey(Response, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.TextField()

    def __str__(self):
        return repr(self.question)
