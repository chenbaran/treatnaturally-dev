from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from .models import Ailment, AilmentItem


class DynamicPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        request = self.context.get('request')
        view = self.context.get('view')
        if request and view:
            model_class = view.get_queryset().model
            return model_class.objects.all()
        return super().get_queryset()

class AilmentItemSerializer(serializers.ModelSerializer):
    content_type = serializers.PrimaryKeyRelatedField(queryset=ContentType.objects.all())
    content_object = DynamicPrimaryKeyRelatedField(queryset=None)
    class Meta:
        model = AilmentItem
        fields = ['objects', 'ailment', 'content_type', 'object_id', 'content_object']


class AilmentSerializer(serializers.ModelSerializer):
    ailmentitems = AilmentItemSerializer(many=True)
    class Meta:
        model = Ailment
        fields = ['title', 'description', 'ailmentitems']