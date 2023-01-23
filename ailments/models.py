from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class AilmentItemManager(models.Manager):
    def get_tags_for(self, obj_type, obj_id):
        content_type = ContentType.objects.get_for_model(obj_type)

        return AilmentItem.objects \
            .select_related('ailment') \
            .filter(
                content_type=content_type,
                object_id=obj_id
            )


class Ailment(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.title


class AilmentItem(models.Model):
    objects = AilmentItemManager()
    ailment = models.ForeignKey(Ailment, on_delete=models.CASCADE, related_name='ailmentitems')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
