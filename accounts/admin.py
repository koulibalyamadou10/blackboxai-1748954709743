from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile, SellerProfile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class SellerProfileInline(admin.StackedInline):
    model = SellerProfile
    can_delete = False
    verbose_name_plural = 'Seller Profile'
    fk_name = 'user'

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, SellerProfileInline)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_seller')
    list_filter = BaseUserAdmin.list_filter + ('profile__is_seller',)

    def is_seller(self, obj):
        return obj.profile.is_seller
    is_seller.boolean = True
    is_seller.short_description = 'Seller Status'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_seller', 'created_at', 'updated_at')
    list_filter = ('is_seller', 'created_at')
    search_fields = ('user__username', 'user__email', 'bio')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'verified', 'total_sales', 'rating')
    list_filter = ('verified',)
    search_fields = ('user__username', 'company_name')
    readonly_fields = ('total_sales', 'rating')

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('user',)
        return self.readonly_fields

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
