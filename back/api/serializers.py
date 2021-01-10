from django.db import models
from django.db.models import fields
from rest_framework import serializers

from polls.models import Poll


class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = '__all__'
