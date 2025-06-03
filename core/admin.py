from django.contrib import admin
from .models import SiteConfiguration, FAQ, ContactMessage

@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'maintenance_mode', 'contact_email')
    search_fields = ('site_name', 'contact_email')

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'order', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('question', 'answer')
    list_editable = ('order', 'is_active')
    ordering = ('order',)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'name', 'email', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at',)
    list_editable = ('is_read',)
    ordering = ('-created_at',)

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected messages as read"

    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = "Mark selected messages as unread"

    actions = [mark_as_read, mark_as_unread]
