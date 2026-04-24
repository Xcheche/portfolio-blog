from django.db import models
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
from django_resized import ResizedImageField

from django.contrib.auth.models import AbstractUser, UserManager
from Common.manager import CommonQuerySet, GeneralManager, AllObjectsManager
from Common.models import CommonModel
# Create your models here.



#Default image
def default_image():
    # ImageField defaults must be storage-relative names, not full URLs.
    """
    Returns the default image path for portfolio items  from cloud storage. This function is used as the default value for the image fields in the Portfolio model, ensuring that if no image is uploaded, a default image from the cloud storage will be used instead.

    """
    return "portfolio_images/default-image.png"



class ActiveUserManager(UserManager.from_queryset(CommonQuerySet)):
    def get_queryset(self):
        return super().get_queryset().alive()

    def _create_or_revive_user(self, email, password=None, **extra_fields):
        username = extra_fields.pop("username", None)
        existing_user = self.model.all_objects.filter(email__iexact=email).first()
        if existing_user is None:
            user = self.model(email=email, username=username, **extra_fields)
            if password:
                user.set_password(password)
            else:
                user.set_unusable_password()
            user.save(using=self._db)
            return user
        if not existing_user.is_deleted:
            raise ValidationError({"email": "A user with that email already exists."})

        if username is not None:
            existing_user.username = username
        for field, value in extra_fields.items():
            setattr(existing_user, field, value)

        existing_user.is_deleted = False
        existing_user.deleted_at = None
        existing_user.is_active = extra_fields.get("is_active", True)
        existing_user.is_staff = extra_fields.get("is_staff", False)
        existing_user.is_superuser = extra_fields.get("is_superuser", False)
        if password:
            existing_user.set_password(password)
        else:
            existing_user.set_unusable_password()
        existing_user.save(using=self._db)
        return existing_user

    def create_user(self, email, username=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", True)
        return self._create_or_revive_user(email, password=password, username=username, **extra_fields)

    def create_superuser(self, email, username=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_or_revive_user(email, password=password, username=username, **extra_fields)


class AllUserObjectsManager(UserManager.from_queryset(CommonQuerySet)):
    pass

class CustomUser(CommonModel, AbstractUser):
    # Extra fields
    email = models.EmailField(unique=True,null=False,blank=False)
    bio = models.TextField(blank=True, null=True)
    profile_image = ResizedImageField(upload_to='profile_images/',size=[300, 300],
    crop=['middle', 'center'],
                                       blank=True, null=True, default=default_image)
    display_name = models.CharField(max_length=150, blank=True, null=True)
    whatsapp_link = models.URLField(blank=True, null=True)
        
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # Keep auth-compatible manager methods (create_user/create_superuser)
    # while filtering out soft-deleted users from the default queryset.
    objects = ActiveUserManager()
    all_objects = AllUserObjectsManager()


    def __str__(self):
        return self.display_name or self.username

    @property
    def default_image_url(self):
        return default_storage.url(default_image())



