from django.db import models

from Common.models import CommonModel

# Create your models here.


class Contact(CommonModel):
    name = models.CharField(max_length=255)

    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.email}"

    @property
    def full_name(self):
        return f"{self.name} - {self.email}"