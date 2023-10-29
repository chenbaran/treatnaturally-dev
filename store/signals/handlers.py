from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import transaction
from store.models import BillingAddress, Customer, OptionalShippingAddress, Order
from store.emails import send_order_alert_to_admin, send_order_confirmation_email
from core.emails import send_user_registration_mail

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_customer_for_new_user(sender, **kwargs):
    if kwargs['created']:
      Customer.objects.create(user=kwargs['instance'])


@receiver(post_save, sender=Customer)
def send_user_creation_email_on_membership_update(sender, instance, **kwargs):
    customer = instance
    if customer.membership:
        if post_save:
            transaction.on_commit(lambda:send_user_registration_mail(instance.user))


@receiver(post_save, sender=BillingAddress)
def update_customer_billing_address(sender, instance, created, **kwargs):
    customer = instance.customer
    if customer:
        if created:
            customer.billing_address_id = instance.id
            customer.save()


@receiver(post_delete, sender=BillingAddress)
def delete_customer_billing_address(sender, instance, **kwargs):
    customer = instance.customer
    if customer:
        customer.billing_address_id = None
        customer.save()


@receiver(post_save, sender=OptionalShippingAddress)
def update_customer_optional_shipping_address(sender, instance, created, **kwargs):
    customer = instance.customer
    if customer:
        if created:
            customer.optional_shipping_address_id = instance.id
            customer.save()


@receiver(post_delete, sender=OptionalShippingAddress)
def delete_customer_optional_shipping_address(sender, instance, **kwargs):
    customer = instance.customer
    if customer:
        customer.optional_shipping_address_id = None
        customer.save()


# send order confirmation email
@receiver(post_save, sender=Order)
def send_order_confirmation(sender, instance, created, **kwargs):
    if created:
        transaction.on_commit(lambda: send_order_confirmation_email(instance))
        transaction.on_commit(lambda: send_order_alert_to_admin(instance))