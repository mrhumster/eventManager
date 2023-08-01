from django.contrib import admin

# Register your models here.
from accounts.models import Token, Settings


@admin.register(Token)
class CommentAdmin(admin.ModelAdmin):
    model = Token


@admin.register(Settings)
class CommentAdmin(admin.ModelAdmin):
    model = Settings
