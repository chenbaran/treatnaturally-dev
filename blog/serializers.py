from rest_framework import serializers
from .models import BlogPost, BlogPostImage


class BlogPostImageSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        blogpost_id = self.context['blogpost_id']
        return BlogPostImage.objects.create(blogpost_id=blogpost_id, **validated_data)

    class Meta:
        model = BlogPostImage
        fields = ['id', 'image']

class BlogSerializer(serializers.ModelSerializer):
    image = BlogPostImageSerializer(many=True, read_only=True)
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'image', 'last_update']