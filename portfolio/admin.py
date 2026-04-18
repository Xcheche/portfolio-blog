from django.contrib import admin
from .models import Category, Portfolio


class SoftDeleteAdminMixin:
    readonly_fields = ("is_deleted", "deleted_at", "updated_at")
    actions = ("restore_selected", "soft_delete_selected", "hard_delete_selected")

    def get_queryset(self, request):
        return self.model.all_objects.all()

    @admin.action(description="Restore selected records")
    def restore_selected(self, request, queryset):
        queryset.restore()

    @admin.action(description="Soft delete selected records")
    def soft_delete_selected(self, request, queryset):
        queryset.delete()

    @admin.action(description="Hard delete selected records permanently")
    def hard_delete_selected(self, request, queryset):
        queryset.hard_delete()

    def delete_model(self, request, obj):
        obj.delete()

    def delete_queryset(self, request, queryset):
        queryset.delete()


class CategoryAdmin(SoftDeleteAdminMixin, admin.ModelAdmin):
    list_display = ("name", "slug", "is_deleted", "deleted_at")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
    list_filter = ("is_deleted", "created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("name", "slug")}),
        ("Soft Delete", {"fields": ("is_deleted", "deleted_at")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )


admin.site.register(Category, CategoryAdmin)


class PortfolioAdmin(SoftDeleteAdminMixin, admin.ModelAdmin):
    list_display = ("title", "user", "category", "status", "is_deleted", "deleted_at", "created_at", "updated_at","client")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "description", "tech_stack")
    list_filter = ("status", "is_deleted", "created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("user", "category", "client", "title", "slug", "description", "tech_stack")}),
        ("Media", {"fields": ("image1", "image2", "project_link")}),
        ("Publishing", {"fields": ("status",)}),
        ("Soft Delete", {"fields": ("is_deleted", "deleted_at")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

admin.site.register(Portfolio, PortfolioAdmin)