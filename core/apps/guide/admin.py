from django.contrib import admin

from core.apps.guide.models import Card

# Register your models here.


@admin.register(Card)
class GuideCardAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'subject', 'created_at', 'updated_at')
