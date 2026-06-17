from django.contrib import admin
from .models import ContactMessage, Event, ProgramApplication, StudentProfile, Testimonial, TeamMember, Program


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'interest', 'created_at', 'is_read']
    list_filter = ['interest', 'is_read', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'message']
    readonly_fields = ['created_at']
    list_editable = ['is_read']
    ordering = ['-created_at']

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = 'Mark selected as read'
    actions = ['mark_as_read']


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'initials', 'order', 'is_active']
    list_editable = ['order', 'is_active']


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'initials', 'order', 'is_active']
    list_editable = ['order', 'is_active']


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ['title', 'icon', 'tag', 'order', 'is_active']
    list_editable = ['order', 'is_active']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'venue', 'event_date', 'event_time', 'order', 'is_active']
    list_filter = ['is_active', 'event_date']
    search_fields = ['title', 'description', 'venue']
    list_editable = ['order', 'is_active']


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'age', 'location', 'school_or_organization', 'created_at']
    search_fields = ['user__first_name', 'user__last_name', 'user__username', 'user__email', 'phone', 'location']
    readonly_fields = ['created_at']


@admin.register(ProgramApplication)
class ProgramApplicationAdmin(admin.ModelAdmin):
    list_display = ['user', 'program', 'status', 'created_at']
    list_filter = ['status', 'program', 'created_at']
    search_fields = ['user__first_name', 'user__last_name', 'user__username', 'program__title', 'motivation']
    list_editable = ['status']
    readonly_fields = ['created_at']
