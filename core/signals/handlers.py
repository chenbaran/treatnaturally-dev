from django.dispatch import receiver
from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import transaction
from core.emails import send_user_registration_mail
from store.signals import order_created

@receiver(order_created)
def on_order_created(sender, **kwargs):
  print(kwargs['order'])


# send registration success email
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def send_registration_success(sender, instance, **kwargs):
    transaction.on_commit(lambda: send_user_registration_mail(instance))