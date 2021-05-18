from django.contrib import admin

from project.models import Project


class ProjectAdmin(admin.ModelAdmin):
    fields = ['name']
    list_max_show_all = 30
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ['id', 'name']


admin.site.register(Project, ProjectAdmin)
