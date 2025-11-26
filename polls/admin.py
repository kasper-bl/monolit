from django.contrib import admin
from .models import Question, Choice, MyUser



@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'pub_date', 'expires_at', 'is_expired']
    list_filter = ['pub_date', 'expires_at']
    search_fields = ['question_text']

admin.site.register(Choice)

class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 3

admin.site.register(MyUser)