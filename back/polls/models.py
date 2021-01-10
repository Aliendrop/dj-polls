from django.db import models
from django.conf import settings


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
