from django.dispatch import receiver
from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import transaction
from core.emails import send_user_registration_mail, send_contact_form_entry_alert_mail
from store.signals import order_created
from django.db.models.signals import pre_save
from core.models import ContactFormEntry

@receiver(order_created)
def on_order_created(sender, **kwargs):
  print(kwargs['order'])



# @receiver(pre_save, sender=settings.AUTH_USER_MODEL)
# def send_registration_success(sender, instance, **kwargs):
#     if instance._state.adding:
#         transaction.on_commit(lambda: send_user_registration_mail(instance))


# send new contact form entry alert to admin
@receiver(post_save, sender=ContactFormEntry)
def send_order_confirmation(sender, instance, created, **kwargs):
    if created:
        transaction.on_commit(lambda: send_contact_form_entry_alert_mail(instance))