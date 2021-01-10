from django.db import models
from django.db.models import fields
from rest_framework import serializers

from polls.models import Poll


class PollSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        if 'start_at' in validated_data:
            raise serializers.ValidationError({
                'start_at': 'You must not change this field.',
            })

        return super().update(instance, validated_data)

    class Meta:
        model = Poll
        fields = '__all__'
