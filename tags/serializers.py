from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from .models import Tag, TaggedItem


class DynamicPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        request = self.context.get('request')
        view = self.context.get('view')
        if request and view:
            model_class = view.get_queryset().model
            return model_class.objects.all()
        return super().get_queryset()

class TaggedItemSerializer(serializers.ModelSerializer):
    content_type = serializers.PrimaryKeyRelatedField(queryset=ContentType.objects.all())
    content_object = DynamicPrimaryKeyRelatedField(queryset=None)
    class Meta:
        model = TaggedItem
        fields = ['objects', 'tag', 'content_type', 'object_id', 'content_object']


class TagSerializer(serializers.ModelSerializer):
    taggeditems = TaggedItemSerializer(many=True)
    class Meta:
        model = Tag
        fields = ['label', 'taggeditems']