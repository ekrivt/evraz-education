from django.contrib import admin

from .models import Task, Description


class DescriptionInline(admin.TabularInline):
    model = Description


class TaskAdmin(admin.ModelAdmin):
    fields = ['name', 'project', 'status', 'author']
    list_max_show_all = 30
    list_display = ('id', 'name', 'project', 'status','author')
    list_display_links = ('id', 'name')
    list_filter = ('project__name',
                   'performer',
                   'author',
                   'status')
    search_fields = ['id',
                     'name',
                     'project__id',
                     'project__name',
                     'status',
                     'performer',
                     'author']
    inlines = [
        DescriptionInline,
    ]


admin.site.register(Task, TaskAdmin)
