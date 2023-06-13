from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ValidationError
from django.urls import reverse

# Create your models here.
class User(AbstractUser):
  email = models.EmailField(unique=True)

class Graphics(models.Model):
    class Meta:
        verbose_name_plural = 'Graphics'

    def __str__(self) -> str:
        return 'Homepage Graphics'

    def get_absolute_url(self):
        return reverse('admin:yourapp_graphics_change', args=[self.pk])

    def save(self, *args, **kwargs):
        if self.pk is None and Graphics.objects.exists():
          raise ValidationError('There can be only one instance of the Graphics model')
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
      raise ValidationError('Cannot delete instance of Graphics model')
    
class HomePageSlider(models.Model):
    graphics = models.ForeignKey(Graphics, on_delete=models.CASCADE, related_name='home_page_slider')
    subtitle = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='graphics/home_page_slider/', null=True, blank=True)
    link = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ['id']
        verbose_name_plural = 'Home Page Sliders'

class HomePageSmallPicture(models.Model):
    graphics = models.ForeignKey(Graphics, on_delete=models.CASCADE, related_name='home_page_small_picture')
    title = models.CharField(max_length=255, null=True, blank=True)
    subtitle = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='graphics/home_page_small_picture/', null=True, blank=True)
    link = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ['id']
        verbose_name_plural = 'Home Page Small Pictures'

class HomePageIcon(models.Model):
    graphics = models.ForeignKey(Graphics, on_delete=models.CASCADE, related_name='home_page_icon')
    title = models.CharField(max_length=255, null=True, blank=True)
    subtitle = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='graphics/home_page_slider/', null=True, blank=True)

    class Meta:
        ordering = ['id']
        verbose_name_plural = 'Home Page Icons'

class Logo(models.Model):
    graphics = models.OneToOneField(Graphics, on_delete=models.CASCADE, related_name='logo')
    image = models.ImageField(upload_to='graphics/logo/', null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Logos'
        
    def save(self, *args, **kwargs):
        if self.pk:
            obj = Logo.objects.get(pk=self.pk)
            if obj.image != self.image:
                obj.image.delete()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)


class ContactFormEntry(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    subject = models.CharField(max_length=255, null=True, blank=True)
    message = models.TextField(max_length=2550, null=True, blank=True)

    class Meta:
        ordering = ['id']
        verbose_name_plural = 'Contact Form Entries'