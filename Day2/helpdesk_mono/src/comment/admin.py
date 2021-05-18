from django.contrib import admin

from comment.models import Comment


class CommentAdmin(admin.ModelAdmin):
    fields = ['task', 'text', 'author']
    list_max_show_all = 30
    list_display = ('id', 'task', 'text', 'author')
    list_display_links = ('id', 'task', 'text', 'author')
    search_fields = ('id', 'task', 'text', 'author')


admin.site.register(Comment, CommentAdmin)