from django.db import models


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

    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    text = models.TextField()
    question_type = models.CharField(max_length=64, choices=QUESTION_TYPES, default=AS_TEXT)

    def __str__(self):
        return self.get_question_type_display()
