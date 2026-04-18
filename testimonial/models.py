from django.db import models
from Common.models import CommonModel
# Create your models here.

#----------------------------Testimonial model-------------------------#
class Testimonial(CommonModel):
    class PermissionChoices(models.TextChoices):
        YES = "yes", "Yes"
        #YES_ANONYMOUS = "yes_anonymous", "Yes, publish anonymously"
        NO = "no", "No"
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    role = models.CharField(max_length=255, blank=True, null=True)
   
    message = models.TextField()
    project_name = models.CharField(max_length=255, blank=True, null=True)
    permission_to_publish = models.CharField(max_length=20, choices=PermissionChoices.choices, 
                                             default=PermissionChoices.NO)
    testimonial_image = models.ImageField(upload_to="testimonial_images/", blank=True, null=True)
    is_approved = models.BooleanField(default=False)

    

    def __str__(self):
        return self.full_name

    class Meta:
        
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"
