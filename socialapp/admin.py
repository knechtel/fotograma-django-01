from django.contrib import admin
from .models import Comment, Like, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('author__username', 'caption')


admin.site.register((Comment, Like))
