#-------------Abstract class for all models in the project-------------#
from django.db import models
from django.utils import timezone
from .manager import GeneralManager, AllObjectsManager

#----TimeStampedModel: An abstract base class that provides created_at and updated_at fields to track when records are created and modified.----#
class TimeStampedModel(models.Model):
	created_at = models.DateTimeField(default=timezone.now)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True


#-------------Abstract class for all models in the project-------------#
class SoftDeleteModel(models.Model):
	is_deleted = models.BooleanField(default=False)
	deleted_at = models.DateTimeField(null=True, blank=True)

	objects = GeneralManager()
	all_objects = AllObjectsManager()

	class Meta:
		abstract = True

	def delete(self, using=None, keep_parents=False, hard=False):
		if hard:
			return super().delete(using=using, keep_parents=keep_parents)
		self.is_deleted = True
		self.deleted_at = timezone.now()
		self.save()

	def restore(self):
		self.is_deleted = False
		self.deleted_at = None
		self.save()

#-----------Join TimeStampedModel and BaseModel to create a common base model for all models in the project-----------#
class CommonModel(TimeStampedModel, SoftDeleteModel):
    class Meta:
        abstract = True   