from django.db import models
from .validators import validate_file_size

class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(null=True, blank=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['last_update']

class BlogPostImage(models.Model):
    blogpost = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='image')
    image = models.ImageField(
        upload_to='blog/images',
        validators=[validate_file_size])
