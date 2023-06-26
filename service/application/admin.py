from application.v1.models import Task
from django.contrib.admin import ModelAdmin, register
from django.urls import reverse
from django.utils.html import format_html


@register(Task)
class TaskAdmin(ModelAdmin):
    date_hierarchy = 'start_date'
    list_display = (
        'id',
        'link_to_author',
        'description',
        'start_date',
        'finish_date'
    )
    list_display_links = ('id',)
    list_filter = ('author',)
    search_fields = ('description', 'start_date', 'finish_date')

    def link_to_author(self, obj):
        link = reverse("admin:users_user_change", args=[obj.author.id])
        return format_html('<a href="{}">{}</a>', link, obj.author.username)

    link_to_author.short_description = Task._meta.get_field(
        'author'
    ).verbose_name
