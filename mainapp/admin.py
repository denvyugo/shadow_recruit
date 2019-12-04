from django.contrib import admin
from .models import Answers, Planet, Question, Sith

# Register your models here.
admin.site.register(Planet)
admin.site.register(Sith)


class AnswerInline(admin.TabularInline):
    model = Answers
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fields = ['question']
    inlines = [AnswerInline]

admin.site.register(Question, QuestionAdmin)

