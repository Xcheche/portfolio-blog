from django.db import models
from django.utils import timezone

class CommonQuerySet(models.QuerySet):
    def alive(self):
        return self.filter(is_deleted=False)

    def deleted(self):
        return self.filter(is_deleted=True)

    def _has_status_field(self):
        return any(field.name == 'status' for field in self.model._meta.concrete_fields)

    def published(self):
        if not self._has_status_field():
            return self.none()
        return self.filter(status__iexact='published', is_deleted=False)

    def drafts(self):
        if not self._has_status_field():
            return self.none()
        return self.filter(status__iexact='draft', is_deleted=False)

    def delete(self):
        return super().update(is_deleted=True, deleted_at=timezone.now())

    def hard_delete(self):
        return super().delete()

    def restore(self):
        return super().update(is_deleted=False, deleted_at=None)


#---------------Custom manager to handle soft deletion and restoration of objects---------------#
class SoftDeleteManager(models.Manager.from_queryset(CommonQuerySet)):
    def get_queryset(self):
        return super().get_queryset().alive()


class GeneralManager(SoftDeleteManager):
    pass


class AllObjectsManager(models.Manager.from_queryset(CommonQuerySet)):
    pass