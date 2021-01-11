from django.contrib import admin

from .models import Poll, Question, Response, Answer


admin.site.register(Poll)
admin.site.register(Question)
admin.site.register(Response)
admin.site.register(Answer)
