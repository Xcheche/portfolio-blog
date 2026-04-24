from django.db import models
from django.core.files.storage import default_storage
from django_resized import ResizedImageField
from Common.models import CommonModel
#Import default image function for portfolio models

# Create your models here.


#Default image
def default_image():
    # ImageField defaults must be storage-relative names, not full URLs.
    """
    Returns the default image path for portfolio items  from cloud storage. This function is used as the default value for the image fields in the Portfolio model, ensuring that if no image is uploaded, a default image from the cloud storage will be used instead.

    """
    return "portfolio_images/default-image.png"



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
    testimonial_image = ResizedImageField(upload_to="testimonial_images/", blank=True, null=True, default=default_image)
    is_approved = models.BooleanField(default=False)

    

    def __str__(self):
        return self.full_name

    @property
    def default_image_url(self):
        return default_storage.url(default_image())

    class Meta:
        
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"
