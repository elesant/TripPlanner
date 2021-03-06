from django.contrib import admin
from core.models import User, Plan, Collaboration, Event
from django.contrib.sessions.models import Session


class UserAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': ('email', 'facebook_id', 'tz_offset', 'display_name')
        }),
        ('Status', {
            'classes': ('collapse',),
            'fields': ('is_active', 'is_staff', 'is_superuser', 'last_login')
        }),
        ('Groups & Permissions', {
            'classes': ('collapse',),
            'fields': ('groups', 'user_permissions')
        }),
    )
    list_display = ('email', 'is_staff', 'last_login')
    search_fields = ['email']
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'last_login')
    filter_horizontal = ['groups', 'user_permissions']


class CollaborationInline(admin.StackedInline):
    model = Collaboration
    extra = 0


class PlanAdmin(admin.ModelAdmin):

    inlines = [CollaborationInline]
    list_display = ('title', 'time_created', 'time_modified')
    search_fields = ['title']


class EventAdmin(admin.ModelAdmin):

    list_display = ('header', 'category', 'plan', 'order', 'time_modified')
    search_fields = ['header']

admin.site.register(User, UserAdmin)
admin.site.register(Session)
admin.site.register(Plan, PlanAdmin)
admin.site.register(Collaboration)
admin.site.register(Event, EventAdmin)
