from django.contrib import admin
from django.utils.html import format_html
from .models import Template, Category, Purchase

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'template_count')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')

    def template_count(self, obj):
        return obj.templates.count()
    template_count.short_description = 'Number of Templates'

@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'template_type', 'price', 
                   'preview_image_display', 'is_active', 'created_at')
    list_filter = ('is_active', 'template_type', 'category', 'created_at')
    search_fields = ('title', 'description', 'author__username')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('is_active', 'price')
    date_hierarchy = 'created_at'

    def preview_image_display(self, obj):
        if obj.preview_image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', 
                             obj.preview_image.url)
        return "No Image"
    preview_image_display.short_description = 'Preview'

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('author',)
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        if not change:  # if creating a new object
            obj.author = request.user
        super().save_model(request, obj, form, change)

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'user', 'template', 'amount', 'purchase_date')
    list_filter = ('purchase_date',)
    search_fields = ('transaction_id', 'user__username', 'template__title')
    readonly_fields = ('transaction_id', 'purchase_date', 'user', 'template', 'amount')
    date_hierarchy = 'purchase_date'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        # Only allow deletion through bulk actions by staff
        if request.user.is_staff and not obj:
            return True
        return False

    actions = ['export_as_csv']

    def export_as_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse
        from django.utils import timezone

        # Create the HttpResponse object with CSV header
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename=purchases-{timezone.now().date()}.csv'

        # Create the CSV writer
        writer = csv.writer(response)
        writer.writerow(['Transaction ID', 'User', 'Template', 'Amount', 'Purchase Date'])

        # Write the data
        for purchase in queryset:
            writer.writerow([
                purchase.transaction_id,
                purchase.user.username,
                purchase.template.title,
                purchase.amount,
                purchase.purchase_date
            ])

        return response
    export_as_csv.short_description = "Export selected purchases as CSV"
