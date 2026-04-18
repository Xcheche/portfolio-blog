from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("email", "username", "display_name", "is_staff", "is_active", "is_deleted", "deleted_at")
    list_filter = ("is_staff", "is_active", "is_deleted")
    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),
        ("Personal Info", {"fields": ("display_name", "bio", "profile_image", "whatsapp_link")}),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
        ("Soft Delete", {"fields": ("is_deleted", "deleted_at")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "username", "display_name", "bio", "profile_image", "whatsapp_link", "password1", "password2"),
        }),
    )
    search_fields = ("email",)
    ordering = ("email",)
    readonly_fields = ("is_deleted", "deleted_at")
    actions = ("restore_selected", "soft_delete_selected", "hard_delete_selected")

    def get_queryset(self, request):
        return self.model.all_objects.all()

    @admin.action(description="Restore selected users")
    def restore_selected(self, request, queryset):
        queryset.restore()

    @admin.action(description="Soft delete selected users")
    def soft_delete_selected(self, request, queryset):
        queryset.delete()

    @admin.action(description="Hard delete selected users permanently")
    def hard_delete_selected(self, request, queryset):
        queryset.hard_delete()

    def delete_model(self, request, obj):
        obj.delete()

    def delete_queryset(self, request, queryset):
        queryset.delete()

admin.site.register(CustomUser, CustomUserAdmin)