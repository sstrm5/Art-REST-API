from django.contrib import admin

from .models.questions import Test, Question, Answer
from .models.subjects import Subject

# Register your models here.
@admin.register(Test)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'subject', 'created_at', 'question_count', 'description', 'is_visible')

@admin.register(Question)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'test', 'test_id', 'created_at', 'updated_at', 'description', 'subject', 'is_visible')

@admin.register(Answer)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'text', 'created_at', 'updated_at', 'is_correct')

@admin.register(Subject)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'is_visible')
