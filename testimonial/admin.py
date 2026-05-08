from django.contrib import admin
from django.db import models


from Common.email import send_testimonial_approved_email
from testimonial.models import Testimonial
# Register your models here.

class TestimonialAdmin(admin.ModelAdmin):
   
    list_display = ('full_name', 'email', 'project_name', 'permission_to_publish', 'created_at', 'is_approved','role')
    list_filter = ('permission_to_publish', 'created_at', 'is_approved','role')
    search_fields = ('full_name', 'email', 'project_name')
    list_editable = ('is_approved',)



    
    # Override save_model to send email notification when a testimonial is approved.
    def save_model(self, request, obj, form, change):
        previous_is_approved = None
        if change and obj.pk:
            previous_is_approved = (
                Testimonial.objects.filter(pk=obj.pk).values_list("is_approved", flat=True).first()
            )

        super().save_model(request, obj, form, change)

        if change and previous_is_approved is False and obj.is_approved is True:
            # Send email notification to user when their testimonial is approved.
            send_testimonial_approved_email(obj)

admin.site.register(Testimonial, TestimonialAdmin)